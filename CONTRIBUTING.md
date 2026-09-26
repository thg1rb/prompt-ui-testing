# Contributing

Contributions should improve prompt-driven, black-box browser testing without requiring changes to the application under test. Keep `SKILL.md` short and place conditional guidance in relevant references. Add scripts only for operations that benefit from deterministic code.

Use fictional data in every example and fixture. Do not submit credentials, session state, private URLs, confidential screenshots, real account details, internal IDs, or organization-specific terminology. Public examples should use `example.com`, loopback addresses, and neutral names such as `Sample User` and `TEST-001`.

For evidence-helper changes, install `requirements.txt` and run:

```sh
python3 -m unittest discover -s tests -v
```

Check that raw screenshot pixels remain intact in the composed image, sensitive URL parts are redacted, and the active URL is readable. For Skill policy changes, walk through a representative prompt and confirm the expected status, safety decision, and evidence behavior. See [docs/PLAN.md](docs/PLAN.md) for the full validation phases.
