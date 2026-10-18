## ADDED Requirements

### Requirement: Opt-in quota failover preserves retained desktop context
When `quota_failover_retained_context_enabled` is enabled, the HTTP Responses
bridge MAY replay a verified full resend on a different account after the
durable owner becomes rate-limited or quota-exceeded. The bridge MUST verify
the original stored prefix and retained output or exact pending-call manifest
before removing an anchor. It MUST preserve all original input items, IDs,
annotations and encrypted content in the replacement request. It MUST exclude
the exhausted owner and use the existing fenced recovery and alias publication
path. It MUST NOT replay a file-pinned request, a mismatched explicit anchor,
unknown context shapes, or a request whose owner's quota status is unconfirmed.
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
