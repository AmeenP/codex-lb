# Verification

- Reconstructed the 327-item failing request from the private upstream capture and saved rollout. The old same-owner proof rejected a developer annotation containing only content_item_kinds. The corrected bound proof accepts the complete request without changing input.
- 1,506 request/replay/HTTP bridge unit tests passed.
- 69 focused tests passed, including both Responses HTTP routes, original owner retention, stale-anchor recovery, no replay after visible output, unavailable owners, missing tool output, and unavailable settlement fences.
- Frontend typecheck/build, changed Python lint/format/type checks, wheel asset validation, and strict change validation passed.
- All 67 OpenSpec capabilities validate (existing advisory warnings remain).
- Upgrade of a private database backup reached the upstream merge head with migration_policy=ok and schema_drift=none. The retired overflow feature is unused on both deployment hosts.
- Live deployment verification follows; no conversation files are modified by this change.
