# Explicit web-history compatibility (P04)

## Why
A verified historical native web action fails upstream replay before response.created. Its content must remain available without editing saved history.

## What Changes
Provide an explicit, empty-by-default ID allowlist that renders listed completed web actions as assistant text containing the entire original JSON record.

## Impact
Opt-in Responses input normalization. No authentication, account policy, or database changes.
