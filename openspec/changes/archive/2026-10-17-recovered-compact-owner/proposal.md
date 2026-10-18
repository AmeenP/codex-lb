# Compaction after verified bridge recovery

A successful quota handoff publishes a synthetic turn-state alias to a recovery bridge while an older raw sticky mapping can remain attached to its former account. Normal turns follow the alias, but compaction resolves the new owner then rejects the old sticky mapping as a competing owner.

For a synthetic turn-state only, resolve its scoped durable alias again after checking all required owners. If it points to the same required owner in the reserved recovery namespace and has a completed response anchor, omit the superseded sticky hint for this selection. Keep the required owner, payload, file checks, and fallback prohibition intact. Do not mutate historical sticky rows, aliases, or conversation files. Missing or incomplete recovery proof retains existing fail-closed behavior.
