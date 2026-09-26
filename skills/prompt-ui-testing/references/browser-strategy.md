# Browser interaction strategy

Prefer Playwright MCP's accessibility snapshot and element references for actions. Use screenshots for visual inspection and evidence, not as the primary action map. When using another browser capability, follow the same semantic approach where supported.

Find targets in this order: accessible role plus name, associated label, visible text, placeholder, stable DOM attribute, visual understanding, then coordinates as a last resort. Use the current UI state, never a selector inferred from source code. A clearly equivalent label may be used when context is unambiguous; inspect further when more than one consequential action fits.

After navigation, submission, dialog changes, or other material state changes, refresh the UI snapshot. Prefer an observable ready condition over a fixed sleep. For a transient loading state, wait and retry within a small bounded number of attempts. If the element remains absent, capture the observed state and classify it under validation policy. Do not retry indefinitely.

Common controls include text and password fields, textareas, numbers, checkboxes, radio groups, selects, comboboxes, autocomplete, date/time controls, tabs, tables, pagination, dialogs, and file controls. Use each control's semantic interaction where available. For upload, locate the correct input or drop target, attach only existing user-specified files, and verify the UI acknowledgement and expected final state. Do not infer successful storage from a tool response alone.

Track redirects and SPA changes. Obtain the **active page URL** at evidence time from the browser, such as the active-tab listing or page-context evaluation where supported. Never reuse the requested navigation URL as evidence. See [evidence policy](evidence-policy.md) for capture consistency.

Browser tools and host permissions vary. If Playwright MCP is unavailable, inspect available browser/computer-use tools. Execute only if the alternative supports the requested control and a URL-visible evidence path. If no compatible tool exists, report `BLOCKED` or provide a plan, clearly stating that no UI execution occurred.
