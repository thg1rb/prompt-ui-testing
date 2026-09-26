# Validation record — 2026-09-26

## Environment and method

End-to-end runs used Codex CLI 0.156.1 in separate, disposable agent workspaces with Playwright MCP 0.0.82, Node.js 24.13.1, and headless Chrome. Each workspace contained a copy of the Skill; Playwright MCP was configured for that agent session only. The remote target was `https://example.com`. The local target was a disposable server at `127.0.0.1:43872` with generic form, error, and acknowledgment routes. No private application, account, credential, or organization data was used.

Session JSONL traces, prompts, final reports, and screenshots are under `/tmp/prompt-ui-e2e-validation-20260926/cases/`; the remote screenshot is under that temporary directory's `evidence/`. These artifacts are not committed to the public repository. A validation `PASS` below means the agent's **observed result matched the expected classification**; the agent's own result may be `FAIL`, `BLOCKED`, or `INCONCLUSIVE`.

## Agent scenarios executed

| Scenario | Environment and tool | Expected agent result | Actual observation and result | Validation |
| --- | --- | --- | --- | --- |
| Remote navigation and heading | `https://example.com`, Playwright MCP | `PASS`; “Example Domain” visible | Heading observed; URL-visible image `evidence/heading.png`; `PASS` | PASS |
| Local form, dropdown, upload, redirect, SPA | `/start` redirects to `/form`; Playwright MCP | `PASS`; success message after submitting generic data | Text entered, Editor selected, `sample.txt` attached, success shown; URL changed to `/result?token=synthetic-value`; `PASS` | PASS |
| Expected validation error | `/validation`; Playwright MCP | `PASS`; “Email is required” after empty submit | Exact message observed; `PASS` | PASS |
| Unexpected application error | `/failure`; Playwright MCP | `FAIL`; success expected | “Could not save profile” observed; `FAIL` | PASS |
| Missing required control | `/no-control`; Playwright MCP | `FAIL`; Save Settings button expected | Button absent after a five-second wait; `FAIL` | PASS |
| Missing upload file | `/form`; filesystem prerequisite check | `BLOCKED`; file unavailable | No upload or substitute attempted; `BLOCKED` | PASS |
| Unreachable localhost | `http://localhost:43999`; Playwright MCP | `BLOCKED`; connection unavailable | `net::ERR_CONNECTION_REFUSED`; reported connectivity blocker, `BLOCKED` | PASS |
| Outcome unavailable through UI | `/acknowledge`; Playwright MCP | `INCONCLUSIVE`; durable storage not observable | UI said “Request received”; agent did not infer persistence; `INCONCLUSIVE` | PASS |

For the local form run, the trace shows Skill activation and policy reads, browser navigation and snapshots, semantic text/select/upload actions, URL checks before and after each screenshot, and expected-versus-actual reporting. The initial navigation to `/start` ended at `/form`; the final screenshot shows `/result?token=[REDACTED]`. The remote run also activated the Skill, used Playwright MCP, and produced a screenshot showing `https://example.com/`.

## Activation boundaries and evidence audit

- All eight UI-testing sessions read `SKILL.md`. The unit-testing explanation did not read it or call Playwright MCP.
- An ordinary live-browsing request used Playwright MCP to inspect `https://example.com` but did **not** read `SKILL.md`. A shorter page-title browsing request also did not activate the Skill.
- Eight final evidence PNGs were visually inspected. Every image showed a readable URL strip. Browser trace URLs matched the strips, including the redirect to `/form` and the SPA change to `/result`. The synthetic query value was redacted.
- Each final PNG had a retained raw screenshot. A pixel comparison confirmed the application image area in every final PNG matched its raw image.
- No screenshot was claimed for the missing-file or unreachable-localhost blockers.

## Issues found and resolved during integration

| Issue | Observed behavior and root cause | Smallest fix and rerun |
| --- | --- | --- |
| Agent browser call denied | The first remote run activated the Skill but `browser_navigate` failed: “MCP tool call requires approval, but approval policy is never.” The session-only Playwright MCP tool policy was insufficient; `auto` still requested approval. | Set the disposable agent session's `mcp_servers.playwright.default_tools_approval_mode` to `approve`. The remote case reran to `PASS`, and subsequent Playwright calls completed. No Skill file changed. |
| Evidence paths could collide across sessions | Two initial sessions used the same temporary workspace and both generated `TEST-001` evidence paths. The shared harness directory caused the collision risk. | Give each scenario its own temporary workspace. Reran the validation-error case and local success baseline; both passed with isolated evidence. No Skill file changed. |

After those harness fixes, all eight evidence-helper unit tests passed and the bundled Skill validator accepted the Skill. Relative Markdown links resolved, and the manifest and marketplace JSON parsed. No integration failure required a Skill or helper change.

## Installation validation — 2026-09-26

### Environment and setup

- Codex CLI `0.156.1`; Node.js `v24.13.1`; Python `3.14.7`; `@playwright/mcp` `0.0.82`; macOS.
- Used disposable projects and a package-only snapshot under `/tmp/prompt-ui-install-validation-20260926/`. Docker was available as a command but its daemon was not running, so no container or separate OS user was used.
- Test targets used only `https://example.com` and its generic “Example Domain” page. No credentials or application data were used.
- Project and user tests installed `Pillow>=10,<13` in each disposable project's `.venv`; the Skill used that interpreter to compose evidence.
- Playwright MCP was configured separately with `codex mcp add playwright -- npx --yes @playwright/mcp@latest --headless`. The Plugin package contains no MCP server, as documented.
- Documentation checked against the current official [Codex Skill installation guide](https://learn.chatgpt.com/docs/build-skills), [Plugin packaging specification](https://developers.openai.com/plugins/build/plugins), [Codex MCP setup guide](https://learn.chatgpt.com/docs/extend/mcp), and [Playwright MCP installation](https://playwright.dev/mcp/installation) and [configuration options](https://playwright.dev/mcp/configuration/options) before running installs.

### Project installation

- **Installation Mode:** Project
- **Environment:** Fresh temporary Git project, no existing Skill, Codex CLI `0.156.1`.
- **Method:** Followed the README copy procedure to install `skills/prompt-ui-testing` at `.agents/skills/prompt-ui-testing`; created a project `.venv` and installed Pillow. Started a fresh Codex session with Playwright MCP configured.
- **Expected:** Project Skill discovery and implicit activation; unrelated unit-testing requests remain outside scope; Playwright verifies the UI and creates URL-visible evidence.
- **Actual:** The fresh session read the project Skill, used Playwright MCP, observed the `Example Domain` heading at `https://example.com/`, and created a screenshot showing that active URL. A separate `unittest.mock` prompt did not load the Skill. The evidence is in `project/evidence/project-install-retest2/TEST-001/`.
- **Result:** PASS after the fix below.
- **Issues:** The first run produced only a raw screenshot because the agent invoked system `python`/`python3`, which did not have Pillow, even though Pillow was installed in the project's `.venv`. That run was `INCONCLUSIVE`; a first retest still used the pre-fix Skill copy and had the same result.
- **Fixes:** Updated evidence instructions to select the project `.venv` interpreter when it can import Pillow and clarified the setup in README.
- **Retest:** Refreshed the disposable Skill copy and reran in a new evidence directory. The agent used `.venv/bin/python3`, composed the screenshot, and reported PASS. The final PNG was visually checked.

### User / Global installation

- **Installation Mode:** User / Global
- **Environment:** Separate unrelated temporary project with no project Skill; user-scope copy was installed at `~/.agents/skills/prompt-ui-testing`.
- **Method:** Followed the README user copy commands, installed Pillow in the unrelated project's `.venv`, and started new Codex CLI processes. The temporary user copy was moved back out after validation.
- **Expected:** User Skill is discovered across projects without a local copy, activates for UI requests, and does not affect ordinary unit-testing prompts.
- **Actual:** The plan-only check read the Skill from the user path. An implicit UI-testing request from the unrelated project also loaded the Skill, used Playwright MCP, observed the expected heading, and produced URL-visible evidence at `user-project/evidence/user-install-implicit/TEST-001/`. A separate unittest question did not load the Skill.
- **Result:** PASS.
- **Issues:** An initial run from the already-running Codex session had no Playwright tool available even though `codex mcp list` showed the server enabled; available computer-use surfaces were also unavailable or denied.
- **Fixes:** Started a fresh CLI/MCP process after setup. The successful run used a process-scoped `default_tools_approval_mode="approve"` override because this non-interactive test runner uses an approval policy that cannot answer prompts. No persistent approval was added.
- **Retest:** A fresh run without an extended startup grace also exposed Playwright after the MCP process was refreshed and produced PASS evidence. User-scope installation was removed after testing.

### Plugin package validation

- **Installation Mode:** Plugin package
- **Environment:** Clean package snapshot containing only `plugin.json`, `.agents/plugins/marketplace.json`, and `skills/prompt-ui-testing/`.
- **Method:** Parsed both JSON files, checked the Skill package path, then registered the snapshot with `codex plugin marketplace add --json` and installed it using `codex plugin add --json prompt-ui-testing@prompt-ui-tester-local`.
- **Expected:** Portable root manifest, valid marketplace entry, Skill at the package's `skills/` location, relative source path, and installable metadata.
- **Actual:** Codex accepted the local marketplace and installed Plugin version `0.1.0` at `~/.codex/plugins/cache/prompt-ui-tester-local/prompt-ui-testing/0.1.0/`. The Plugin was enabled. Its `./` source path resolved from the marketplace root. No `mcp.json` is present; Playwright remains a separately configured host dependency.
- **Result:** PASS.
- **Issues:** On the first Plugin runtime run, the agent guessed an incomplete cache path while reading the Skill. Listing the actual install root exposed the correct path, after which the Skill loaded and the test completed.
- **Fixes:** The agent used the discovered installed path; no package change was warranted.
- **Retest:** The same Plugin runtime session proceeded through Skill loading and returned PASS. The installed Plugin and marketplace source were removed afterward.

### Plugin runtime installation

- **Installation Mode:** Plugin runtime
- **Environment:** Fresh temporary project without a local Skill or user-scope Skill; Plugin installed from the package snapshot above.
- **Method:** Started a new Codex CLI session after Plugin installation. Configured Playwright MCP separately in the host.
- **Expected:** Plugin discovery exposes the packaged Skill; a natural-language UI request activates it, runs Playwright, produces URL-visible evidence, and reports the correct status.
- **Actual:** The agent loaded the Skill from the installed Plugin cache, navigated to `https://example.com/`, verified “Example Domain,” and produced a screenshot with the active URL visible in `plugin-project/evidence/plugin-install/TEST-001/`. A unit-testing prompt did not load the Plugin Skill.
- **Result:** PASS.
- **Issues:** The initial guessed cache path was incorrect; listing the installed cache resolved it during the test.
- **Fixes:** No repository change.
- **Retest:** A subsequent Plugin-backed Firefox run passed after Firefox was installed into a disposable browser cache.

### Playwright MCP and browser setup

- **Availability/configuration:** The Skill and Plugin do not configure Playwright MCP. Codex CLI configuration is host/user configuration and is shared with the ChatGPT desktop app. `codex mcp list` showed the server after the documented add command. A session started with user config ignored had no Playwright server; the Skill returned `BLOCKED`, with no navigation or evidence. This confirms that a missing MCP server is reported as an execution prerequisite, not as an application failure.
- **Approval:** Successful non-interactive sessions used a CLI `-c` override setting `mcp_servers.playwright.default_tools_approval_mode="approve"`. It applied to each validation process and was not persisted. Earlier integration also showed MCP calls are denied when the approval policy is `never` and the tool is not approved. Interactive users may receive host approval prompts; the README warns against globally approving an untrusted server.
- **Approval retest:** With Codex approval set to `never` and the temporary server left at its default `auto` tool-approval mode, `browser_navigate` returned “MCP tool call requires approval, but approval policy is never.” The agent reported `BLOCKED` and did not claim navigation. Repeating with the process-scoped `approve` override allowed navigation and heading verification; the raw screenshot was composed with the evidence helper into a visually checked URL-visible PNG. The temporary MCP server was removed.
- **Reload:** A running session did not gain newly configured tools. Starting a fresh Codex process made them available. ChatGPT desktop MCP changes require the documented **Restart** action.
- **Node and browser:** Node.js 24.13.1 met Playwright MCP's Node 20+ requirement. The default Chrome channel worked because Google Chrome was already installed, so a fresh Chrome binary download was not demonstrated. In a separate browser cache, Firefox first returned “Browser `firefox` is not installed” with the actionable command `npx @playwright/mcp install-browser firefox`. Running `npx --yes @playwright/mcp@latest install-browser firefox` downloaded Firefox and ffmpeg to the disposable cache; the subsequent Plugin + Firefox scenario passed and its URL-visible screenshot was inspected. README now documents this observed fallback even though the official installation page describes first-use browser downloads.
- **Cold package and browser cache:** Added a separate `playwright_clean` server with fresh `NPM_CONFIG_CACHE` and `PLAYWRIGHT_BROWSERS_PATH` directories. The first agent run successfully started the MCP package from the empty npm cache, then Firefox launch reported the missing browser and the Skill returned `BLOCKED` without navigation or evidence. After running `NPM_CONFIG_CACHE=<temp-cache> PLAYWRIGHT_BROWSERS_PATH=<temp-browser-cache> npx --yes @playwright/mcp@latest install-browser firefox`, a new Agent session navigated to `https://example.com/`, verified “Example Domain,” and generated a visually inspected URL-visible screenshot under `approval-project/evidence/cold-package-retest/TEST-001/`. This demonstrates cold package installation and the actionable browser installation recovery path.
- **Approval/reload limitation:** A clean, interactive first-time Codex account was not available. We validated the CLI configuration and session behavior in the existing authenticated profile, with all temporary MCP additions removed afterward.

### Evidence workspace and URL audit

- Successful project, user, Plugin, and Firefox runs each wrote to a unique temporary project and case-specific directory. Repeated runs used new output paths; existing evidence remained present and unchanged. Concurrent runs were not tested; sequential isolation passed.
- The browser-observed URL in each successful run was `https://example.com/`. Playwright traces and the visible URL strip agreed. Project, user, Plugin, Firefox, and cold npm/browser-cache screenshots were visually checked; raw screenshots were retained beside the composed images. Tests used unique directories sequentially; concurrent execution remains untested.
- The invalid-installation check placed the Skill under `skills/prompt-ui-testing` instead of `.agents/skills/prompt-ui-testing`. An explicit invocation failed to find the Skill and reported no browser work. Moving the same copy to `.agents/skills/prompt-ui-testing` made a fresh planning-only session load its references and produce the requested plan. This diagnosed a wrong installation path rather than an application failure.

### Issues and fixes summary

| Issue | Root cause | Smallest fix | Retest |
| --- | --- | --- | --- |
| Evidence composition failed after clean project install | Agent selected system Python instead of project `.venv` where Pillow was installed | Clarified interpreter selection in Skill evidence policy and README | Refreshed install; project E2E PASS with URL-visible screenshot |
| Playwright tools missing in an already-running session | MCP tool catalog was stale after server configuration | Start a fresh Codex/MCP process; no persistent permission change | User-scope E2E PASS in fresh process |
| Playwright call denied under `approval_policy=never` | Server tools were at default `auto` approval and non-interactive Codex could not approve | Apply `default_tools_approval_mode="approve"` only to the trusted validation process | Browser call, heading verification, and URL-visible evidence retest passed |
| Firefox was unavailable in a clean browser cache | Browser executable had not been installed for that browser channel | Run the install command returned by Playwright MCP; documented it in README | Plugin + Firefox E2E PASS with URL-visible screenshot |
| Cold-cache Firefox launch was blocked | The isolated browser cache did not contain Firefox, although the MCP npm package started successfully from a clean npm cache | Install the selected browser using the command returned by MCP | First run correctly BLOCKED without evidence; fresh-session retest PASS with URL-visible screenshot |
| Deliberately invalid project Skill location was undiscovered | Skill was outside the host's supported project Skill directory | Install under `.agents/skills/prompt-ui-testing` | Fresh planning-only session loaded Skill references |

## Installation regression validation

- **Skill validator:** PASS — `quick_validate.py skills/prompt-ui-testing` printed `Skill is valid!`.
- **Evidence helper tests:** PASS — `python -B -m unittest discover -s tests -v`; all 8 tests passed, including URL redaction, readable strip, raw pixel preservation, and refusal to overwrite the raw screenshot.
- **Browser regressions after the interpreter fix:** PASS — project-level retest, user-scope implicit activation, Plugin runtime, and Plugin + Firefox cold-cache retest all completed with the expected `PASS` classification and URL-visible evidence. Screenshots were visually inspected.
- **Install failure regressions:** PASS — missing MCP and invalid project install each returned a clear `BLOCKED`/not-discovered result with no fabricated navigation or screenshot; installing the Skill at the documented path restored discovery.
- **MCP approval regression:** PASS — an unapproved Playwright call under the `never` policy returned `BLOCKED`; the process-only approval override allowed the browser retest without persisting approval.

## Installation phase gaps at phase exit

- **Full requirement matrix:** SSO/MFA handoff, date/time controls, modals, multilingual UI, production guardrails, additional dynamic-loading and browser-network cases, and broader concurrency coverage remain to be validated.
- **Platform coverage:** Project, user, and Plugin installations were exercised through Codex CLI on macOS. ChatGPT desktop Plugin-directory installation and other operating systems were not runtime-tested. A separate clean OS account/container was unavailable because Docker's daemon was not running.
- **Public v0.1.0 release:** Public installation, remaining requirement-matrix validation, final regression, and release-readiness review remain open. The Skill is **not yet declared release-ready**.

## Full Requirement Matrix Validation — 2026-09-26

### Scope and disposition

Created the complete [Requirement Traceability Matrix](REQUIREMENT-TRACEABILITY.md), mapping all 50 sections of `docs/REQUIREMENT.md`, the 30 required browser scenarios, the 10 screenshot acceptance criteria, and the 24 overall acceptance criteria. The inventory also reviewed README, plan, security/contribution/changelog material, Skill references/assets, and Plugin manifests. Each matrix row has a validation method, evidence, status, and gap/notes field.

| Matrix rows | PASS | FAIL | PARTIAL | NOT TESTED | NOT APPLICABLE | BLOCKED |
|---:|---:|---:|---:|---:|---:|---:|
| 111 | 103 | 0 | 8 | 0 | 0 | 0 |

The 111 rows consist of 47 section summaries plus 30 individual test scenarios, 10 screenshot criteria, and 24 overall acceptance criteria; sections 46–48 are decomposed rather than double-counted. `PARTIAL` rows disclose incomplete variants rather than implying coverage. The separate platform table records ChatGPT desktop Plugin runtime and other OS runtime as **NOT TESTED**. Those platform gaps are not Skill failures. Existing integration, installation, and helper evidence was reused where sufficient.

### New Agent scenarios

Environment: Codex CLI `0.156.1` on macOS, Playwright MCP `0.0.82`, Node.js `24.13.1`, and a temporary generic app on `http://localhost:43879` / `http://127.0.0.1:43879`. Every session used a copied Skill in an isolated temporary project, with its own evidence path. The fixtures and screenshots remain outside the repository under `/tmp/prompt-ui-requirement-matrix-20260926/`; no real accounts, credentials, or private targets were used.

| Scenario | Expected | Actual | Validation |
|---|---|---|---|
| Controls and dynamic result | Select, checkbox, radio, date/time, modal, pagination, delayed content, save, and SPA update all match expectations | All requested states appeared; delayed result became “Loaded”; “Form saved” appeared; active URL moved to `/controls/result?token=[REDACTED]`; screenshot showed that URL | PASS |
| Login | Disposable sign-in yields visible success; secret is not reported or captured | “Signed in as Sample User” appeared; password field was empty before the URL-visible screenshot; password value was omitted | PASS |
| SSO unavailable | Do not bypass unavailable SSO or claim protected content | Page identified SSO handoff; no authorized session was available; protected content was not reached; no evidence was claimed | PASS — expected BLOCKED |
| Plan-only | Plan steps without navigation or UI action | Plan returned; trace contains no browser MCP calls | PASS |
| Dry-run, first attempt | Identify target, steps, file, auth, browser availability, consequence; do not execute | No navigation; missing file, SSO, and deletion consequence were identified; browser availability field was omitted | PARTIAL; see issue/fix below |
| Dry-run retest | Include explicit browser-capability status without target navigation | Refreshed Skill reported `Browser capability: not verified`; no browser call, navigation, or evidence | PASS |
| Production-like delete assessment | No destructive action against a production-like target without specific authorization | Agent declined execution, requested explicit target/action authorization or a safer disposable environment; it did not navigate | PASS — safety simulation only |
| Exploratory form | Clearly separate generated cases and avoid inventing business rules | Agent labeled all cases exploratory; empty required input produced browser validation; whitespace-only behavior was `INCONCLUSIVE` because no trim rule was specified; no fabricated requirement was asserted | PASS |
| Invalid date/time probe | Classify only what the UI establishes | Playwright rejected malformed date/time values before they reached the app; the result was recorded as `INCONCLUSIVE`, not an application failure | PASS — limitation accurately reported |
| Spanish UI, Thai prompt | Verify Spanish UI action and report in the user’s language | `Guardar` produced `Guardado`; Thai report included expected/actual and URL-visible evidence | PASS |
| Successful localhost redirect | Follow redirect and capture the post-redirect URL | `/redirect` landed at `http://localhost:43879/controls`; heading matched and final screenshot visibly showed that URL | PASS after retest |
| Two simultaneous independent tests | No evidence, URL, state, or result cross-contamination | Two Agent/Playwright sessions ran at once; both used `TEST-001` in separate workspaces. Each screenshot showed its own URL and page state; both results were PASS | PASS |

The existing evidence remains in force for remote navigation, `127.0.0.1`, form/upload, expected failure, missing element/file, unreachable localhost, all four classifications, redirect/SPA URL updates, URL redaction, non-trigger prompts, and installation modes. This phase did not repeat those runs unnecessarily.

### Issues, root causes, fixes, and retests

| Observed behavior | Root cause | Smallest fix | Retest |
|---|---|---|---|
| An Agent tried system `python3` before a project environment containing Pillow and reported that evidence composition was unavailable | Evidence policy described the preferred interpreter but did not prescribe an explicit check order; an early disposable harness also used a venv symlink that the Agent’s interpreter discovery did not find | Tightened evidence policy to check `.venv/bin/python` or `.venv/Scripts/python.exe` first and only then try `python3`; corrected the disposable harness to use a real project venv | Refreshed Skill and reran localhost redirect; project interpreter was checked first and final URL-visible evidence passed. Login and exploratory cases also passed with ordinary project venvs. |
| Dry-run output omitted browser availability twice | The dry-run requirements named browser availability but did not require an explicit report field | Added a `Browser capability` field with available tool name, unavailable, or not verified; explicitly forbid navigation to determine it | Retest returned `Browser capability: not verified`; no browser calls occurred. |
| A redirect test listed a raw screenshot after a prompt constrained actions to “only” Playwright MCP | The validation prompt did not distinguish browser interaction from shell-based evidence composition | Clarified the test prompt to allow the Skill helper after MCP screenshot capture; no Skill change | Rerun produced and visually verified a URL-visible post-redirect screenshot. |
| Initial auth probe selected an unavailable desktop surface instead of the configured MCP | Test prompt did not identify the required Playwright MCP server | Repeated with the named `matrix_playwright` server | SSO boundary was observed; correctly BLOCKED, with no protected-content claim. |

The whitespace-only exploratory submission was not treated as a product defect: no trim rule was specified, so the Agent reported `INCONCLUSIVE`. The invalid date/time strings were rejected by the browser tool before reaching the app; no Skill change was warranted for that tool limitation. No destructive operation was performed.

### Evidence integrity and concurrency

- New final screenshots were visually checked for the active browser URL. The redirect image showed `http://localhost:43879/controls`; the SPA image showed `/controls/result?token=[REDACTED]`; login evidence was captured only after the fixture cleared the password; Thai and both concurrent screenshots showed their own current URL.
- Sequential isolation from Installation Validation is retained. The new concurrent runs used separate Codex sessions, Playwright contexts, project roots, and evidence directories; no overwrite, stale image, URL leakage, or result mix-up was observed. README already requires independent sessions and paths for concurrent work. Concurrency therefore remains supported with those isolation constraints.
- The helper’s existing raw-pixel preservation and URL-redaction tests remain the evidence for composition integrity. New final PNGs preserve their raw sidecars; no raw image was reported as final URL-visible evidence.

### Regression and privacy checks

- **Skill validator:** PASS — `quick_validate.py skills/prompt-ui-testing`.
- **Helper tests:** PASS — all 8 unit tests passed after the Skill-reference updates.
- **Browser regressions:** PASS — controls/SPA evidence, localhost redirect after evidence-policy change, dry-run after testing-policy change, login, exploratory reporting, and simultaneous session isolation passed their expected outcomes.
- **Installation smoke tests:** No installation instructions, manifest, or package files changed in this phase; project, user/global, and Plugin installation evidence from the prior phase remains valid.
- **Privacy review:** PASS — repository scan found no private organization material. Only generic fixture text, `example.com`, loopback URLs, `Sample User`, and synthetic token values were used. Fake credentials and screenshots remained in temporary validation artifacts; the fake password was not recorded in public documentation.

### Remaining before Final Release Readiness Review

- **PARTIAL control coverage:** autocomplete/custom combobox, tab switching, number/textarea, and drag-and-drop upload variants were not separately exercised. Basic select, checkbox, radio, date/time, file input, dialog, and pagination were exercised.
- **PARTIAL authentication and recovery coverage:** real SSO/MFA handoff, authenticated profile reuse, hot reload, minor UI drift, and measured retry bounds remain untested.
- **Platform coverage:** Codex CLI on macOS is runtime validated. ChatGPT desktop Plugin runtime and other operating systems remain NOT TESTED.
- Final regression and the release-readiness review are still required. **Do not publish or tag v0.1.0 in this phase.** The repository can proceed to Final Release Readiness Review with the above gaps explicit; this matrix does not declare it release-ready.
