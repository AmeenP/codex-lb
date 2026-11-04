## ADDED Requirements

### Requirement: Verified retained context can recover from an operator pause
With retained-context recovery enabled, the HTTP bridge SHALL replay verified
history after `previous_response_owner_unavailable` or `continuity_owner_policy_conflict`
only for a fresh persisted paused owner in scope and not pending deletion.
Existing history, anchor and resource checks MUST pass. Eligible replacement
selection MUST exclude the owner and preserve input items and conversation files.
The owner MUST remain paused.

#### Scenario: Intentional switch away from the previous owner
- **WHEN** a verified full-history resend belongs to a paused account and recovery is enabled
- **THEN** the bridge SHALL select an eligible replacement and replay the complete input without the old anchor
- **AND** the paused account SHALL remain paused

#### Scenario: Pause recovery is unproven
- **WHEN** history is incomplete, a resource is owner-bound, the owner is outside scope or pending deletion, the status lookup fails, or recovery is disabled
- **THEN** the bridge SHALL preserve the existing error and SHALL NOT authorize pause recovery
