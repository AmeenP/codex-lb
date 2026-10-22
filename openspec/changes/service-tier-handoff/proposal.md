# Preserve context when the requested service tier excludes the current owner

Changing an existing Astra conversation from Fast to Ultrafast can exclude its Pro owner. The HTTP bridge currently permits intact retained-context recovery only for persisted quota exhaustion. A healthy owner excluded solely by the requested tier therefore returns 503 even when the request has a verified complete history.

Extend the existing opt-in retained-context recovery to a scoped, authoritative tier mismatch on the same model. Require a healthy current owner, model eligibility without the tier, exclusion with the explicitly requested tier, and at least one tier-capable account in scope. Reuse the sealed full-resend proof, resource checks, original input, owner exclusion, recovery fencing and alias publication. Never downgrade the requested tier or weaken missing-history checks.

An active local bridge previously emitted a generic 502 before account selection for an anchored tier mismatch. Use the existing pre-submission failure marker to permit the same tier-only proof after that 502, so both live and durable-only sessions reach the guarded recovery path. Other 502 errors and model-change behavior remain unchanged.
