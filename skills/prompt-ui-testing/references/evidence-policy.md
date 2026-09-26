# Screenshot evidence and integrity

Capture at meaningful checkpoints: loaded page, completed input, attached file, before an important submission, result, failed validation, or unexpected error. Honor explicit screenshot requests. Avoid secret entry and irrelevant or duplicate images. Every **final** evidence screenshot must visibly show the active page URL; filenames and report text do not replace this requirement.

## Capture sequence

1. Query the active browser page URL.
2. Capture a raw page screenshot to a test-specific path.
3. Query the active URL again. If it changed, discard this checkpoint and retry after the page settles. A capture that cannot be associated with a stable URL is not final evidence.
4. Run `python scripts/compose_evidence.py --input <raw-image> --output <final-image>` and supply `{"url":"<active-browser-url>"}` as JSON on stdin. Use a safe structured stdin operation rather than interpolating a sensitive URL into shell text. Save the generated PNG separately and keep the raw image. The helper requires Pillow.
5. Inspect the final image for readable URL text and important content. If capture or composition fails, report the limitation and do not list a nonexistent file.

The helper uses the browser-provided URL, never the requested URL. It places a metadata strip above the application screenshot without changing its pixels. It redacts URL credentials, query values, and fragments. The host and path remain visible; path segments after secret-bearing labels are redacted. A page that itself displays secrets should not be screenshotted until the secret is hidden or a safe state is reached.

Use a neutral directory and ordered names, for example `TEST-001/01-page-loaded.raw.png` and `TEST-001/01-page-loaded.png`. Never reuse evidence from a different test or earlier state. Report only files that were actually produced. The report may additionally list the redacted URL shown in each final screenshot.
