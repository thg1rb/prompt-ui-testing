---
name: prompt-ui-testing
description: Test a web application's UI from a natural-language request using a browser, including localhost flows, form validation, uploads, and screenshot evidence. Use for browser-based functional testing; do not use for unit or API-only tests, source review, ordinary browsing, or requests to write test specifications.
---

# Prompt-driven UI testing

Treat the target as a black-box web application. Do not require changes to its source, selectors from the user, or Playwright test files. Follow the user's language where practical.

1. Interpret the request into target, test cases, inputs, steps, expected observable UI results, evidence requests, prerequisites, and consequential actions. Preserve explicit steps. For plan-only or dry-run requests, produce the plan and prerequisite/safety review without opening the application or executing actions. See [testing policy](references/testing-policy.md).
2. Before execution, check authorization and environment risk under [safety](references/safety.md). Check browser capability and target reachability under [browser strategy](references/browser-strategy.md) and [localhost guidance](references/localhost.md). Treat missing prerequisites as `BLOCKED`.
3. Prefer Playwright MCP when available. Inspect the current UI, interact semantically, and re-evaluate after state changes. Use another browser capability only when it can execute the test and meet the evidence requirement. Never claim execution without a compatible tool.
4. Use [authentication guidance](references/authentication.md) for login, sessions, SSO, and MFA. Use actual available files for uploads; never invent files.
5. Compare each expected outcome with observed UI behavior using [validation policy](references/validation-policy.md). Completing steps alone is not a pass. Report `PASS`, `FAIL`, `BLOCKED`, or `INCONCLUSIVE` for each test independently.
6. Capture meaningful checkpoints under [evidence policy](references/evidence-policy.md). **Every final evidence screenshot must visibly show the actual current page URL.** If the browser screenshot lacks an address bar, use the deterministic URL-strip helper. Preserve the raw screenshot. If URL-visible evidence cannot be produced, explain the limitation and do not claim an evidence image exists.
7. Report against the [report template](assets/report-template.md), including expected versus actual, status, and only evidence files that exist. Label agent-generated exploratory cases separately from user-specified cases.

Keep the entrypoint short; read the linked reference only when that aspect of the current test is relevant. The browser capability performs interactions; this Skill supplies the workflow and policies.
