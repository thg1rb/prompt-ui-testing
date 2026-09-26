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

### Gaps recorded at the end of matrix validation

- **PARTIAL control coverage:** autocomplete/custom combobox, tab switching, number/textarea, and drag-and-drop upload variants were not separately exercised. Basic select, checkbox, radio, date/time, file input, dialog, and pagination were exercised.
- **PARTIAL authentication and recovery coverage:** real SSO/MFA handoff, authenticated profile reuse, hot reload, minor UI drift, and measured retry bounds remain untested.
- **Platform coverage:** Codex CLI on macOS is runtime validated. ChatGPT desktop Plugin runtime and other operating systems remain NOT TESTED.
- At that phase exit, final regression and release readiness were still pending. The release review and current disposition are recorded below.

## Final Release Readiness Review — 2026-09-26

### Result and requirement coverage

- **Release candidate:** `v0.1.0`
- **Overall status:** READY FOR v0.1.0. No concrete release blocker was found. No tag or publication was created.
- **Current traceability totals:** 111 rows; 105 PASS, 0 FAIL, 6 PARTIAL, 0 NOT TESTED, 0 NOT APPLICABLE, 0 BLOCKED. REQ-047 and REQ-111 moved from PARTIAL to PASS after the artifact and publication-suitability review. Earlier phase tables retain their as-of-phase counts.
- **Remaining PARTIAL decisions:** REQ-010, REQ-011, REQ-022, REQ-028, REQ-029, and REQ-103 are acceptable v0.1.0 limitations. Their unverified variants and safe fallbacks are summarized in README and detailed in the traceability matrix. Each is listed with its decision in [RELEASE-READINESS.md](RELEASE-READINESS.md).

### Public documentation and platform claims

- README now contains Compatibility and Known Limitations sections and Windows-specific Python environment commands. The 0.1.0 changelog summarizes the validated workflow and explicitly points to known limits.
- Current official Skill, Plugin, MCP, and Playwright documentation was checked. README correctly presents Playwright MCP as a separate dependency (Node.js 20+), covers browser first-use/download behavior, possible host approval, MCP restart/fresh-process behavior, and `BLOCKED` behavior when browser execution is unavailable.
- **Runtime coverage:** Codex CLI on macOS, including project, user/global, and Plugin installations, is validated. ChatGPT desktop Plugin runtime and other operating systems are documented as untested; their design compatibility is not represented as runtime validation.

### Security, privacy, evidence, and hygiene

- **Security review:** PASS. Production safety and explicit intent for consequential actions are documented. The helper accepts a URL through structured stdin, performs no shell execution, redacts URL metadata, and retains raw screenshots. Input/output paths are explicit caller arguments and are not derived from target-page content; instructions use isolated evidence workspaces. Documentation does not claim that metadata redaction removes secrets visible in page pixels.
- **Privacy review:** PASS. Tracked public content uses generic examples and public documentation links. No real credentials, private targets, organization-specific examples, private screenshots, or validation artifacts were found in the repository; credential-like values in helper tests are synthetic redaction inputs.
- **Evidence review:** PASS using the existing helper tests and integration/concurrency records. Browser-observed URL strips, redirects, SPA changes, redaction, image preservation, and isolated concurrent evidence were validated in earlier phases.
- **Repository hygiene:** PASS. No in-repository virtualenv, browser profile, screenshots, caches, or validation workspaces were found; `.gitignore` covers the current Python and evidence artifacts. The working tree was clean before this review, and no v0.1.0 tag exists.

### Final regression

- **Skill validator:** PASS — `quick_validate.py skills/prompt-ui-testing`.
- **Helper tests:** PASS — all 8 unit tests, run with an isolated temporary Python environment containing Pillow.
- **Browser smoke evidence:** PASS by reuse of the same-date remote (`https://example.com`) and localhost redirect/form/SPA Playwright MCP scenarios documented above. No browser scenario was rerun because this release review changed public documentation only and Playwright MCP was not exposed in the current review process.
- **README installation smoke:** PASS — copied the Skill into a new temporary project's `.agents/skills/prompt-ui-testing`, created its `.venv`, installed Pillow, and started a fresh Codex CLI session. Explicit Skill invocation discovered the installed copy, read its references, and returned the requested plan-only response without browser calls. This smoke covers the macOS/Unix command path; Windows commands remain untested.
- **PASS/FAIL/BLOCKED classification and URL-visible evidence:** PASS by reuse of the full matrix records, including expected FAIL, BLOCKED, and INCONCLUSIVE results and visually audited screenshots.
- **Documentation and manifests:** PASS — Markdown links checked, JSON manifests parse, and `git diff --check` passes.
- **Installation smoke:** Existing Project, User/Global, and Plugin runtime records remain applicable. The README's Unix copy and Pillow setup path was exercised in a clean temporary project; no Plugin or manifest command changed. Windows commands were added as unvalidated platform guidance, not as a runtime support claim.

No implementation defect was found. Deferred variants and untested platform runtimes are documented limitations, not blockers for this candidate.

## Chrome isolated headed browser defaults — 2026-09-26

### Environment and configuration

- Codex CLI `0.156.1` on macOS; Playwright MCP `0.0.82`; Node.js `v24.13.1`; Google Chrome `154`.
- Used `--browser=chrome --isolated`, `launchOptions.headless=false`, `launchOptions.args=["--start-maximized"]`, and `contextOptions.viewport=null`. No `--headless`, Chrome `--incognito`, or OS fullscreen option was used. The MCP configuration was a process-only override; persistent user MCP settings were not changed.
- A disposable fixture was served only on `127.0.0.1`. It stores a synthetic sign-in marker in a cookie, local storage, and session storage; no real credentials or accounts were used.
- The configured browser reported `navigator.userAgentData.brands` containing `Google Chrome 154`. Headed mode was set explicitly. Reported outer window size `1800×1130` matched the available desktop area `1800×1130`; this validates maximization in this macOS environment only.
- Every successful evidence image was composed from a raw Playwright screenshot and the browser-observed `http://127.0.0.1:43992/` URL. The URL strip and page content were visually checked. Images and fixture files remain under a disposable `/tmp` workspace and are not committed.

### Scenarios

| Scenario | Expected | Actual | Result |
| --- | --- | --- | --- |
| Chrome selection and headed/maximized localhost run | Launch branded Google Chrome visibly, use the available work area, interact with the page, and produce URL-visible evidence | Google Chrome 154 reported; `headless=false`; outer dimensions matched available desktop dimensions; heading and synthetic signed-in state matched; composed screenshot displayed the current localhost URL | PASS |
| Fresh isolated process | State set in Session A is absent in a new isolated Session B | The new process displayed “No sign-in state found”; local storage, session storage, and cookies were empty | PASS |
| Browser close then new case in the same MCP connection | Closing Case A's browser session clears state before Case B | After `browser_close`, a new navigation in the same Codex/Playwright MCP connection showed no sign-in marker, empty storage, and no cookies | PASS |
| Screenshot integrity after maximize | Final evidence still visibly shows the actual current URL without losing page pixels | URL strip matched the Playwright-observed URL; composed image preserved the captured page below the strip | PASS |

### Findings and limitations

- The README previously recommended `--headless`, contrary to the requested visible default. Setup guidance now selects Chrome and isolated mode, with headed operation and a tested maximized-window config.
- Native Chrome Incognito was intentionally avoided; Playwright MCP isolated mode met the state-isolation requirement. Native Incognito UI and OS fullscreen were not used or claimed.
- Computer Use is not a normal dependency or automatic fallback. It may be considered only for a required interaction Playwright MCP cannot perform and only when browser/session and evidence constraints remain satisfiable.
- Chrome identity, headed launch, and maximization were validated on this macOS environment only. Other operating systems and display managers remain untested. If Chrome is unavailable, report the limitation and do not silently switch browsers when identity matters.
- Authentication was validated with a synthetic local marker, not a real account. Authentication-dependent tests should log in within the isolated case or use explicitly requested storage state; persistent profile reuse remains an explicit, reportable exception.

## v0.1.2 release-candidate validation — 2026-09-26

### Environment and configuration

- Codex CLI `0.156.1`, Playwright MCP `0.0.82`, Node.js `v24.13.1`, Google Chrome `154`, macOS.
- Used a process-only MCP configuration with `--browser=chrome --isolated`, `launchOptions.headless=false`, `--start-maximized`, and `contextOptions.viewport=null`. No persistent MCP settings were changed.
- Local tests used a disposable fixture served only on `127.0.0.1:43661`; remote navigation used `https://example.com`. Browser state was synthetic, with no real credentials or account.
- On the local run, Playwright reported a `1920×1050` outer window on a `1920×1080` screen and a `1920×963` viewport. This is consistent with a maximized headed window in this macOS environment; other platforms remain untested.

### Release-candidate scenarios

| Scenario | Expected | Actual | Result |
| --- | --- | --- | --- |
| Local multi-step case and SPA URL | In one case session, set synthetic state, complete the flow, and observe `/complete` | The state appeared in cookie, local storage, and session storage; “Sample flow complete” appeared and the browser URL became `http://127.0.0.1:43661/complete` | PASS |
| Independent case isolation | After closing Case A, Case B has no prior case state | Case B opened with empty cookie, local storage, and session storage; “Sample Checkout” remained visible | PASS |
| Explicit state reuse exception | When explicitly requested, supplied state can be loaded and the deviation from the fresh-session default is reported | Synthetic storage state was explicitly restored; the page reported state present. The report called out the deviation and did not claim real-account or persistent-profile reuse | PASS |
| Local URL-visible evidence | Final screenshot shows the browser-observed current URL and preserves page content | Composed image showed `http://127.0.0.1:43661/complete` above the captured completion page; raw screenshot was retained | PASS |
| Remote navigation | `https://example.com` shows “Example Domain” and evidence uses the active URL | Heading and title matched; final image visibly showed `https://example.com/` and the page | PASS |
| Remote URL-visible evidence | Capture the actual active URL, not just the requested URL | Browser evaluation reported `https://example.com/`; composed evidence displayed that URL | PASS |
| Result classification regression | Correct PASS behavior and no change to established FAIL/BLOCKED behavior | Current local and remote cases returned PASS. Existing expected application-error (`FAIL`) and unavailable prerequisite (`BLOCKED`) integration scenarios remain valid and were reused; classification code was unchanged | PASS |
| URL redaction and composition regression | Redact sensitive URL metadata without changing raw pixels | All evidence-helper tests passed, covering URL redaction and raw-pixel preservation; prior redirect/SPA/redaction integration evidence remains applicable | PASS |

Successful raw and composed screenshots were visually inspected from the disposable workspace and are not committed. A first attempt to compose local evidence ran in a read-only nested sandbox and was interrupted after helper write permission was denied; the final successful runs used explicit workspace-write permissions. This was a test-run setup issue, not a Skill or helper defect.

### Scope and limitations

- The dedicated feature validation and release-candidate checks both used macOS, Playwright MCP `0.0.82`, and Google Chrome `154`; no claim is made for other platforms.
- Native Chrome Incognito UI and true OS fullscreen were not used or claimed. Maximization is best-effort.
- Real SSO/MFA and persistent authenticated profile reuse remain untested. Only explicit synthetic storage-state restoration was exercised.
- An existing validated expected-error scenario produced the expected `FAIL`; the unavailable-prerequisite scenario produced `BLOCKED`. These were reused rather than manufacturing a failure in the release-candidate fixture.

## Chrome Fullscreen browser behavior — 2026-09-26

### Environment and configuration

- macOS `27.0`, Node.js `v24.13.1`, Playwright MCP `0.0.82`, Google Chrome `154.0.8037.57`.
- The MCP server was started with the package's stdio transport from a disposable Node MCP client. The process-only config used `channel: "chrome"`, `headless: false`, `--start-fullscreen`, `isolated: true`, `contextOptions.viewport: null`, and the packaged `chrome-window-mode.cjs` `initPage` hook. No persistent Codex MCP settings were changed.
- `navigator.userAgentData.fullVersionList` reported `Google Chrome 154.0.8037.57`. `page.viewportSize()` returned `null`.
- In the primary localhost run, the host reported a `1920×1080` screen and `1920×1050` available area at DPR 1. After the Fullscreen transition settled, Chromium reported `windowState: fullscreen`; the browser content bounds and page viewport were `1920×992`, and the raw screenshot was `1920×992`. A separate isolated run selected a display reported as `1800×1169` and produced an `1800×1042` page viewport and raw screenshot. This confirms that the viewport varies with the browser-selected display/window; no monitor dimensions were hardcoded or explicitly selected. `page.viewportSize()` returned `null` in both headed runs.

### Scenarios

| Scenario | Expected | Actual | Result |
| --- | --- | --- | --- |
| Chrome identity and headed Fullscreen localhost case | Visible Google Chrome starts in Fullscreen, the page follows the browser content area, and a safe interaction succeeds | Chrome `154.0.8037.57` was identified. CDP reported `windowState: fullscreen`; viewport was `1920×992` on a `1920×1080` screen. The fixture rendered its desktop layout, the Save state button updated the UI and synthetic storage, and the same case session retained that state | PASS |
| Independent case and browser restart | A new isolated test starts Fullscreen without state from the previous case | A new MCP server process reported Fullscreen again. The fixture found no prior cookie, local-storage, or session-storage marker; its desktop layout remained active | PASS |
| Remote navigation | Safe public page loads with its expected heading and Fullscreen viewport | `https://example.com/` loaded; the heading and title were `Example Domain`; CDP reported Fullscreen; the raw screenshot and page viewport were `1800×1042` on the display selected for that session | PASS |
| Fullscreen screenshot and URL composition | Raw screenshot matches the page viewport; final evidence shows the browser-observed URL and preserves page pixels | Raw localhost and remote screenshots were `1920×992` and `1800×1042`, respectively. The composed URL-visible images were `1920×1046` and `1800×1096`; each displayed the actual observed URL above the page. Both were visually inspected | PASS |
| Responsive layout | The app uses the actual Fullscreen content viewport, not a fixed or guessed size | Local fixture reported `1920×992 desktop layout`, above its `1600px` desktop breakpoint. In the separate `1800×1042` session, the page viewport and raw screenshot also matched the selected window content size | PASS |
| Maximized fallback and unverified reporting | Failed Fullscreen uses maximized mode when available; unavailable window control is not claimed as Fullscreen | Node's built-in tests simulated CDP returning normal after the Fullscreen request, then confirmed a maximized request and `maximized-fallback` report. A CDP-unavailable case reported `unverified`. A real unsupported-host fallback was not available on this macOS host | PASS (simulated fallback) |
| Explicit headless mode | Headless execution does not request or claim Fullscreen | Headless Chrome was identified by its standard user-agent marker; the helper skipped window control and CDP remained `normal` (`756×469` page viewport in an `800×600` virtual screen) | PASS |

### Findings and fixes

| Finding | Observed behavior and root cause | Fix and retest |
| --- | --- | --- |
| Fullscreen launch flag and direct state request were insufficient | With `--start-fullscreen` alone, CDP reported a normal `1200×1006` Chrome window and page viewport `1200×919`. A direct Fullscreen request from a normal window also remained normal on this Playwright MCP/macOS path. Maximizing first, then requesting Fullscreen, succeeded | The `initPage` helper now establishes a maximized base window before requesting Fullscreen through Chromium's `Browser.setWindowBounds`. It verifies the final state and falls back to maximized if needed. Fresh MCP reruns reported Fullscreen and the responsive fixture used the `1920×992` content viewport |
| Fullscreen state could be transient during startup | A timing trace showed an intermediate `1920×1080` viewport followed about `600ms` later by the settled `1920×992` content area. The first helper version could accept an early Fullscreen state without waiting for the native transition | The helper now samples CDP bounds and viewport metrics every `100ms`, requires them unchanged for `700ms`, and applies a five-second bound. Local and remote retests confirm the settled Fullscreen state before interaction or capture |
| CDP can report Fullscreen in headless Chrome | A headless MCP run returned `windowState: fullscreen` after a protocol request, even though its browser was not visible. CDP window state alone does not prove headed execution | The helper now detects the standard `HeadlessChrome` user-agent marker and skips window controls. The headless retest remained `normal`; a unit test confirms no CDP session or Fullscreen request is made |

### Regression and limitations

- `node --test tests/test_chrome_window_mode.cjs`: 4 passed, including Fullscreen success, maximized fallback, unverified-mode reporting, and headless behavior.
- `node` MCP-client scenarios exercised remote navigation, localhost interaction, browser restart, independent-session state isolation, CDP window-state inspection, and URL-visible evidence composition. The change was not run through a Codex Agent session because the current Agent tool surface did not expose Playwright MCP directly; the Playwright MCP server itself was exercised over stdio.
- True Fullscreen and viewport behavior were runtime validated on macOS with Chrome `154.0.8037.57` only. Windows, Linux, explicit multi-monitor placement, and a real-host maximized fallback remain unvalidated. Chrome/OS chooses the display; the Skill does not move windows between monitors. A failed window-mode request is reported as a browser/runtime limitation, not an application `FAIL`.
- `--start-fullscreen` is retained as the startup preference, but the validated MCP hook is needed for this runtime. Headless execution does not claim Fullscreen. Native Chrome Incognito is not used; the MCP isolated context remains the session privacy mechanism. Computer Use is not required.

## v0.1.3 release-candidate validation — 2026-09-26

### Environment and configuration

- macOS `27.0`, Node.js `v24.13.1`, Playwright MCP `0.0.82`, Google Chrome `154.0.8037.57`.
- Used a disposable Node MCP client over stdio with `--browser=chrome --isolated`; `headless` was `false`, `--start-fullscreen` was set, and `contextOptions.viewport` was `null`. The packaged `chrome-window-mode.cjs` hook maximized first, requested Fullscreen over CDP, and verified a stable window/viewport before navigation. No persistent MCP settings changed.
- Browser identity was checked using `navigator.userAgentData.fullVersionList`; CDP `Browser.getWindowForTarget` reported `windowState: fullscreen`. `page.viewportSize()` returned `null`.
- The selected display reported `1920×1080` CSS pixels; the Fullscreen content viewport, CDP bounds, `innerWidth/innerHeight`, and raw screenshot were all `1920×992`. No monitor resolution was configured or hardcoded.
- Browser automation used only a disposable localhost fixture and `https://example.com`. All evidence images and fixture data remained outside the repository.

### Release-candidate scenarios

| Scenario | Expected | Actual | Result |
| --- | --- | --- | --- |
| Chrome, headed Fullscreen, and viewport | Branded Chrome is headed, CDP confirms Fullscreen, and the page viewport follows the window | Chrome `154.0.8037.57` was identified; headless was disabled; CDP reported `fullscreen`; viewport and bounds were `1920×992` on the selected `1920×1080` screen | PASS |
| Local interaction and same-case continuity | One case uses one isolated session across steps and interaction updates visible UI/state | The fixture began with no cookie or web-storage state. Filling `TEST-001` and clicking Save updated the page and cookie, local storage, and session storage in the same session | PASS |
| Independent case and browser restart | A fresh session starts in Fullscreen and inherits no state from the previous case | A second MCP server/browser session reported Fullscreen and found no prior cookie, local-storage, or session-storage marker | PASS |
| Responsive viewport | Application layout uses the actual Fullscreen content viewport rather than fixed emulation | The fixture reported `1920×992 desktop layout`; `viewport: null` and page dimensions matched the Fullscreen CDP bounds | PASS |
| Safe public remote navigation | `https://example.com/` loads its expected heading in Fullscreen Chrome | Google Chrome reported Fullscreen at `1920×992`; title and heading were `Example Domain` | PASS |
| Screenshot and URL evidence | Raw screenshot represents the tested viewport; composed screenshot shows the observed URL, preserves content, and redacts sensitive URL values | Local and remote raw images were `1920×992`; composed images were `1920×1046`. The local synthetic query value appeared as `[REDACTED]`; both URL strips and page content were visually inspected | PASS |
| Result classification | Expected UI outcome is classified as successful | The local Save confirmation and remote heading matched their expected results; both smoke cases were classified `PASS` | PASS |
| Maximized fallback and unverified mode | Unsupported Fullscreen uses an honest maximized fallback; unverified state is not claimed as success | Helper tests simulated Fullscreen rejection and confirmed `maximized-fallback`; CDP-unavailable case reported `unverified`. A real unsupported-host fallback was not available | PASS (simulated fallback) |
| Authenticated private-application dogfooding | Real authenticated UI flow completes in the new Fullscreen mode with URL-visible evidence | User-confirmed dogfooding passed for Google Chrome, headed Fullscreen, form interaction, authentication flow, post-login navigation, and URL-visible evidence. No target details, screenshots, credentials, logs, or paths are included here | PASS (sanitized confirmation) |

A transient authentication-related application/network response was observed during the private dogfooding login sequence; the expected UI flow completed successfully. This is recorded generically and was not attributed to Skill behavior.

### Regression and limitations

- Skill validator: **PASS**. Python helper/privacy tests: **13 passed**. Fullscreen helper tests: **4 passed**. Git metadata privacy guard: **PASS**. Plugin manifest parse and relative Markdown link validation: **PASS**. `git diff --check`: **PASS**.
- The Fullscreen browser scenarios used the direct Playwright MCP stdio client because Playwright MCP was not exposed directly in the current Agent tool surface; no Codex Agent execution is claimed by these rows.
- True Fullscreen and viewport behavior are runtime validated on macOS with Chrome `154.0.8037.57` and Playwright MCP `0.0.82`. Other operating systems, explicit multi-monitor placement, and real-host maximized fallback remain unvalidated. Headless execution does not use desktop Fullscreen.
- Native Chrome Incognito UI and Computer Use are not required. Existing URL evidence redaction and PASS/FAIL/BLOCKED/INCONCLUSIVE policies are unchanged.
