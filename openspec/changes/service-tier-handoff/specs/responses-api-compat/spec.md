## ADDED Requirements

### Requirement: Verified retained context can recover from service tier owner exclusion
When retained-context recovery is enabled, the HTTP bridge SHALL permit an intact replay after `continuity_owner_policy_conflict` or a locally proven pre-submission continuity refusal only if a scoped authoritative catalog proves the active owner supports the unchanged model but not the explicitly requested tier, and another account in scope advertises that tier. The existing sealed full-history proof, matching owner and anchor, and resource portability checks MUST pass.

#### Scenario: Fast owner cannot serve Ultrafast
- **WHEN** an intact verified follow-up requests Ultrafast on the same model, excluding its active Fast-only owner
- **THEN** the proxy SHALL exclude that owner and select a tier-capable replacement through the existing recovery flow
- **AND** SHALL preserve the supplied input and requested tier without modifying conversation files

#### Scenario: Tier handoff cannot be proven
- **WHEN** history is incomplete, a resource is owner-bound, the model changed, the owner is paused or outside the API-key scope, or catalog evidence is missing
- **THEN** the proxy SHALL preserve the existing error and SHALL NOT authorize tier recovery

## MODIFIED Requirements

### Requirement: Opt-in quota failover preserves retained desktop context
When `quota_failover_retained_context_enabled` is enabled, the HTTP Responses
bridge MAY replay a verified full resend on a different account after the
durable owner becomes rate-limited or quota-exceeded. The bridge MUST verify
the original stored prefix and retained output or exact pending-call manifest
before removing an anchor. It MUST preserve all original input items, IDs,
annotations and encrypted content in the replacement request. It MUST exclude
the exhausted owner and use the existing fenced recovery and alias publication
path. It MUST NOT replay a file-pinned request, a mismatched explicit anchor,
unknown context shapes, or a request whose owner's quota status is unconfirmed unless the separate verified service-tier recovery requirement applies.
The setting MUST default to false. Failure on the replacement account MUST NOT
cause silent context removal or transcript modification.

#### Scenario: Exhausted owner with complete desktop history
- **GIVEN** opt-in is enabled, the stored prefix and output manifest match, and the owner is rate-limited
- **WHEN** a full resend includes recognized encrypted compaction, reasoning and agent messages
- **THEN** a replacement account receives the complete input without the previous-response anchor
- **AND** the old account and its session headers are excluded from recovery

#### Scenario: Missing history or non-quota owner failure
- **GIVEN** a resend omits prior output, references account-bound files, or the owner is paused or deactivated
- **WHEN** owner selection fails
- **THEN** retained-context quota failover is refused

#### Scenario: Existing default remains strict
- **GIVEN** the setting is disabled
- **WHEN** an encrypted full resend's owner is unavailable
- **THEN** the existing account-neutral proof still governs whether recovery is allowed

### Requirement: Quota recovery handles catalog policy conflicts
After 503 `continuity_owner_policy_conflict`, the HTTP bridge SHALL allow opt-in retained-context quota recovery only with a matching durable full-resend proof, persisted quota exhaustion, no input-file pin, and valid retained context. Replacement selection MUST enforce account eligibility and preserve complete input. Other policy failures MUST remain failures unless the separate verified service-tier recovery requirement applies.

#### Scenario: Exhausted owner omitted from the catalog
- **GIVEN** a verified full-history resend and a quota-exhausted durable owner
- **WHEN** admission rejects that owner with 503 `continuity_owner_policy_conflict` and retained-context quota recovery is enabled
- **THEN** the bridge retries the intact history without the old anchor through eligible replacement selection

#### Scenario: Policy rejection without quota evidence
- **GIVEN** a policy-conflict rejection without persisted quota exhaustion or verified service-tier recovery eligibility
- **WHEN** recovery is evaluated
- **THEN** the bridge preserves the failure and does not switch accounts

