## ADDED Requirements

### Requirement: Fork builds expose their version suffix
The maintained fork MUST expose its ameen build suffix in package metadata, the runtime X-App-Version header, and the frontend build version.

#### Scenario: Operator identifies the deployed fork
- **GIVEN** the ameen.2 wheel is installed
- **WHEN** the operator checks package metadata and a health response
- **THEN** both identify the ameen.2 build
- **AND** the bundled frontend uses the same build suffix
