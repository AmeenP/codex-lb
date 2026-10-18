# Maintained fork patches

Baseline: upstream/main `72630bbfeee9e3b0d9acfb95e2b1e706b8b0188e`.

| Patch | Purpose | Internal PR | Origin |
|---|---|---|---|
| P01 | Preserve agent context across reconnects | [#1](https://github.com/AmeenP/codex-lb/pull/1) | Soju06/codex-lb#2581 |
| P02 | Preserve quota reset evidence during retries | [#2](https://github.com/AmeenP/codex-lb/pull/2) | Soju06/codex-lb#2440 |
| P03 | Accept desktop annotations in same-owner full-history recovery | [#3](https://github.com/AmeenP/codex-lb/pull/3) | Local reconnect repair |
| P04 | Preserve explicitly listed incompatible web actions as complete JSON text | [#4](https://github.com/AmeenP/codex-lb/pull/4) | Local history repair |
| P05 | Identify and document the deployed fork build | [#5](https://github.com/AmeenP/codex-lb/pull/5) | Fork maintenance |

Each patch has exactly one commit and one PR in AmeenP/codex-lb. PRs are stacked in the order above. P03 depends on P01; the linear stack keeps each diff reviewable. The default stable branch contains the whole stack. The original deployment tag and backup tag retain pre-cleanup history.

Runtime code, tests, dependency lock, and frontend source match the verified deployed build. Reorganizing these commits does not modify accounts, service configuration, or conversation files and requires no restart.

Build from the fork with bundled frontend assets and locked dependencies. Before future deployment, preserve the installed environment, service configuration, and a consistent database backup. Keep per-record compatibility IDs in host configuration. Do not replace this fork with the registry release without checking patch equivalence.
