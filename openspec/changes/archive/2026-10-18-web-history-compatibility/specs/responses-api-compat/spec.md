## ADDED Requirements

### Requirement: Explicit incompatible web-action replay adapter
The proxy MUST default replay_web_action_as_text_ids to an empty list. Only completed web_search_call records whose IDs are explicitly listed MAY be converted to assistant text containing the entire original JSON record. Other records MUST remain unchanged. Conversion MUST be idempotent and MUST NOT modify saved conversation files.

#### Scenario: Operator enables a verified incompatible record
- **GIVEN** an operator lists the ID of a completed web action
- **WHEN** that record is normalized for a Responses request
- **THEN** its complete JSON is preserved as historical assistant text
- **AND** unlisted and incomplete records remain native items
