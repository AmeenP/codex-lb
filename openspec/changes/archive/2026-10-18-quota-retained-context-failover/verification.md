# Verification

- 393 focused recovery, replay-safety, compact, settings, and release-version tests passed; 88 additional selected bridge/reconnect tests passed.
- An isolated git archive export passed 56 recovery/configuration tests. Bypassing the persisted quota gate caused the non-quota regression test to fail; the original source bytes were restored.
- Changed Python files passed Ruff lint/format. Frontend build, wheel asset checks, and all 67 OpenSpec capability validations passed.
- Both hosts run the identical `1.25.0b9+ameen.3` wheel, SHA-256 `ee360c652fbfa3c3d3133204beacc34a8c4c2c2b34a82939b2cd05261c6ba8d8`. All 821 installed application/static files matched the wheel on each host. Readiness and version headers passed on macOS and SPAOS.
- The affected SPAOS conversation logged `quota_owner_retained_context_replay` and moved from its exhausted owner to another authorized account. The initial post-handoff observation contained 56 successful requests and zero errors.
- Both original rollout prefixes remained byte-identical to the pre-deployment backup (57,700,432 and 162,707,927 bytes). No conversation files were rewritten or truncated.
- Consistent database, installed environment, service configuration, and provenance backups were preserved on both hosts before deployment.
- P06 is one commit and one internal draft PR: https://github.com/AmeenP/codex-lb/pull/6. Independent source review found no actionable defect; full repository CI and human review remain outstanding.
