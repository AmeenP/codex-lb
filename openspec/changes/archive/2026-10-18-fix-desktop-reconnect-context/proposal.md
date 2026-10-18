# Desktop reconnect context (P03)

## Why
Valid desktop annotations can omit turn_id. Rejecting those annotations causes full history to be trimmed against an obsolete response anchor.

## What Changes
Accept recognized optional annotations in classification-only same-owner proofs and preserve existing owner-pinning safeguards.

## Impact
Replay classification only; no input rewriting, database migration, or rollout edits. Depends on P01.
