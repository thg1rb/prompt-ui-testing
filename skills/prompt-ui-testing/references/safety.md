# Safety and authorization

Access to a page does not establish authorization to change its data. Use the user's requested scope and known environment to decide actions.

- On explicitly identified localhost, development, test, staging, or sandbox targets, perform requested state changes subject to ordinary permission and privacy constraints.
- On production-like or uncertain targets, read-only inspection can proceed when appropriate. Before a consequential create, update, delete, submit, approve, reject, account modification, or financially meaningful action, require explicit user intent that covers the action and target. For destructive or irreversible changes, seek specific authorization immediately before the action if it has not already been given.
- Never infer authorization merely because a control is enabled or an authenticated session exists.

Prefer test data and the smallest action needed to verify the expectation. Do not expose passwords, tokens, authentication codes, personal identifiers, or confidential content in reports or screenshots. The public Skill must not store secrets. Respect host and tool approval boundaries.

For unexpected errors, inspect the current UI and retry only recoverable transient conditions within reasonable bounds. If recovery would broaden the user's requested actions, stop that branch and ask. Keep any `BLOCKED` or `INCONCLUSIVE` result honest and specific.
