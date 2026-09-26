# Changelog

## v0.1.3 release candidate — 2026-09-26 (not yet published)

Fullscreen browser execution improvement for desktop UI testing.

### Changed

- Prefer Google Chrome in headed, isolated Fullscreen sessions.
- Use maximized mode as a fallback when Fullscreen cannot be established.
- Preserve isolated state per independent case and one session across that case's steps.

### Validation

- Chrome 154, headed Fullscreen, viewport tracking, isolated restart behavior, localhost and remote navigation, URL-visible evidence, redaction, and fallback behavior validated with Playwright MCP 0.0.82 on macOS.
- Sanitized authenticated-application dogfooding: **PASS** for Fullscreen, form interaction, authentication flow, post-login navigation, and URL-visible evidence. Private targets and artifacts are not included.

### Notes

- Computer Use is not required for normal Fullscreen browser execution.
- Fullscreen runtime validation covers macOS only. Other operating systems and multi-monitor placement remain unvalidated; headless runs do not use desktop Fullscreen.

## v0.1.2 — 2026-09-26

Browser-execution and test-isolation improvements for the existing Skill.

### Changed

- Prefer Google Chrome and headed browser execution for UI tests.
- Start each independent case in a fresh isolated session; retain one session across that case's steps.
- Require explicit intent to reuse supplied authentication or browser state, and report that deviation.
- Use best-effort maximization while continuing in a headed window if it is unavailable.

### Documentation

- Clarified that Playwright isolated state serves the private-session intent without claiming Chrome's native Incognito UI.
- Clarified that Computer Use is not required for normal browser testing.
- Documented that true OS fullscreen is not guaranteed and maximization is best-effort.

### Validation

- Google Chrome 154, headed execution, isolated sequential cases, explicit synthetic storage-state reuse, best-effort maximization, localhost interaction, remote navigation, SPA URL update, and URL-visible evidence validated with Playwright MCP 0.0.82 on macOS.
- Other operating systems and real authenticated profile reuse were not runtime validated.

## v0.1.1 — 2026-09-26

This privacy and release correction supersedes the withdrawn `v0.1.0`; it contains the same initial Skill functionality.

### Security / Privacy

- Re-published the initial release from sanitized Git metadata.
- Added permanent Git metadata privacy validation to the release checks.

## v0.1.0 — 2026-09-26

- Prompt-driven black-box UI testing for remote sites and localhost applications, using Playwright MCP as a separately configured browser capability.
- Natural-language planning and execution for forms, common controls, file-input uploads, redirects, and SPA navigation, with Expected vs Actual validation and `PASS`, `FAIL`, `BLOCKED`, or `INCONCLUSIVE` results.
- URL-visible screenshot evidence composed from browser-observed URLs, with conservative URL redaction, retained raw captures, and isolated per-test workspaces. Concurrent runs were validated when each uses separate browser sessions and evidence paths.
- Project and User/Global Skill installation guidance, Plugin packaging, and Plugin runtime validation in Codex CLI on macOS, plus safety policies, report assets, and generic public-safe examples.
- Known limits include unvalidated custom controls and interaction variants, real SSO/MFA handoff and profile reuse, some dynamic UI/recovery behavior, and runtime validation beyond Codex CLI on macOS. See the README compatibility and Known Limitations sections.
