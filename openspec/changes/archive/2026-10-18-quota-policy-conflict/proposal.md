# Recover quota-related continuity policy conflicts

An exhausted continuity owner can disappear from the eligible model catalog. HTTP bridge admission then returns 503 continuity_owner_policy_conflict, bypassing the existing 502 quota recovery. Extend only the opt-in, verified retained-context recovery to this error. Do not infer quota exhaustion from policy rejection alone or alter historical ownership records.
