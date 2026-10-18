from contextlib import asynccontextmanager, nullcontext
from copy import deepcopy
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest

from app.core.clients.proxy import ProxyResponseError
from app.core.config.settings import Settings
from app.core.openai.requests import ResponsesRequest
from app.db.models import AccountStatus, HttpBridgeSessionState
from app.modules.proxy import service as proxy_service
from app.modules.proxy.replay_safety import (
    responses_payload_is_account_neutral_fresh_replay,
    responses_payload_is_retained_context_replay,
)
from tests.unit.test_proxy_http_bridge import _make_bridge_session
from tests.unit.test_replay_safety import _agent_followup


@pytest.fixture
def desktop_payload():
    return {
        "model": "gpt-6-astra",
        "instructions": "Continue the task.",
        "input": [
            {
                "type": "additional_tools",
                "role": "developer",
                "tools": [
                    {
                        "type": "namespace",
                        "name": "functions",
                        "description": "Local tools",
                        "tools": [
                            {"type": "custom", "name": "shell"},
                        ],
                    },
                ],
            },
            {"type": "compaction", "id": "cmp_1", "encrypted_content": "retained-compaction"},
            {
                "role": "developer",
                "id": "dev_1",
                "content": "Keep the context.",
                "internal_chat_message_metadata_passthrough": {"content_item_kinds": ["text"]},
            },
            {"role": "user", "content": "Inspect the workspace."},
            {"type": "reasoning", "id": "rs_1", "encrypted_content": "retained-reasoning", "summary": []},
            {
                "type": "custom_tool_call",
                "name": "shell",
                "call_id": "call_1",
                "input": "pwd",
            },
            {"type": "custom_tool_call_output", "call_id": "call_1", "output": "/workspace"},
            _agent_followup(),
        ],
        "reasoning": {"effort": "xhigh", "summary": "detailed", "context": "all_turns"},
        "stream_options": {"reasoning_summary_delivery": "sequential_cutoff"},
        "client_metadata": {"thread_id": "thread_1", "guardian_credits_requested": "true"},
    }


def test_retained_context_validation_preserves_original_and_strict_default(desktop_payload):
    original = deepcopy(desktop_payload)
    assert responses_payload_is_retained_context_replay(desktop_payload)
    assert not responses_payload_is_account_neutral_fresh_replay(desktop_payload)
    assert desktop_payload == original
    assert Settings().quota_failover_retained_context_enabled is False


@pytest.mark.parametrize(
    "bad",
    [
        "file",
        "container",
        "orphan",
        "unknown",
        "agent_resource",
        "blank_ciphertext",
        "metadata",
        "namespace",
        "hosted_tool",
        "conversation",
        "anchor",
        "stream_options",
        "reasoning",
    ],
)
def test_retained_context_rejects_nonportable_or_unknown_state(desktop_payload, bad):
    p = desktop_payload
    if bad == "file":
        p["input"].append({"role": "user", "content": [{"type": "input_file", "file_id": "file_owner"}]})
    elif bad == "container":
        p["input"].append({"type": "code_interpreter_call", "container_id": "container_owner"})
    elif bad == "orphan":
        p["input"] = [x for x in p["input"] if x.get("type") != "custom_tool_call"]
    elif bad == "unknown":
        p["input"][1]["future_state"] = "unknown"
    elif bad == "agent_resource":
        p["input"][-1]["content"].append({"type": "input_file", "file_id": "file_owner"})
    elif bad == "blank_ciphertext":
        p["input"][1]["encrypted_content"] = " "
    elif bad == "metadata":
        p["input"][2]["internal_chat_message_metadata_passthrough"]["owner"] = "account_1"
    elif bad == "namespace":
        p["input"][5]["namespace"] = {"id": "opaque"}
    elif bad == "hosted_tool":
        p["input"][0]["tools"][0]["tools"].append({"type": "file_search", "vector_store_ids": ["vs_owner"]})
    elif bad == "conversation":
        p["conversation"] = "conv_owner"
    elif bad == "anchor":
        p["previous_response_id"] = "resp_owner"
    elif bad == "stream_options":
        p["stream_options"]["unknown"] = True
    else:
        p["reasoning"]["context"] = "unknown"
    assert not responses_payload_is_retained_context_replay(p)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case", ["quota", "disabled", "non_quota", "missing_output", "changed_prefix", "file_pin", "wrong_anchor"]
)
async def test_bridge_quota_recovery_sends_intact_history_only_when_proven(
    monkeypatch, db_setup, desktop_payload, case
):
    service = proxy_service.ProxyService(cast(Any, nullcontext()))
    settings = Settings(quota_failover_retained_context_enabled=case != "disabled")
    monkeypatch.setattr(proxy_service, "get_settings", lambda: settings)
    dashboard = SimpleNamespace(
        sticky_threads_enabled=False,
        openai_cache_affinity_max_age_seconds=1800,
        http_responses_session_bridge_prompt_cache_idle_ttl_seconds=3600,
        http_responses_session_bridge_gateway_safe_mode=False,
    )
    monkeypatch.setattr(
        proxy_service, "get_settings_cache", lambda: SimpleNamespace(get=AsyncMock(return_value=dashboard))
    )
    stored_count = 4
    lookup = proxy_service.DurableBridgeLookup(
        session_id="durable-quota-test",
        canonical_kind="thread_header",
        canonical_key="thread_quota_test",
        api_key_scope="__anonymous__",
        account_id="exhausted",
        owner_instance_id=None,
        owner_epoch=1,
        lease_expires_at=None,
        state=HttpBridgeSessionState.CLOSED,
        latest_turn_state="http_turn_quota_test",
        latest_response_id="resp_last",
        latest_input_item_count=stored_count,
        latest_input_full_fingerprint=proxy_service._fingerprint_input_items(desktop_payload["input"][:stored_count]),
        latest_pending_tool_calls={"call_1": "custom_tool_call"},
        model="gpt-6-astra",
    )
    if case == "missing_output":
        desktop_payload["input"] = [x for x in desktop_payload["input"] if x.get("type") != "custom_tool_call_output"]
    elif case == "changed_prefix":
        desktop_payload["input"][3]["content"] = "Changed old question."
    elif case == "wrong_anchor":
        desktop_payload["previous_response_id"] = "resp_other"
    payload = ResponsesRequest.model_validate(desktop_payload)
    quota_check = AsyncMock(return_value=case != "non_quota")
    monkeypatch.setattr(service, "_owner_selection_loss_is_quota_caused", quota_check)
    monkeypatch.setattr(service._durable_bridge, "lookup_request_targets", AsyncMock(return_value=lookup))
    monkeypatch.setattr(
        service._durable_bridge, "retire_continuity_owner_if_unavailable", AsyncMock(return_value=False)
    )
    monkeypatch.setattr(service, "_http_bridge_has_live_local_session", AsyncMock(return_value=False))
    monkeypatch.setattr(service, "_http_bridge_can_forward_to_active_owner", AsyncMock(return_value=False))
    monkeypatch.setattr(
        service,
        "_resolve_file_account_for_responses",
        AsyncMock(return_value="exhausted" if case == "file_pin" else None),
    )
    monkeypatch.setattr(service, "_http_bridge_local_owner_account_id", AsyncMock(return_value="exhausted"))
    monkeypatch.setattr(service, "_resolve_websocket_previous_response_owner", AsyncMock(return_value="exhausted"))
    failure = ProxyResponseError(
        502, proxy_service.openai_error("previous_response_owner_unavailable", "Owner unavailable")
    )
    session = _make_bridge_session()
    session.request_model = "gpt-6-astra"
    create = AsyncMock(side_effect=[failure, session])
    monkeypatch.setattr(service, "_get_or_create_http_bridge_session", create)
    sent = []

    async def stream_events(_session, **kwargs):
        import json

        sent.append(json.loads(kwargs["text_data"]))
        yield 'data: {"type":"response.completed"}\n\n'

    monkeypatch.setattr(service, "_stream_http_bridge_session_events", stream_events)
    stream = service._stream_via_http_bridge(
        payload,
        headers={"thread-id": "thread_quota_test", "x-codex-turn-state": "http_turn_quota_test"},
        codex_session_affinity=True,
        propagate_http_errors=True,
        openai_cache_affinity=True,
        api_key=None,
        api_key_reservation=None,
        suppress_text_done_events=False,
        idle_ttl_seconds=120,
        codex_idle_ttl_seconds=1800,
        max_sessions=8,
        queue_limit=4,
        enforce_openai_sdk_contract=False,
        rewritten_file_account_id="exhausted" if case == "file_pin" else None,
    )
    if case != "quota":
        with pytest.raises(ProxyResponseError):
            _ = [chunk async for chunk in stream]
        assert not sent
        assert create.await_count <= 1
        return
    assert [chunk async for chunk in stream] == ['data: {"type":"response.completed"}\n\n']
    assert sent[0]["input"] == desktop_payload["input"]
    assert sent[0].get("previous_response_id") is None
    assert create.await_count == 2
    replacement = create.await_args_list[1].kwargs
    assert replacement["preferred_account_id"] is None
    assert "exhausted" in replacement["exclude_account_ids"]
    assert "thread-id" not in replacement["headers"]
    assert "x-codex-turn-state" not in replacement["headers"]
    quota_check.assert_awaited_once_with("exhausted")


@pytest.mark.asyncio
@pytest.mark.parametrize("status", list(AccountStatus) + [None, "lookup_failure"])
async def test_shared_owner_quota_check_requires_persisted_quota_status(status):
    account = SimpleNamespace(status=status) if status is not None else None
    get = AsyncMock(
        return_value=account, side_effect=RuntimeError("lookup failure") if status == "lookup_failure" else None
    )

    @asynccontextmanager
    async def repos():
        yield SimpleNamespace(accounts=SimpleNamespace(get_by_id_fresh=get))

    service = proxy_service.ProxyService(repos)
    assert await service._owner_selection_loss_is_quota_caused("owner") == (
        status in (AccountStatus.RATE_LIMITED, AccountStatus.QUOTA_EXCEEDED)
    )
