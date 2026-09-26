# Git Metadata Privacy Remediation

**Status: remote history remediation complete; `v0.1.1` recovery release in progress.** This record omits the exposed email and old commit hashes.

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
- Immediately after rewriting, before adding this remediation record and metadata check, local sanitized refs were `main` at `72eddaead857d2228c55b4697972388890b5d5ee`, `develop` at `41339844dbfc01fd444c653da1545fb19cb01816`, and a temporary local `v0.1.0` tag at `4d0bb85e0969b72190d68c9dc411790798ebb962`. That local tag was later deleted to prevent accidental reuse.
- The public `v0.1.0` Release was deleted and its lookup now returns 404. The remote `v0.1.0` tag was deleted and is absent from `ls-remote`; its local sanitized counterpart was also deleted.
- `main` and `develop` were updated with exact lease-guarded pushes to the sanitized history. Both branch-protection checks reported no protection. No other remote refs were updated.
- At the history-update checkpoint, the remote had `main` at `e2e9c65a78ccd0b3d496117eb56f0c2539cd7d02`, `develop` at `41339844dbfc01fd444c653da1545fb19cb01816`, and no tags. The repository default branch remains `main`; the recovery release commit will advance `main` after these checks.

## Regression Results

- Skill validator: **PASS**.
- Helper and metadata-check tests: **PASS**, all 11 tests. Tests confirm that author, committer, and annotated tagger email violations fail without printing the address.
- Reachable metadata scan on the sanitized working tree: **PASS**, six commits and zero annotated tag objects after local `v0.1.0` removal.
- Clean project install smoke: **PASS** for copying the complete Skill, validator discovery, and evidence-helper startup with Pillow installed in the disposable project environment.
- Plugin and marketplace JSON manifests, changed Markdown relative links, and `git diff --check`: **PASS**.
- Fresh public clone: **PASS**. Both branches were present, no tags were present, the metadata guard passed, and 36 text files had no non-example email or high-confidence secret pattern.
- The five old commit API lookups returned “No commit found for SHA”; the five direct commit pages returned 404. This indicates the old commits are not available through those public GitHub views now; it does not prove all caches or external copies are erased.
- Browser behavior was not rerun because Playwright MCP is unavailable in this remediation environment. Existing browser validation remains recorded in `docs/VALIDATION.md`; no Skill or browser-helper behavior changed.

## Public Remote Verification

The authorized narrow remote operations completed:

1. The `v0.1.0` GitHub Release was deleted and verified absent.
2. The affected remote `v0.1.0` tag was deleted with a lease and verified absent. The tag was not moved or recreated.
3. Only `main` and `develop` were force-updated with leases against the recorded old objects. Both updates were immediately verified; the branches now point to sanitized targets.
4. A fresh public clone contained both sanitized branches and no tags. The privacy guard and file-content scans passed.

The public repository showed no visible forks or pull requests when checked. Old commit API lookups returned no commit and direct pages returned 404. External clones, forks created later, or unobserved caches cannot be enumerated or rewritten by the repository owner. Anyone with a pre-remediation clone under maintainer control should re-clone from the sanitized repository; never merge or push a pre-remediation branch.

## Backup, Rollback, and GitHub Support

The verified private bundle can restore the pre-remediation local refs if local recovery is needed. The sanitized repository can also be regenerated from that bundle. Restoring the bundle to public refs would re-expose the affected metadata and is not an acceptable rollback.

GitHub's current [sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) says support may remove cached views and references after refs are cleaned, but only for data GitHub determines is sensitive and whose risk cannot be addressed by rotating credentials. A support request is **potentially applicable** for this personal-email exposure; approval and purge are not guaranteed. No request was submitted, and this task did not contact third parties.

## Recovery Release

`v0.1.0` is withdrawn. `v0.1.1` is being prepared as the first acceptable public release with the same initial Skill functionality and sanitized Git metadata. The release commit, tag, GitHub Release, fresh installation, and post-release validation will be recorded here after completion. Plugin publication remains paused until the replacement release passes fresh-install validation; Plugin publication is outside this task.
