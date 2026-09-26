# Expected versus actual validation

Classify each test from UI observations, not from completed clicks or presumed backend state.

| Status | Meaning |
| --- | --- |
| `PASS` | Observable UI behavior satisfies the stated expected result. |
| `FAIL` | Observable UI behavior contradicts it, including a required element absent after a reasonable wait. |
| `BLOCKED` | An external prerequisite prevents the test, such as unreachable target, missing file, unavailable authentication or browser permission. |
| `INCONCLUSIVE` | Execution occurred but the UI evidence cannot establish whether the expectation was satisfied. |

Record the expected result and the actual observed text, state, or navigation separately. A file chooser accepting a file is not proof of upload success. A submit click is not proof of account creation. A screenshot alone does not establish pixel-perfect correctness without an explicit comparison capability and baseline.

For dynamic UI, wait for a meaningful condition such as a heading, row, toast, enabled control, or navigation. Capture a validation failure or unexpected error as evidence when safe. Distinguish a tool/environment failure from an application failure. If a consequence cannot be observed through the UI, use `INCONCLUSIVE` rather than inferring backend success.

Step summaries are optional for short cases but should identify the point of failure or blockage. Do not fabricate any action, message, output, URL, or evidence path.
