# Test workflow and modes

## Convert a prompt into a test

Identify the target URL or configured base URL, requested flow, inputs, expected observable result, explicit steps, requested evidence, and prerequisites. If the prompt omits an expected result, use only a directly observable outcome implied by the request; otherwise ask for the missing criterion or mark the result `INCONCLUSIVE`. Do not silently add a business rule.

Prepare a short internal plan before executing. Preserve explicit user steps and order. For each test, record intended action, expected observation, and the observation that would decide its result. Keep multiple tests separate, identify dependencies, and isolate evidence and browser state where the available tool permits.

## Modes

- **Plan-only:** describe proposed steps and validation without opening the target or changing its state.
- **Dry-run:** additionally identify target, inputs, files, authentication needs, browser availability, and consequential actions; do not execute the test. Include a `Browser capability` field with the currently visible compatible tool name, `unavailable`, or `not verified`. Determine availability from the host's current tool/configuration context without navigating to the target.
- **Execution:** use the browser, collect observations and evidence, and report results.
- **Exploratory:** create a small, clearly labeled set of agent-generated cases based on visible UI and obvious validation edges. Do not attribute them to formal requirements.

If a requested file does not exist, report `BLOCKED` for the dependent test. Never create a substitute file without the user's instruction. If instructions conflict or multiple consequential targets are equally plausible, ask before that action and continue independent read-only inspection where useful.

Use generic IDs such as `TEST-001`, `TEST-002`; otherwise derive a neutral slug from the test name. Use a separate evidence directory per test.
