# Changelog

## v0.1.0 — 2026-09-26

- Prompt-driven black-box UI testing for remote sites and localhost applications, using Playwright MCP as a separately configured browser capability.
- Natural-language planning and execution for forms, common controls, file-input uploads, redirects, and SPA navigation, with Expected vs Actual validation and `PASS`, `FAIL`, `BLOCKED`, or `INCONCLUSIVE` results.
- URL-visible screenshot evidence composed from browser-observed URLs, with conservative URL redaction, retained raw captures, and isolated per-test workspaces. Concurrent runs were validated when each uses separate browser sessions and evidence paths.
- Project and User/Global Skill installation guidance, Plugin packaging, and Plugin runtime validation in Codex CLI on macOS, plus safety policies, report assets, and generic public-safe examples.
- Known limits include unvalidated custom controls and interaction variants, real SSO/MFA handoff and profile reuse, some dynamic UI/recovery behavior, and runtime validation beyond Codex CLI on macOS. See the README compatibility and Known Limitations sections.
