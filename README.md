<p align="center">
  <img src="./assets/logo.png" alt="Prompt UI Testing" width="180" />
</p>

<h1 align="center">Prompt UI Testing</h1>

<p align="center"><strong>From Prompt to Proof.</strong></p>

<p align="center">
  Prompt-driven black-box UI testing for AI Agents with browser automation,<br />
  Expected vs Actual validation, and screenshot evidence.
</p>

**Current release:** [`v0.1.3`](https://github.com/thg1rb/prompt-ui-testing/releases/tag/v0.1.3). See the [changelog](CHANGELOG.md), [v0.1.2 release record](docs/releases/v0.1.2.md), and [v0.1.3 release record](docs/releases/v0.1.3.md). The earlier `v0.1.0` release was withdrawn and superseded by `v0.1.1` after Git metadata privacy remediation; see the [remediation record](docs/PRIVACY-REMEDIATION.md).

## Tired of Testing the Old Way?

Build a feature. Open the browser. Click through every step. Take screenshots one by one. Save the evidence. Write the test. Change the feature. And… do it all over again.

What if you could simply describe what you want to test and what you expect to happen? Prompt UI Testing lets you describe the goal in natural language while an Agent handles browser interaction, compares the observed UI with your expectations, and collects evidence. It helps with the repetitive workflow; it does not replace QA judgment or make every test automatic.

## Prompt-Driven UI Testing

**The test specification is the prompt.** Describe the target application, goal, test data, any necessary actions, expected result, and evidence checkpoints. The Agent turns that intent into a black-box UI test without requiring changes to the application under test.

## From Prompt to Proof

```text
Intent / Requirement
        ↓
Natural-language Test Specification
        ↓
AI Agent + prompt-ui-testing
        ↓
Google Chrome via Playwright MCP
        ↓
UI Interaction
        ↓
Expected vs Actual
        ↓
Screenshot + URL Evidence
        ↓
PASS / FAIL / BLOCKED / INCONCLUSIVE
```

The application remains a black box: the Agent observes and interacts through the browser, checks the expected result against what actually appeared, then reports the result with URL-visible screenshot evidence. Remote sites and apps at `localhost` or `127.0.0.1` are supported. Common workflows include forms, file-input uploads, redirects, and single-page app navigation.

The [Skill entrypoint](skills/prompt-ui-testing/SKILL.md) stays concise; detailed policy lives in its `references/` directory. The [evidence helper](skills/prompt-ui-testing/scripts/compose_evidence.py) adds a redacted, browser-observed URL above the screenshot and retains the raw image. Its only Python dependency is Pillow; install it from [requirements.txt](requirements.txt) in the Agent's execution environment.

For information about the skills-only Plugin package, see [privacy details](PRIVACY.md), [security guidance](SECURITY.md), and the [submission preparation record](docs/PLUGIN-SUBMISSION.md). Browser automation is provided separately by the host.

## Quick Start

1. [Install the Skill](#install-the-skill) in your project or user Skill folder.
2. [Configure Playwright MCP](#connect-a-browser) and the documented Google Chrome setup.
3. Ask the Agent to test a flow and state what should happen. For example, use the [short prompt below](#short-example).

The default setup prefers headed, isolated Google Chrome with Fullscreen and a maximized fallback. Playwright MCP performs normal browser automation; Computer Use is not required. Fullscreen behavior is runtime-validated on macOS only.

## Copy-Paste Prompt Template

You normally do not need to provide CSS selectors, XPath, or Playwright locator syntax. The Agent works from the observable UI and chooses appropriate interactions. If a control is ambiguous or unavailable, it may ask for clarification or report the limitation.

Copy this template and fill in the parts relevant to your test; you can omit sections you do not need:

```markdown
Use $prompt-ui-testing to test:

<TARGET_URL>

## Goal

<Describe what you want to verify>

## Preconditions

- <Optional prerequisite>
- <Authentication requirement, if needed>

## Test Data

- <Field> = <Value>
- <Field> = <Value>

## Steps

1. <Action>
2. <Action>
3. <Action>

## Expected Result

- <Expected behavior>
- <Expected visible result>
- <Expected navigation or state>

## Files

- <Optional file path>

## Evidence

Capture screenshots at:

1. <Checkpoint>
2. <Checkpoint>
3. <Final result>

## Report

Compare Expected vs Actual.

Return one of:

- PASS
- FAIL
- BLOCKED
- INCONCLUSIVE

Include the observed result and relevant screenshot evidence.
```

### Short Example

You do not need to fill every template section for a simple test:

```text
Use $prompt-ui-testing to test:

http://localhost:3000/example

Goal:
Verify that a user can submit the form successfully.

Input:
Name = Sample User
Email = sample@example.com

Expected:
- The form submits successfully.
- A confirmation message appears.

Evidence:
- Before submission
- Final result

Report:
Compare Expected vs Actual and return
PASS, FAIL, BLOCKED, or INCONCLUSIVE.
```

## Install the Skill

Codex discovers project skills under `.agents/skills` from the working directory up to the repository root. User skills belong under `~/.agents/skills` and are available across projects. Copy the whole Skill folder, including its references, assets, and script:

```sh
# From this repository, for one target project:
mkdir -p /path/to/project/.agents/skills
cp -R skills/prompt-ui-testing /path/to/project/.agents/skills/

# Or, for the current user across projects:
mkdir -p ~/.agents/skills
cp -R skills/prompt-ui-testing ~/.agents/skills/
```

The Skill's files must be visible to the agent and the screenshot helper must be runnable in its execution environment. Install Pillow in that environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

On Windows PowerShell, create and install into the equivalent environment with:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The Skill prefers the target project's `.venv` interpreter when it can import Pillow. When installing into a project or user folder that does not contain this repository's `requirements.txt`, create a project environment and install Pillow directly:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install 'Pillow>=10,<13'
```

On Windows PowerShell, use `py -3 -m venv .venv` followed by `.venv\Scripts\python.exe -m pip install 'Pillow>=10,<13'`.

Codex detects newly installed skills automatically; start a new session if the Skill does not appear. See the [current Codex Skill documentation](https://learn.chatgpt.com/docs/build-skills) for supported locations and host behavior.

## Connect a browser

Playwright MCP is a separate dependency; installing this Skill does not install or configure it. It requires Node.js 20 or newer. For Codex CLI, add the server using the current [Codex MCP command format](https://learn.chatgpt.com/docs/extend/mcp) and [Playwright MCP package](https://playwright.dev/mcp/installation):

```sh
codex mcp add playwright -- npx --yes @playwright/mcp@0.0.82 --browser=chrome --isolated --config /absolute/path/to/playwright-mcp-config.json
codex mcp list
```

This selects Google Chrome and an in-memory isolated profile; headed mode is Playwright MCP's default. Each independent test uses a fresh browser session, while all steps within one case remain in that session. Configure Fullscreen by default and allow the page viewport to follow the window. The MCP `initPage` hook below also requests maximized mode if Fullscreen cannot be established. Do not add `--incognito` or describe Chrome's native Incognito UI as active: isolated Playwright state is the default privacy behavior. Headless mode is optional when explicitly requested.

The following config was verified with Playwright MCP `0.0.82` and Google Chrome on macOS. Replace the helper path with the absolute path to the installed Skill's `scripts/chrome-window-mode.cjs` file:

```json
{
  "browser": {
    "browserName": "chromium",
    "isolated": true,
    "launchOptions": {
      "channel": "chrome",
      "headless": false,
      "args": ["--start-fullscreen"]
    },
    "contextOptions": {
      "viewport": null
    },
    "initPage": ["/absolute/path/to/prompt-ui-testing/scripts/chrome-window-mode.cjs"]
  }
}
```

Save the JSON as a local file outside a public repository at the absolute path used in the command above. If a `playwright` server is already configured, update its command arguments to use this config rather than leaving the previous setup in place. The `--start-fullscreen` argument alone did not set Chrome's native Fullscreen window state on the tested macOS host; the `initPage` helper uses Chromium's DevTools Protocol to set and verify the state, then tries maximized mode as fallback. `viewport: null` disables fixed viewport emulation so the web page follows the actual Fullscreen content area. Fullscreen behavior outside macOS is not yet runtime-validated. See the [browser strategy](skills/prompt-ui-testing/references/browser-strategy.md) for fallback and reporting behavior.

Playwright's install guide says the browser downloads automatically on first use. If Google Chrome is unavailable, report that limitation and use another browser only if the user allows it or the documented fallback applies. Do not silently change browser identity when it matters to the test. Start a fresh Codex process after adding the server; an already-running session may retain its previous tool list. In the ChatGPT desktop app, MCP configuration is shared with Codex CLI; add the server under **Settings → MCP servers** and select **Restart**. The host may request approval before browser tool calls. Do not globally approve an MCP server unless you trust it. In non-interactive runs that cannot answer approval prompts, configure the server's `default_tools_approval_mode` for that run; this validation used `approve` only for its disposable Playwright session because its CLI approval policy was `never`. See the [Codex MCP settings](https://learn.chatgpt.com/docs/extend/mcp#configure-with-configtoml) for supported approval values.

The browser capability must support navigation, semantic inspection, requested controls, active URL retrieval, and screenshots. If Playwright MCP is absent, unavailable, or denied, the Skill must report `BLOCKED` (or another accurate execution limitation) without claiming browser execution or evidence. Do not automatically switch to Computer Use. Consider it only when Playwright MCP genuinely cannot perform a required interaction, the alternate path can preserve the requested session and evidence requirements, and the host provides it. If a requested control or URL-visible evidence cannot be produced, explain the limitation.

For a local app, run its server before testing. A remote or containerized browser may not share your machine's `localhost`; use a browser on the same machine or an explicitly provided reachable endpoint. A browser-to-localhost network limitation is `BLOCKED`, not an application failure.

## Compatibility

| Environment | Status |
| --- | --- |
| Codex CLI on macOS | Runtime validated, including project, user, and Plugin installation with Playwright MCP. |
| Codex CLI on Windows or Linux | Intended to work with the documented Skill paths and platform-specific Python environment; not runtime validated. |
| ChatGPT desktop Plugin runtime | Supported by the documented Plugin/MCP model; not runtime validated for this Skill. |
| Other Agent Skill hosts | The Skill follows the `SKILL.md` folder format, but host discovery, tool permissions, and helper execution are not validated here. |

Playwright MCP and Pillow are separate prerequisites. Install/configure them in the environment that runs the agent. Codex CLI and the desktop app share Codex MCP configuration. After changing MCP configuration, start a fresh CLI process or use the desktop app's **Restart** action. A host can request approval for browser tools; availability does not mean calls are pre-approved. The browser is downloaded on first use in a clean Playwright setup, but a missing selected browser may require Playwright's browser install command. See the sections above for setup details. If the compatible browser tool is missing, denied, or cannot reach the target, the Skill must report the execution limitation without claiming that it ran a test.

## Use it

Invoke `$prompt-ui-testing` explicitly or let the agent select it for a matching request. The public examples in [examples/](examples/) cover basic, local, form, upload, validation, and configuration flows. Example hosts and data are illustrative; supply a real target and authorized test account at run time.

```text
Use $prompt-ui-testing to test the Create Account flow at http://localhost:3000.
Enter Name = Sample User and Email = sample@example.com.
Expected: a success message appears and the account page opens.
Capture evidence before submission and after the result.
```

For planning without browser execution, say “plan-only” or “dry-run.” For exploratory tests, ask the agent to explore; its generated cases will be labeled separately. Optional project settings may be adapted from [project-config.example.yaml](skills/prompt-ui-testing/assets/project-config.example.yaml) and kept outside the public Skill. The example is guidance, not a required parser or config file.

## Evidence

Every final evidence image must visibly show the **actual active URL**. A regular Playwright MCP page screenshot does not include the browser address bar, so the workflow saves a raw screenshot, obtains the URL before and after capture, and uses the helper to add a readable strip. If the URL changes during capture, the checkpoint is retried after the page settles. The helper removes URL userinfo, query values, fragments, and likely token-bearing path segments from the visible strip.

Example helper invocation after a browser has saved `TEST-001/01-page-loaded.raw.png` and supplied its actual URL:

```sh
printf '%s' '{"url":"http://localhost:3000/create-account"}' | \
  .venv/bin/python skills/prompt-ui-testing/scripts/compose_evidence.py \
  --input TEST-001/01-page-loaded.raw.png \
  --output TEST-001/01-page-loaded.png
```

The URL in that command is only an illustration. During a test, use the URL returned by the active browser page, including redirects or SPA navigation. Do not pass sensitive URLs on a shell command line; feed the JSON through stdin from a safe environment. The helper does not remove secrets already visible inside the application screenshot, so avoid capturing secret entry or confidential page content.

Use a separate evidence workspace for each independent test run, with unique test/checkpoint filenames. Do not reuse earlier screenshots or output folders; concurrent browser runs also need separate browser sessions and output paths. The Skill reports only evidence that the current run actually created.

## Distribution

The root [plugin.json](plugin.json) makes this repository a portable skills-only plugin package under the [current plugin structure](https://developers.openai.com/plugins/build/plugins). The package deliberately does not bundle a browser server: hosts differ in how they launch browsers and reach local applications. Configure Playwright MCP or another compatible browser capability in the host separately.

For local plugin testing in Codex CLI, this repository provides a [repo marketplace](.agents/plugins/marketplace.json). Add the marketplace root, then install its plugin:

```sh
codex plugin marketplace add /absolute/path/to/prompt-ui-tester
codex plugin add prompt-ui-testing@prompt-ui-tester-local
```

Start a fresh Codex session after installing the plugin. For local marketplace changes in the ChatGPT desktop app, restart the app before selecting the marketplace and installing the plugin. The Plugin packages the Skill; it does not bundle or configure Playwright MCP, so configure that dependency separately as described above. A public directory listing is a separate publication step and has not been performed. Project and user Skill installation above work without a plugin host.

## Safety and limitations

- The agent uses only UI observations for results. A click or upload-tool response alone does not prove success.
- Consequential actions on production-like or uncertain targets need explicit user intent. Authentication may need a secure or manual handoff.
- Browser capability, file access, and network topology vary by host. The Skill reports missing prerequisites as `BLOCKED`.
- Screenshot comparison is not pixel-perfect visual regression without a separate comparison capability and baseline.
- URL redaction protects the visible metadata strip, not secrets already shown on the page or in the retained raw screenshot.

### Known limitations

- **Control coverage:** Common text, password, select, checkbox, radio, date/time, file-input, dialog, and pagination interactions were exercised. Custom combobox/autocomplete, tab switching, number/textarea, and drag-and-drop upload variants were not individually validated; use semantic controls the browser exposes, otherwise report the limitation.
- **Authentication and recovery:** Disposable login and unavailable-SSO handling were validated. Real SSO/MFA handoff and authorized profile reuse were not; hot reload, minor UI drift recovery, and measured retry bounds were not directly tested. Stop at unavailable authentication and report `BLOCKED` rather than bypassing it.
- **Browser session and window modes:** Independent cases use fresh isolated state by default. Reusing explicitly supplied storage state is supported and must be disclosed; real authenticated profile reuse is not runtime validated. Native Chrome Incognito UI is not required. Fullscreen is preferred and maximized mode is the fallback. Chrome 154 headed, isolated, Fullscreen, and actual page-viewport behavior were runtime validated on macOS only; fallback is covered by a helper test but has not been exercised on a host where Fullscreen is unavailable. Headless runs do not use desktop Fullscreen. Multi-monitor selection is not controlled.
- **Dynamic UI and wording:** SPA navigation, redirects, delayed content, and modal behavior were exercised. Lazy loading, toast-specific behavior, and hot-reload recovery were not; ambiguous equivalent labels were not separately tested. Do not guess when meaning is unclear.
- **Platform coverage:** Only Codex CLI on macOS was runtime validated. Other platforms and ChatGPT desktop Plugin runtime remain untested; see [Compatibility](#compatibility).
- **Evidence privacy:** URL metadata is redacted, but secrets rendered inside the page remain visible in both raw and final screenshots. Review captures before sharing them.

The unverified variants are tracked in the [requirement traceability matrix](docs/REQUIREMENT-TRACEABILITY.md); they are limitations, not claims of runtime support.

## Documentation and Contributing

- [Validation record](docs/VALIDATION.md)
- [Requirement traceability matrix](docs/REQUIREMENT-TRACEABILITY.md)
- [Security guidance](SECURITY.md)
- [Contribution workflow](CONTRIBUTING.md)

Contributions follow the documented task-branch → PR → review → `develop` workflow. Use public-safe examples and never add private targets, credentials, or screenshots.

## License

This project is available under the [MIT License](LICENSE).
