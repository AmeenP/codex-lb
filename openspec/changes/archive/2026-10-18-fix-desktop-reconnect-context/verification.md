# Verification

- Reconstructed the 327-item failing request from the private upstream capture and saved rollout. The old same-owner proof rejected a developer annotation containing only content_item_kinds. The corrected bound proof accepts the complete request without changing input.
- 1,506 request/replay/HTTP bridge unit tests passed.
- 69 focused tests passed, including both Responses HTTP routes, original owner retention, stale-anchor recovery, no replay after visible output, unavailable owners, missing tool output, and unavailable settlement fences.
- Frontend typecheck/build, changed Python lint/format/type checks, wheel asset validation, and strict change validation passed.
- All 67 OpenSpec capabilities validate (existing advisory warnings remain).
- Upgrade of a private database backup reached the upstream merge head with migration_policy=ok and schema_drift=none. The retired overflow feature is unused on both deployment hosts.
- An additional 130 settings, quota-reset, and bridge-recovery tests passed.
- Deployed the identical `1.25.0b9+ameen.2` wheel on macOS and Linux, code commit `b42df6dc4852ec4c60f2bfaf49a6b16a808edfa2`, SHA-256 `fed5db60b39f10361ea101a623afba496775e17cc278138182a31758883b5e82`. Runtime readiness and version headers verified on both hosts.
- Live isolated sessions on both hosts completed a first response, survived a service restart, then accepted a full resend containing the missing-turn-ID developer annotation, prior assistant output, and an agent followup. Each logged `fresh_reattach_full_resend_preserved`, retained its owner, and reached `response.completed` without an error (2.47 s macOS, 3.59 s Linux).
- Post-deployment observation: zero rejected-anchor errors; 17 successful requests in the original affected conversation; 33 successful Linux and 19 successful macOS requests overall at the verification snapshot. Two initial synthetic probes per host had unsupported parallel_tool_calls payload settings; correcting the probe to the actual Responses-Lite contract resolved those test-only errors.
- Both existing conversation-file prefixes passed SHA-256 comparison (57,700,432 and 152,258,593 bytes). The active file continued growing normally. All eight account identities and routing policies match the backups. Conversation archiving remains off.
- Full installed environments, service configuration, and consistent SQLite backups remain locally on each host. No saved conversation content was edited.
