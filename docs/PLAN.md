# Implementation plan: prompt-driven UI testing Skill

This plan implements [REQUIREMENT.md](REQUIREMENT.md) as a portable public Agent Skill. The selected name is `prompt-ui-testing`; alternatives considered were `browser-flow-testing` and `web-ui-check`. Version 1 uses an available browser capability, preferably Playwright MCP, and does not modify the application under test.

## Phase 1 — Research

- Verify current Agent Skill format and Codex project/user installation, portable plugin packaging, MCP configuration, and Playwright MCP tools from first-party documentation.
- Confirm semantic snapshots, file upload, page URL retrieval, screenshots, and localhost networking behavior before documenting setup.
- Gate: cite the verified sources in the README and avoid unverified install commands.

## Phase 2 — Privacy and design

- Define prompt interpretation, plan-only and dry-run modes, execution, expected-versus-actual validation, evidence, and reporting.
- Define production protection, authentication handoff, bounded recovery, test isolation, and status rules for `PASS`, `FAIL`, `BLOCKED`, and `INCONCLUSIVE`.
- Review all examples before use; allow only neutral fictional data and public-safe hosts.
- Gate: architecture and examples contain no organization-derived details.

## Phase 3 — Portable Skill

- Create `skills/prompt-ui-testing/SKILL.md` with concise discovery metadata, workflow, mandatory safeguards, and links to focused references.
- Keep policy in `references/`, templates in `assets/`, and deterministic evidence code in `scripts/`.
- Gate: Skill metadata validates and references resolve.

## Phase 4 — Browser workflow

- Use semantic UI inspection and interactions; adapt to small wording changes only when context makes the intended action clear.
- Support common controls, file upload, authentication handoffs, dynamic pages, redirects, multiple tests, multilingual prompts, and localhost targets.
- Distinguish application failures from missing prerequisites and browser-to-localhost connectivity failures.
- Gate: representative prompts yield an evidence-backed status without selectors or target source changes.

## Phase 5 — URL-visible evidence

- Capture the active page URL with each raw screenshot; verify the URL did not change during capture.
- Compose a separate PNG with a readable, safely redacted URL strip above unmodified application pixels; preserve the raw screenshot.
- Gate: all final evidence images show the correct active URL after redirects and SPA navigation, including loopback addresses.

## Phase 6 — Public distribution and documentation

- Provide project and user installation guidance, a portable plugin manifest, Playwright MCP setup, security guidance, and generic example prompts.
- Add README, MIT license, changelog, contribution and security guidance.
- Gate: a new user can install the Skill, supply a browser capability, and run a documented prompt.

## Phase 7 — Validation and dogfood

- Validate format, manifest, links, helper behavior, installation instructions, and the requirement's browser behavior matrix on disposable public/local applications.
- Check every evidence URL, including redirection, SPA changes, redaction, localhost, and `127.0.0.1`.
- Gate: record observed results and limitations; do not claim scenarios that were not executed.

## Phase 8 — Public-release audit

- Search all repository files and generated examples for real names, domains, secrets, internal IDs, private URLs, and proprietary terminology.
- Report implementation, validation, limitations, and remaining improvements.
- Gate: explicitly confirm that repository examples and artifacts are public-safe.

## Version 1 interfaces and defaults

- Primary input: a natural-language test request. Optional project configuration stays outside the reusable Skill.
- Browser: Playwright MCP preferred; another browser capability is acceptable only if it can execute the request and provide trustworthy URL-visible evidence.
- Evidence helper: raw image and active page URL in; preserved raw image and redacted URL-visible PNG out.
- Report: test name, environment, result, inputs, expected, actual, useful steps, evidence, and failure point when relevant.
- Defaults: automatic Skill discovery, meaningful screenshot checkpoints, neutral test IDs, explicit user intent before consequential actions in production-like or uncertain environments, and MIT licensing.

## Sources checked

- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Package plugins](https://developers.openai.com/plugins/build/plugins)
- [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Playwright MCP installation](https://playwright.dev/mcp/installation)
- [Playwright MCP screenshots](https://playwright.dev/mcp/tools/screenshots)
