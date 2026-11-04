## ADDED Requirements

### Requirement: Accept encrypted-output include requests
Responses request validation SHALL accept `output.encrypted_content` in `include`
and preserve it in the upstream request. Unsupported include values MUST remain
validation errors.

#### Scenario: Desktop requests encrypted output
- **WHEN** a desktop Responses request includes `output.encrypted_content`
- **THEN** request validation SHALL accept it and forward that include value unchanged

#### Scenario: Unknown include value
- **WHEN** a request includes an unsupported value
- **THEN** request validation SHALL reject it
