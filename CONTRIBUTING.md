# Contributing

Contributions should improve prompt-driven, black-box browser testing without requiring changes to the application under test. Keep `SKILL.md` short and place conditional guidance in relevant references. Add scripts only for operations that benefit from deterministic code.

## Branching Strategy

- `main` is the stable public and release branch. Do not use it for ordinary development.
- `develop` is the integration branch for reviewed work, integration validation, regression, and release preparation.
- Every normal change starts from an up-to-date `develop` on a dedicated task branch. Use `feature/<short-description>`, `fix/<short-description>`, `docs/<short-description>`, `test/<short-description>`, `refactor/<short-description>`, or `chore/<short-description>` as appropriate.
- A genuine urgent fix may use `hotfix/<short-description>` from `main`; validate it, review it whenever circumstances allow, and merge it back to both `main` and `develop`.
- Keep branch names generic and public-safe. Never include private organization names, internal project terms, private URLs, credentials, or confidential identifiers.

The normal path is:

```text
task branch
  → Pull Request targeting develop
  → independent Review Sub-agent
  → Main Agent fixes and updates the PR
  → fresh re-review after material fixes
  → approved merge commit into develop
  → integration and regression validation
  → deliberate promotion from develop to main
  → release tag from validated main
```

Do not merge normal task branches directly into `develop` without a PR, or directly into `main`. A release promotion should use a PR from `develop` to `main` where practical and show the complete release delta. Do not tag an unreviewed task branch or unvalidated `develop`.

### Review-only Sub-agent

Every normal PR into `develop` requires a dedicated Review Sub-agent after the PR is opened. Provide the reviewer the current PR diff, relevant requirements and conventions, and available validation evidence. The reviewer independently examines changed files and surrounding context for correctness, regressions, requirement alignment, security, privacy, error handling, tests, maintainability, documentation, installation, and release impact.

Use a prompt equivalent to this contract:

```text
You are the dedicated Pull Request reviewer. Review only.
Do not modify files, write code, commit, push, merge, rebase, or change repository state.
Inspect the current PR changes and relevant surrounding context, requirements, and conventions.
Return structured findings and recommendations to the Main Agent.
Prioritize correctness, regressions, security, privacy, requirement compliance, tests,
maintainability, and documentation. Separate blocking findings from non-blocking suggestions.
```

The reviewer is strictly read-only. It reports findings to the Main Agent and must not modify files, implement fixes, commit, amend, push, rebase, merge, change settings, or resolve comments by editing. Review feedback must distinguish `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, and `SUGGESTION`, and include the affected file/location, problem, impact, and recommended direction where applicable. Use this format:

```text
Overall Review: APPROVE or CHANGES REQUESTED
Blocking Findings:
- ...
Non-blocking Findings:
- ...
Suggestions:
- ...
Validation Concerns:
- ...
Files Reviewed:
- ...
Summary:
...
```

The Main Agent owns all fixes and decides each meaningful finding as `ACCEPT`, `REJECT WITH JUSTIFICATION`, or `DEFER WITH JUSTIFICATION`. Accepted fixes stay on the same task branch; rerun relevant checks, update the PR, and request a fresh Review Sub-agent for material changes. Record the final status in the PR as `APPROVED FOR DEVELOP` or `CHANGES STILL REQUIRED`. Tests passing, small diff size, or documentation-only scope do not waive independent review. Do not claim a GitHub reviewer approval unless the platform actually records one.

### Contributor and Agent Checklist

Before implementation:

- [ ] Confirm current branch, task type, and target branch.
- [ ] Fetch remote refs and ensure `develop` is current.
- [ ] Create a dedicated task branch from `develop`.

Before opening a PR:

- [ ] Complete the focused implementation and relevant tests.
- [ ] Update documentation where needed and run applicable privacy checks.
- [ ] Ensure the working tree and task diff are clean and the PR targets `develop`.

During PR review:

- [ ] Create an independent, read-only Review Sub-agent.
- [ ] Evaluate and disposition meaningful findings; implement accepted fixes as Main Agent.
- [ ] Request re-review after material fixes and record the final review status.
- [ ] Resolve blockers and high findings or document a clear justification before merge.

Before merge and promotion:

- [ ] Merge to `develop` only after review and relevant task-branch checks pass.
- [ ] Run integration and regression validation on `develop`.
- [ ] Promote to `main` only after release readiness, privacy, and relevant security checks pass.

Use fictional data in every example and fixture. Do not submit credentials, session state, private URLs, confidential screenshots, real account details, internal IDs, or organization-specific terminology. Public examples should use `example.com`, loopback addresses, and neutral names such as `Sample User` and `TEST-001`.

For evidence-helper changes, install `requirements.txt` and run:

```sh
python3 -m unittest discover -s tests -v
```

Check that raw screenshot pixels remain intact in the composed image, sensitive URL parts are redacted, and the active URL is readable. For Skill policy changes, walk through a representative prompt and confirm the expected status, safety decision, and evidence behavior. See [docs/PLAN.md](docs/PLAN.md) for the full validation phases.

## Release privacy checks

Before creating a release tag, configure Git to use the GitHub-provided `noreply` commit email. Keep the email private in GitHub account settings and enable the option to block command-line pushes that expose a personal email. Verify the effective identity with `git config user.name` and `git config user.email`.

Run the release metadata check and inspect file contents and secrets separately:

```sh
python3 scripts/check_git_metadata_privacy.py
```

The metadata check scans reachable commit author and committer fields plus annotated tagger fields. It allows GitHub `users.noreply.github.com` identities and redacts unapproved addresses in its output. Before tagging, also run the repository privacy scan, secret scan, Skill validator, helper tests, manifest checks, link checks, and `git diff --check`.

### Branch protection recommendations

These are recommendations for repository administrators; contributors and Agents must not change GitHub settings as part of ordinary work. Protect `main` against ordinary direct pushes and prefer reviewed release promotion with relevant required checks. Prefer PRs from task branches into `develop`, requiring review and practical validation checks before merge. Settings changes require separate authorization.
