The reconnect trace showed full input being trimmed against a durable response from an earlier socket, then previous_response_not_found and denied_proxy_anchor_before_dispatch. The recovered request has a developer annotation with content_item_kinds and no turn_id. Proof normalization is classification-only; wire data remains intact.

The web-action adapter is opt-in because only individual upstream-incompatible records were verified. Deployment stores the private ID in machine configuration, never in this repository. JSON representation retains all fields without modifying the Codex rollout.

Fork baseline: upstream/main 72630bbfeee9e3b0d9acfb95e2b1e706b8b0188e. The patch stack carries agent-message continuity (upstream PR 2581), quota reset evidence (PR 2440), desktop metadata/same-owner safeguards, and the explicit historical web-action adapter. The allowlist is a T4 incident compatibility setting because globally converting unverified native web records would change unaffected conversations.

Set CODEX_LB_REPLAY_WEB_ACTION_AS_TEXT_IDS to a JSON array of verified IDs only. Default is empty. This setting affects input normalization, including HTTP and WebSocket requests; it does not mutate rollouts, authentication, account policy, or persisted conversation records.

Deploy a wheel built from this fork with bundled frontend assets. Keep origin pointing at AmeenP/codex-lb and upstream at Soju06/codex-lb. Preserve database and service configuration backups before updating. Install the same wheel on both hosts with locked dependency constraints, record the commit and SHA-256 locally, and restart the existing service. Future updates must rebase these fixes on upstream/main and rerun the replay regression suite; do not replace the fork with a registry release.
