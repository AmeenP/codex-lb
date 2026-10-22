# Recover stale rate limits after verified probes

## Why
Accounts retain old multi-day rate-limit deadlines even after completing responses with quota available. Force Probe currently accepts HTTP headers without checking streaming completion.

## What changes
Require response.completed before reporting probe success. Recover an unchanged rate_limited block after a completed probe and fresh available quota, guarded by a pre-request account snapshot and replica health version. Preserve newer failures, operator state, genuine quota exhaustion, and routing policies.

## Impact
Account probe API and load-balancer settlement; no schema migration or new configuration.
