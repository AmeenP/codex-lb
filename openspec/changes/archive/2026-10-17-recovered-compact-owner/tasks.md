## Tasks
- [x] Add scoped completed-recovery recognition for compaction affinity.
- [x] Cover actual compact routing after recovery and rejected proof/conflicting ownership.
- [x] Deploy and verify SPAOS recovery without changing conversation files.
- [x] Record the patch as one commit and internal PR.

Verification: 126 compact/quota/version tests passed in a clean archive; removing the completed-anchor guard produced two expected failures. The affected SPAOS synthetic key returned 503 before deployment and 200 response.compaction after deployment. Both hosts report ameen.4; both affected rollout prefixes remain byte-identical. Internal PR: https://github.com/AmeenP/codex-lb/pull/7.
