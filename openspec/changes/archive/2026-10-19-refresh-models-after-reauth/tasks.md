## Implementation
- [x] Publish refresh requests after successful credential persistence.
- [x] Wake the owned scheduler without overlapping refreshes or losing requests during a fetch.
- [x] Cover OAuth recovery, imports, peer delivery, failed login, and scheduler lifecycle.
- [x] Validate code and specifications, sync the specification, and archive.

## Validation results
- 257 affected scheduler, OAuth, import, cache-bus, model-replication, and lifecycle tests passed.
- Strengthened selector-level regression: 4 cases passed; removing the OAuth signal makes the recovery test fail, restoring it passes.
- `make lint` passed. The change's strict OpenSpec validation passed.
- Full type checking reports 35 existing diagnostics, byte-identical to the base after normalizing checkout paths.
- Full strict OpenSpec validation has the existing baseline result: 8 passed, 59 failed.
- Full `make ci` stops at the frontend prerequisite because `bun` is unavailable. No CI-green or deployment claim is made.
