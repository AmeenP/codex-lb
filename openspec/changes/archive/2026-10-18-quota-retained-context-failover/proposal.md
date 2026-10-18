# Quota failover with retained context (P06)

A desktop full resend can prove complete history yet remain pinned to an
exhausted account because it contains encrypted compaction or agent messages.
An isolated upstream probe accepted the intact retained context on another
account. Add explicit opt-in replay of that context on confirmed quota loss.

The default account-neutral contract remains unchanged. File pins, incomplete
history, unknown context shapes, auth failures and operator pauses remain
fail-closed. Preserve the client transcript and all serialized input items.

This is an HTTP Responses bridge recovery path. Upstream acceptance is still
required; do not silently drop encrypted or visible context after a rejection.

The fork adds one T4 boolean (settings budget 97 -> 98). A zero-config default
would change encrypted-context ownership expectations for every installation.
The explicit setting records operator consent; the standard replay contract
remains strict. Enable it on the two user-authorized hosts only.
