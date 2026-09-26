# Repository Agent Workflow

Before changing files, inspect the current branch, target branch, and task type. Keep `main` as the stable release branch; do not make ordinary feature, fix, documentation, test, refactor, or tooling changes directly on it.

For normal work, update `develop`, create a focused task branch from it, and implement only on that task branch. Open a Pull Request targeting `develop`; do not merge a task branch directly into `develop` or target a normal task PR at `main`.

Every normal PR into `develop` requires an independent Review Sub-agent after the PR is opened. The reviewer is read-only: it may inspect the current diff and relevant context and return findings, but must not edit files, commit, push, rebase, merge, resolve comments by editing, or change repository settings. Do not describe self-review as independent review. The Main Agent evaluates every meaningful finding, implements accepted fixes on the same task branch, records reasons for rejected or deferred findings, updates the PR, and requests a fresh review after material changes. Repeat until there are no unresolved BLOCKERs or HIGH findings without justification and the final status is `APPROVED FOR DEVELOP`.

Only the Main Agent or an authorized repository workflow merges an approved PR into `develop`. Use a merge commit for task PRs. Run relevant integration and regression checks on `develop` after merge. Promote `develop` to `main` only through a deliberate release PR or equivalent controlled promotion after release readiness is confirmed; create public tags from validated `main` only.

True urgent hotfixes may start from `main`, but must be validated and reviewed whenever circumstances allow, then merged back into both `main` and `develop`. Security, privacy, and release-recovery exceptions require explicit authorization. Do not rewrite published history merely to recreate this workflow. Keep branch names, PRs, tests, and documentation public-safe.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the detailed branching, review, and validation checklists. Use the repository [Pull Request template](.github/pull_request_template.md).
