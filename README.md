# Prompt UI Testing

`prompt-ui-testing` is a reusable Agent Skill for prompt-driven, black-box testing of web applications. Give the agent a URL, actions, and an expected UI result. The Skill guides browser interaction, evidence capture, and an honest `PASS`, `FAIL`, `BLOCKED`, or `INCONCLUSIVE` report. It supports remote sites and applications running at `localhost` or `127.0.0.1`.

**Current release:** [`v0.1.1`](https://github.com/thg1rb/prompt-ui-testing/releases/tag/v0.1.1) supersedes withdrawn `v0.1.0`, which did not meet the repository's Git metadata privacy requirements. See the [changelog](CHANGELOG.md), [release record](docs/releases/v0.1.1.md), and [remediation record](docs/PRIVACY-REMEDIATION.md).

The target application needs no code changes, test files, selectors, or automation scripts. The Skill supplies policy and workflow; a separate browser capability performs the actions. [Playwright MCP](https://playwright.dev/mcp/installation) is preferred.

For the Plugin listing, see [privacy details](PRIVACY.md), [security guidance](SECURITY.md), and the [submission preparation record](docs/PLUGIN-SUBMISSION.md). The public package is skills-only; browser automation is provided separately by the host.

## How it works

```text
Natural-language request
  → test plan and safety review
  → semantic browser interaction
  → expected-versus-actual UI validation
  → raw screenshot + active URL → URL-visible evidence PNG
  → per-test result report
```

The [Skill entrypoint](skills/prompt-ui-testing/SKILL.md) stays concise. Its `references/` directory contains the detailed policies. The [evidence helper](skills/prompt-ui-testing/scripts/compose_evidence.py) adds a redacted active-page URL above the screenshot and retains the raw file. Its only Python dependency is Pillow; install it from [requirements.txt](requirements.txt) in the agent's execution environment. The browser remains responsible for reporting the actual URL at capture time.

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
codex mcp add playwright -- npx --yes @playwright/mcp@latest --headless
codex mcp list
```

Playwright's install guide says the browser downloads automatically on first use. If a server reports that the selected browser is missing, install that browser with the command in its error (for example, `npx --yes @playwright/mcp@latest install-browser firefox`); this was required for Firefox in validation. The default `chrome` channel used an existing Google Chrome installation on this machine. Start a fresh Codex process after adding the server; an already-running session may retain its previous tool list. In the ChatGPT desktop app, MCP configuration is shared with Codex CLI; add the server under **Settings → MCP servers** and select **Restart**. The host may request approval before browser tool calls. Do not globally approve an MCP server unless you trust it. In non-interactive runs that cannot answer approval prompts, configure the server's `default_tools_approval_mode` for that run; this validation used `approve` only for its disposable Playwright session because its CLI approval policy was `never`. See the [Codex MCP settings](https://learn.chatgpt.com/docs/extend/mcp#configure-with-configtoml) for supported approval values.

The browser capability must support navigation, semantic inspection, requested controls, active URL retrieval, and screenshots. If Playwright MCP is absent, unavailable, or denied, the Skill must report `BLOCKED` (or another accurate execution limitation) without claiming browser execution or evidence. If a requested control or URL-visible evidence cannot be produced, explain the limitation.

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
- **Dynamic UI and wording:** SPA navigation, redirects, delayed content, and modal behavior were exercised. Lazy loading, toast-specific behavior, and hot-reload recovery were not; ambiguous equivalent labels were not separately tested. Do not guess when meaning is unclear.
- **Platform coverage:** Only Codex CLI on macOS was runtime validated. Other platforms and ChatGPT desktop Plugin runtime remain untested; see [Compatibility](#compatibility).
- **Evidence privacy:** URL metadata is redacted, but secrets rendered inside the page remain visible in both raw and final screenshots. Review captures before sharing them.

The unverified variants are tracked in the [requirement traceability matrix](docs/REQUIREMENT-TRACEABILITY.md). They are limitations of the v0.1.0 validation scope, not claims of runtime support.

See [SECURITY.md](SECURITY.md) for handling sensitive targets and [CONTRIBUTING.md](CONTRIBUTING.md) for the task-branch → PR → review → develop workflow, validation guidance, and public-safe examples.
