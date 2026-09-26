# Plugin submission preparation

**Status:** Prepared for publisher review; not submitted. Public publication is not authorized by this preparation record.

## Architecture

The public package is skills-only. It contains the portable root `plugin.json` and the `skills/prompt-ui-testing/` Skill. It does not contain `mcp.json`, `.mcp.json`, `.app.json`, or a browser server. OpenAI supports skills-only Plugins and describes Skills as workflows that can use tools already available to the host. This Skill prefers Playwright MCP when available, accepts another compatible browser capability, and must report `BLOCKED` when it cannot execute or capture evidence. Playwright MCP remains a separate, user-configured prerequisite; no public remote MCP service is required by this package architecture.

The package is useful for planning without a browser, but execution requires host browser tooling. Submission prompts and user-facing copy must keep this limitation visible. See the official [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins), [Skills](https://developers.openai.com/plugins/concepts/skills), [submission guide](https://developers.openai.com/plugins/deploy/submission), and [package format](https://developers.openai.com/plugins/build/plugins).

For a skills-only upload, build the archive from the repository root after the final reviewed commit is on `main`:

```sh
zip -r -X /tmp/prompt-ui-testing-0.1.1.zip plugin.json assets skills/prompt-ui-testing \
  -x '*/__pycache__/*' '*.pyc' '*/.DS_Store'
```

The archive root must contain `plugin.json`, `assets/`, and `skills/`; do not include repository docs, local marketplace configuration, tests, caches, or `.git`. An initial packaging check found that `zip` includes ignored bytecode caches unless excluded. The command now excludes those files; the rebuilt archive is checked for cache entries. Install/configure Playwright MCP separately when using that browser capability. It requires Node.js 20+, a supported Playwright browser installation, and host tool approval; after configuration, start a fresh agent process. If no compatible browser capability is available, the Skill reports `BLOCKED` without claiming execution.

## Listing material

| Field | Prepared value |
| --- | --- |
| Plugin name | `prompt-ui-testing` |
| Display name | Prompt UI Testing |
| Short description | Black-box web UI testing |
| Long description | Guide an agent through authorized, black-box web UI testing. Plan and run browser checks against remote or localhost applications, compare expected and observed results, and report PASS, FAIL, BLOCKED, or INCONCLUSIVE with URL-visible screenshot evidence. A compatible browser capability must be available in the host. Playwright MCP is a separately configured option and is not bundled; without a usable browser, the Skill reports BLOCKED. |
| Category | Developer Tools |
| Website | <https://github.com/thg1rb/prompt-ui-testing> |
| Support | <https://github.com/thg1rb/prompt-ui-testing/issues> |
| Privacy policy | <https://github.com/thg1rb/prompt-ui-testing/blob/main/PRIVACY.md> (available after the policy is merged to `main`) |
| Terms | Omit; optional for a skills-only ZIP under current submission error guidance. Do not substitute the software license for product terms. |
| Logo / composer icon | `assets/prompt-ui-testing-logo.svg`, `assets/prompt-ui-testing-icon.svg` |
| Root `author.name` / listing `developerName` | Not set in the repository because the verified publisher name is account data and must not be guessed. Current OpenAI submission guidance says the portal can populate both from the selected verified identity after confirmation. Select the intended identity and confirm the normalized manifest before submission. |
| Availability | Publisher selects countries/regions after confirming support and legal readiness. |
| Release notes | Initial skills-only listing of the released `v0.1.1` Skill. Browser tooling is external and is not included. |

The current [submission error reference](https://developers.openai.com/plugins/deploy/submission-errors) limits final display name and short description to 30 characters, permits up to three starter prompts, lists supported categories, and requires square logo and composer icon assets for directory submissions. It requires both `author.name` and `interface.developerName`; when these are absent or differ, the portal can default both to the selected verified identity after confirmation. This repository intentionally leaves those account-specific values unset. Therefore, the package is prepared, but submission is blocked until the publisher selects the verified identity and confirms the portal-normalized manifest. The publisher also selects availability in the portal.

Runtime validation currently covers Codex CLI on macOS, including local Plugin installation. ChatGPT desktop Plugin runtime and other operating systems have not been runtime-validated; describe these as untested rather than validated. OpenAI's public Plugin directory is shared across supported surfaces, but surface availability may differ; verify the portal's current availability choices and reviewer requirements before submission.

## Starter prompts

1. `Test https://example.com and verify that the page heading is Example Domain.`
2. `At http://localhost:4173, test the sample form and select sample-upload.txt.`
3. `Plan a test for http://localhost:4173; do not open the page or execute any steps.`

## Submission test cases

The portal currently requests five positive and three negative cases. Each case below is written for a reviewer without private credentials or internal context. The local fixture is static and disposable; start it from the repository root with `python3 -m http.server 4173 --bind 127.0.0.1 --directory examples/plugin-fixture`, then open `http://127.0.0.1:4173`. Binding to loopback keeps the fixture local to the machine. Its file chooser only demonstrates local selection and a client-side confirmation; it does not upload the file to a server.

For execution cases, the reviewer also needs a compatible browser capability. The README's [browser setup instructions](../README.md#connect-a-browser) give the Playwright MCP setup, Node.js prerequisite, browser install guidance, host approval behavior, and fresh-session requirement. Planning and negative missing-browser cases do not require Playwright MCP.

### Positive cases

| ID | Prompt and prerequisites | Expected Skill / tool behavior and result | Evidence expectation |
| --- | --- | --- | --- |
| POS-1 | “Test `https://example.com/`. Expected: the page heading is `Example Domain`.” Requires a compatible browser capability and network access. | Activate the Skill, navigate, inspect the rendered heading, compare it with the expected value, and report `PASS` if it matches. | A screenshot of the observed page with its current browser-observed URL visible. |
| POS-2 | “At `http://localhost:4173`, enter Name `Sample User`, Email `sample@example.com`, select `Basic`, submit, and verify the confirmation.” Requires the local fixture and compatible browser capability. | Fill the form semantically and verify `Form accepted for Sample User.`; report `PASS` when observed. | Screenshot showing the confirmation and current URL. |
| POS-3 | “At `http://localhost:4173`, submit the sample form with required values missing. Expected: the inline validation message appears.” Requires the local fixture and compatible browser capability. | Submit the empty form, compare the observed inline message with the expectation, and report `PASS` when the expected validation is shown. | Screenshot showing the validation message and current URL. |
| POS-4 | “At `http://localhost:4173`, select `examples/plugin-fixture/sample-upload.txt` and confirm the selected filename.” Requires the local fixture, the included text file, and a compatible browser capability. | Use the file chooser, then verify `Selected file: sample-upload.txt`; explain that this fixture confirms local file selection only. | Screenshot showing the filename confirmation and current URL; do not claim a server upload. |
| POS-5 | “Plan how to test the sample form at `http://localhost:4173`, but do not open it or perform any actions.” No browser capability is needed. | Activate the Skill in plan-only mode and return target, planned steps, expected results, prerequisites, and safety considerations without browser calls. This is a plan result, not an executed test classification. | No screenshot is expected; explicitly state that execution and evidence capture did not occur. |

### Negative cases

| ID | Prompt and prerequisites | Expected safe behavior | Evidence expectation |
| --- | --- | --- | --- |
| NEG-1 | “Write unit tests for this Python function.” No browser prerequisite. | Do not activate the UI-testing Skill; handle as a unit-testing task. | No browser calls or UI evidence. |
| NEG-2 | “Open `https://example.com/` and tell me what the site is about.” No UI test expectation is provided. | Do not activate the Skill for ordinary browsing; answer using the available browsing capability. | No Skill-generated test evidence. |
| NEG-3 | “Test `https://example.com/` and verify the heading,” while no compatible browser tool is available. | Activate the Skill, identify the missing execution prerequisite, return `BLOCKED` (or an equivalent explicit execution limitation), and make no claim that navigation or validation occurred. | No screenshot may be claimed or listed. |

## Safety, privacy, and test data

Users must be authorized to test targets. Browser reachability does not imply authorization. Tests can change application data; consequential or irreversible actions need explicit user intent and should use disposable environments. Browser tools and MCP providers have independent permissions and data handling. The Skill creates evidence files in the selected local workspace and cannot remove sensitive content already rendered in screenshot pixels. See [Privacy](../PRIVACY.md) and [Security](../SECURITY.md).

## Publisher portal checklist

- Confirm the verified developer identity is the intended public publisher and the account has Apps Management write access.
- Upload the skills-only package and verify the portal's safety/security scan passes.
- Review listing text, the privacy URL after it is live on `main`, the supplied logo and icon, and all eight test cases.
- Select only regions where the publisher, product, support process, and legal terms are ready.
- Complete policy attestations only after reviewing their accuracy, then submit for review.
- Record portal status without storing account details. Approval is not publication; publishing requires a separate explicit decision.

This preparation references the current official [submission flow](https://developers.openai.com/plugins/deploy/submission), [submission errors](https://developers.openai.com/plugins/deploy/submission-errors), [Plugin guidelines](https://developers.openai.com/plugins/app-guidelines), and [security and privacy guidance](https://developers.openai.com/plugins/guides/security-privacy). Verify them again immediately before submission because portal requirements can change.

## Preparation validation record

| Check | Expected | Actual | Result |
| --- | --- | --- | --- |
| Current package schema | Root manifest conforms to Agent Plugins 1.0.0. | Validated against the live official JSON Schema. | PASS |
| Package metadata/assets | Version and listing limits are valid; referenced assets exist and are square SVGs. | Version `0.1.1`; three prompts are within length limits; both referenced SVG assets exist and are square. Verified publisher identity fields are intentionally unset pending portal normalization and confirmation. | PASS WITH EXTERNAL SUBMISSION GATE |
| Skills-only archive | Root manifest, assets, and complete Skill are present; development files and caches are absent. | Rebuilt ZIP contains 19 package entries and no docs, tests, local marketplace, Git data, bytecode, or cache paths. | PASS |
| Clean Codex Plugin install | Package is installable and enables the Plugin without relying on the development repository. | Codex CLI `0.156.1` installed the clean staged package into a disposable `CODEX_HOME`; the Plugin appears enabled at version `0.1.1`, and the installed Skill references and assets are present. | PASS |
| Skill activation/runtime | Submission prompts activate correctly and unrelated prompts do not. | The prior Codex CLI Plugin end-to-end activation and non-activation results are recorded in [VALIDATION.md](VALIDATION.md). The Skill itself is unchanged in this preparation. | REUSED EVIDENCE |
| Browser smoke in this session | Run a browser test and verify URL-visible evidence when a compatible browser is available. | Playwright MCP is not configured. No browser smoke or screenshot was claimed. | BLOCKED BY MISSING BROWSER TOOL |
| Privacy URL | Public policy is reachable at the manifest URL. | The URL targets `main` and becomes available only after this branch is promoted. | PENDING PROMOTION |
| OpenAI portal | Draft status and portal warnings are recorded. | No portal draft was created and nothing was submitted. Publisher must select a verified identity, confirm the normalized author/listing fields, choose availability regions, and review the final listing before submission. | NOT SUBMITTED |

An initial archive contained ignored Python bytecode because the original `zip` command did not exclude caches. The command was corrected and the archive was rebuilt and inspected; the retest passed. The local fixture is provided for reviewer use, but was not browser-executed in this session because no compatible browser automation tool was available.
