## ADDED Requirements

### Requirement: Quota recovery handles catalog policy conflicts
After 503 `continuity_owner_policy_conflict`, the HTTP bridge SHALL allow opt-in retained-context quota recovery only with a matching durable full-resend proof, persisted quota exhaustion, no input-file pin, and valid retained context. Replacement selection MUST enforce account eligibility and preserve complete input. Other policy failures MUST remain failures.

#### Scenario: Exhausted owner omitted from the catalog
- **GIVEN** a verified full-history resend and a quota-exhausted durable owner
- **WHEN** admission rejects that owner with 503 `continuity_owner_policy_conflict` and retained-context quota recovery is enabled
- **THEN** the bridge retries the intact history without the old anchor through eligible replacement selection

#### Scenario: Policy rejection without quota evidence
- **GIVEN** a policy-conflict rejection without persisted quota exhaustion
- **WHEN** recovery is evaluated
- **THEN** the bridge preserves the failure and does not switch accounts
