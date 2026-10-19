# P09 implementation and validation

OAuth can restore an account while the last authoritative catalog still excludes its models. The prior implementation waits up to 300 seconds for periodic discovery. Publish a dedicated `model_refresh` invalidation namespace after committed credentials, distinct from `model_registry` snapshot publication, so recovery reaches the scheduler leader without creating a feedback loop.

The normal 0.5-second invalidation poll wakes the existing scheduler. Its event coalesces bursts, is cleared before fetching, and preserves signals arriving during a fetch for a subsequent pass. The existing leader gate, bounded upstream clients, persistence, selection-cache invalidation, and cancellation ownership remain in control. No new settings, migrations, or detached tasks are introduced.

A successful callback means credentials were stored, not that discovery has finished. Slow or failed discovery can still delay availability. Failed signal writes use the bus's existing pending retry; periodic discovery remains the backstop. Mixed-version deployments with an older scheduler leader retain the periodic fallback until that leader is updated. Credential sync is covered by the import endpoint; routine automatic access-token refresh is outside this patch.

Regression coverage uses synthetic identities and stub upstream responses: previously known Astra disappears after a paid account requires reauthentication, producing `no_plan_support_for_model`; browser login or auth-file import commits new credentials on one replica; a peer observes the signal and discovers Astra; the same load balancer then selects the recovered account. Discovery failure preserves successful credential storage. Scheduler tests cover idle wake-up, coalescing during a fetch, and awaited cancellation cleanup.

No runtime was deployed or restarted. Conversation records, account pause/routing policies, and decision ledgers are untouched.
