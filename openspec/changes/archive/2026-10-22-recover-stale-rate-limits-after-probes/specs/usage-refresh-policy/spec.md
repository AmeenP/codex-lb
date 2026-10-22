## ADDED Requirements

### Requirement: Probe success requires streaming completion
Force Probe MUST report HTTP 2xx as successful only after receiving response.completed. Error, failed, incomplete, malformed-only, truncated, timed-out, and oversized streams MUST report the existing failure sentinel.

#### Scenario: Headers alone do not prove success
- **WHEN** upstream returns HTTP 200 but fails or closes without response.completed
- **THEN** the probe cannot clear a rate limit

### Requirement: Completed probes recover stale rate limits
A completed probe with a successful usage fetch SHALL clear an unchanged rate_limited status and persisted and replica-local cooldowns only when a new applicable quota sample exists and all known normalized applicable windows have quota. The existing 30-second block floor MUST remain enforced. Background refresh without a completed probe MUST continue respecting plausible cooldowns.

#### Scenario: Weekly-only account proves an old deadline stale
- **GIVEN** an unchanged multi-day rate-limit deadline and a block older than 30 seconds
- **WHEN** a probe completes and a weekly sample recorded after the probe began shows quota available
- **THEN** the response reports active and persisted and replica-local cooldowns are cleared

#### Scenario: Fresh quota is required
- **WHEN** usage fetch fails, produces no new applicable sample, or reports exhausted quota
- **THEN** a completed probe cannot clear the cooldown

### Requirement: Probe recovery preserves newer state
Recovery MUST compare status, reason, reset, and block markers with the pre-request snapshot and reject changed replica health versions. Newer failures, pauses, authentication failures, deletion, and quota exhaustion MUST win over an older probe. Routing policies and conversation history MUST remain unchanged.

#### Scenario: Concurrent changes survive recovery
- **GIVEN** an account starts a probe while rate limited
- **WHEN** a newer failure, pause, authentication failure, or deletion occurs before settlement
- **THEN** the stale probe cannot override that change
