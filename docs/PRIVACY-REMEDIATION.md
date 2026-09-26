# Git Metadata Privacy Remediation

**Status: local remediation verified; public remote remediation awaits explicit authorization.** This record intentionally omits the exposed email and the old commit hashes.

## Exposure and Impact

The public repository's complete reachable history contained five commits. In all five, both the author email and committer email used one non-anonymous address (masked as `b***@***`). The annotated `v0.1.0` tag object also used that address in its tagger field. Six Git objects were therefore affected: five commits and one tag object.

The public refs observed were `main` (default branch), `develop`, and annotated tag `v0.1.0`; the GitHub Release points to that tag. The public repository API showed zero forks, zero pull requests, and zero release assets at inspection time. This does not rule out external clones, cached commit views, or copies outside GitHub's visible refs.

The exact pre-rewrite commit and tag object IDs, field mapping, and reachability by ref are recorded in a mode-600 local impact inventory and the local `git-filter-repo` maps. They are intentionally omitted from this public-safe record to avoid retaining direct references to the affected Git objects.

## Local Remediation and Verification

- Configured this repository's Git identity to the account's ID-based GitHub `noreply` identity. No global Git configuration was changed.
- Created and verified an owner-only local Git bundle containing the pre-remediation branches, tag, remote-tracking refs, and complete history. The bundle is outside the repository and must not be published or shared because it retains the exposed metadata.
- Rewrote all reachable commit author and committer emails and the annotated tagger email using `git-filter-repo` 2.47.0. The rewritten repository contains five commits and the `v0.1.0` tag; the Git object IDs changed.
- Compared all five old/new commit tree IDs: all are identical. File contents, commit order, commit messages, names, and timestamps were preserved.
- Removed the original release commit identifier from the local `v0.1.0` record so current documentation does not provide a direct link to an affected Git object. This documentation correction is separate from the metadata-only history rewrite.
- Marked the earlier release-readiness report as superseded so it cannot be mistaken for approval of the privacy-affected public release.
- Scanned every reachable commit author and committer field and annotated tagger field in both the isolated rewrite and this working repository: no non-allowlisted email remains. The rewritten repository has no unreachable legacy objects according to `git fsck --full --no-reflogs --unreachable`.
- Immediately after rewriting, before adding this remediation record and metadata check, local sanitized refs were `main` at `72eddaead857d2228c55b4697972388890b5d5ee`, `develop` at `41339844dbfc01fd444c653da1545fb19cb01816`, and `v0.1.0` at `4d0bb85e0969b72190d68c9dc411790798ebb962`.
- The original public remote has not been modified. The `origin` remote was removed from this local checkout by the history-rewrite tool; it will not be restored until remote remediation is authorized.

## Regression Results

- Skill validator: **PASS**.
- Helper and metadata-check tests: **PASS**, all 11 tests. Tests confirm that author, committer, and annotated tagger email violations fail without printing the address.
- Reachable metadata scan: **PASS**, five commits and one annotated tag object; no unapproved identity fields.
- Clean project install smoke: **PASS** for copying the complete Skill, validator discovery, and evidence-helper startup with Pillow installed in the disposable project environment.
- Plugin and marketplace JSON manifests, changed Markdown relative links, and `git diff --check`: **PASS**.
- File-content privacy and high-confidence secret-pattern scan: **PASS**, 36 text files scanned; no non-example email or high-confidence secret pattern found.
- Browser behavior was not rerun because Playwright MCP is unavailable in this remediation environment. Existing browser validation remains recorded in `docs/VALIDATION.md`; no Skill or browser-helper behavior changed.

## Proposed Public Remote Operations

The affected public release and refs must be treated as privacy-defective. After explicit authorization, the proposed narrow operations are:

1. Withdraw/delete the GitHub Release for `v0.1.0` and delete the affected `v0.1.0` tag. Do not move that tag to a different commit.
2. Update only `main` and `develop` to the sanitized histories with lease-guarded force updates, requiring the currently observed old ref values. If a lease fails, stop and inspect the new remote state.
3. Fetch a fresh public clone and inspect all reachable author, committer, and tagger metadata. Do not restore old refs as a rollback because that would re-expose the address.
4. After remote verification and final regression, prepare `v0.1.1` as the first acceptable release. State that it supersedes the withdrawn `v0.1.0` due to Git metadata privacy remediation. No `v0.1.1` has been created.

This changes commit and tag object IDs. Anyone with an old clone must discard it or carefully clean it before contributing; pushing an old branch could reintroduce the affected history. No visible forks or pull requests were found, but external clones cannot be enumerated or rewritten by the repository owner.

## Backup, Rollback, and GitHub Support

Before any remote operation, the verified private bundle can restore the pre-remediation local refs if local recovery is needed. The sanitized repository can also be regenerated from that bundle. After a remote rewrite, restoring the bundle to public refs would re-expose the affected metadata and is not an automatic rollback; stop and obtain separate authorization instead.

GitHub's current [sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) says support may remove cached views and references after refs are cleaned, but limits help to data GitHub determines is sensitive and whose risk cannot be addressed by rotating credentials. A support request is **potentially applicable** for this personal-email exposure; approval and purge are not guaranteed. No support request has been submitted.

## Authorization Boundary

The public GitHub Release, public tag, and public branches remain unchanged and affected. No remote refs, release, or repository visibility have been modified in this remediation phase. Explicit user authorization is required before withdrawing the release, deleting the tag, or force-updating either branch.
