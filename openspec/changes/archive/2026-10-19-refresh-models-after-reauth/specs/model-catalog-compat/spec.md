## ADDED Requirements

### Requirement: Credential recovery promptly refreshes model availability

After committing OAuth credentials or an auth-file import, the service MUST publish a model-refresh request through the shared invalidation bus before reporting success. On observing it, the scheduler MUST refresh without waiting for its periodic interval. Failed credential persistence MUST NOT publish a request. Only the leader SHALL fetch upstream; successful discovery MUST use existing registry persistence and selection-cache invalidation.

#### Scenario: Reauthentication restores a missing model
- **GIVEN** an authoritative catalog omits a model because its supporting account required reauthentication
- **WHEN** OAuth successfully restores that account and the refresh request is observed
- **THEN** the leader discovers models using committed credentials without waiting for the periodic interval
- **AND** a successful discovery restores verified model availability and invalidates selection caches

#### Scenario: Credential import reaches the scheduler leader
- **GIVEN** a replica other than the scheduler leader imports valid credentials
- **WHEN** the import commits and publishes its refresh request
- **THEN** the leader observes the shared signal and refreshes model availability

### Requirement: Recovery refreshes preserve scheduler lifecycle

Refresh requests MUST coalesce into the existing owned scheduler task without overlapping passes. Requests observed during discovery MUST cause a subsequent pass. Shutdown MUST cancel and await that task. Discovery failure MUST NOT undo login success, fabricate model access, or disable periodic retries.

#### Scenario: Reauthentication during an ongoing refresh
- **GIVEN** a model refresh is already in progress
- **WHEN** one or more credential-recovery requests arrive
- **THEN** the scheduler runs one subsequent pass after the current pass finishes
- **AND** it does not start concurrent discovery tasks

#### Scenario: Discovery fails after a successful login
- **WHEN** upstream model discovery fails after credentials have been saved
- **THEN** login remains successful and credentials remain stored
- **AND** existing catalog failure behavior and periodic retry remain in force
