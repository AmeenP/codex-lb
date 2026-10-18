## ADDED Requirements

### Requirement: Desktop annotations remain compatible with same-owner replay
The proxy MUST allow recognized desktop annotations containing optional turn_id, positive finite create_time, and nonempty string content_item_kinds when proving a full resend for the same durable owner. Supplied turn_id MUST be nonblank. Unknown or malformed annotations MUST fail proof. Classification MUST NOT mutate the original input or authorize cross-account replay. Missing prior output, incomplete tool calls, owner conflicts, and replay settlement fences MUST retain existing protections.

#### Scenario: Annotation without a turn ID
- **GIVEN** a verified stored prefix contains a developer message annotated only with content_item_kinds
- **AND** the suffix retains prior assistant output and an agent followup
- **WHEN** a fresh bridge is required
- **THEN** the complete input is sent once to its existing owner without the stale proxy-injected anchor
- **AND** original metadata and encrypted content remain unchanged

### Requirement: Explicit incompatible web-action replay adapter
The proxy MUST default replay_web_action_as_text_ids to an empty list. Only completed web_search_call records whose IDs are explicitly listed MAY be converted to assistant text containing the entire original JSON record. Other records MUST remain unchanged. Conversion MUST be idempotent and MUST NOT modify saved conversation files.

#### Scenario: Operator enables a verified incompatible record
- **GIVEN** an operator lists the ID of a completed web action
- **WHEN** that record is normalized for a Responses request
- **THEN** its complete JSON is preserved as historical assistant text
- **AND** unlisted and incomplete records remain native items
