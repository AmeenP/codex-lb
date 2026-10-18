## ADDED Requirements

### Requirement: Compaction follows a completed recovery alias
A compaction request with a proxy-synthesized turn-state MUST retain its resolved required account while omitting a stale sticky hint only when the exact API-key-scoped durable alias resolves to that account in the reserved account-neutral recovery namespace and records a completed response anchor. The proxy MUST preserve file and previous-response owner consistency checks and MUST NOT fall back to another account or rewrite conversation history.

#### Scenario: Old sticky mapping remains after successful quota handoff
- **GIVEN** a synthetic turn-state alias resolves to a completed recovery bridge on account B
- **AND** its raw sticky row still names account A
- **WHEN** compaction resolves account B without conflicting file or response ownership
- **THEN** compaction runs on B and does not rewrite the raw sticky row

#### Scenario: Recovery is unproven or another ownership source conflicts
- **GIVEN** the alias is missing, is not a recovery bridge, has no completed response, or resolves to a different required owner
- **WHEN** compaction is attempted
- **THEN** existing ownership conflict checks remain effective
