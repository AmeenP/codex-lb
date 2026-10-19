# P09: Refresh model availability after reauthentication

## Why
Successful login restores account credentials but leaves the authoritative model catalog unchanged until the five-minute scheduler tick. Requests can fail locally with no_plan_support_for_model even though the recovered account supports the requested model.

## What Changes
- Publish a model-refresh request after committed OAuth credentials or auth-file imports.
- Wake the existing serialized, leader-gated scheduler through the shared invalidation bus.
- Preserve login success during discovery failures and retain periodic retry behavior.

## Impact
OAuth, account import, model-refresh scheduling, and model-catalog-compat. No deployment, schema migration, account policy change, or conversation-history change.
