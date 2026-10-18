# Preserve desktop conversation replay across reconnects

## Why
Desktop history annotations can omit turn_id while retaining content_item_kinds. Rejecting these annotations prevents a complete same-owner resend and injects an obsolete response anchor. The deployed local fixes also need a reproducible upstream-based fork.

## What Changes
- Carry desktop annotation and same-owner routing safeguards onto latest main.
- Accept optional turn_id in recognized desktop annotations for same-owner proof only.
- Provide an explicit, empty-by-default web-action ID compatibility list to preserve a verified incompatible completed record as lossless assistant text on the wire.

## Impact
Responses bridge replay classification and opt-in input normalization. No database migration or saved conversation edits.
