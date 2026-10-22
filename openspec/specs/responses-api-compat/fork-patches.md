# Maintained fork patches

Baseline: upstream/main `72630bbfeee9e3b0d9acfb95e2b1e706b8b0188e`.

| Patch | Purpose | Internal PR | Origin |
|---|---|---|---|
| P01 | Preserve agent context across reconnects | [#1](https://github.com/AmeenP/codex-lb/pull/1) | Soju06/codex-lb#2581 |
| P02 | Preserve quota reset evidence during retries | [#2](https://github.com/AmeenP/codex-lb/pull/2) | Soju06/codex-lb#2440 |
| P03 | Accept desktop annotations in same-owner full-history recovery | [#3](https://github.com/AmeenP/codex-lb/pull/3) | Local reconnect repair |
| P04 | Preserve explicitly listed incompatible web actions as complete JSON text | [#4](https://github.com/AmeenP/codex-lb/pull/4) | Local history repair |
| P05 | Identify and document the deployed fork build | [#5](https://github.com/AmeenP/codex-lb/pull/5) | Fork maintenance |
| P06 | Recover quota-exhausted sessions with intact retained context | [#6](https://github.com/AmeenP/codex-lb/pull/6) | Automatic quota failover |
| P07 | Follow the verified recovery owner during compaction | [#7](https://github.com/AmeenP/codex-lb/pull/7) | Post-handoff compaction repair |
| P08 | Recover quota-exhausted owners rejected by model eligibility | [#8](https://github.com/AmeenP/codex-lb/pull/8) | HTTP bridge 503 recovery |
| P09 | Refresh model availability after reauthentication | [#9](https://github.com/AmeenP/codex-lb/pull/9) | Account catalog refresh |
| P10 | Clear stale rate limits after completed probes | [#10](https://github.com/AmeenP/codex-lb/pull/10) | Account probe recovery |
| P11 | Preserve verified context when the requested tier excludes its owner | [#11](https://github.com/AmeenP/codex-lb/pull/11) | Fast-to-Ultrafast handoff |

Each patch has exactly one commit and one PR in AmeenP/codex-lb. PRs are stacked in the order above. P03 depends on P01; the linear stack keeps each diff reviewable. The default stable branch contains the whole stack. The original deployment tag and backup tag retain pre-cleanup history.

P01–P05 reorganized the original deployed build without changing runtime code. P06 adds opt-in automatic quota recovery with intact retained context (ameen.3); its deployment requires a service restart, but does not modify conversation files.

P07 fixes compaction after a completed recovery (ameen.4): a scoped durable recovery alias supersedes only a stale synthetic sticky hint. Required account ownership, input and historical mappings remain intact.

Build from the fork with bundled frontend assets and locked dependencies. Before future deployment, preserve the installed environment, service configuration, and a consistent database backup. Keep per-record compatibility IDs in host configuration. Do not replace this fork with the registry release without checking patch equivalence.
