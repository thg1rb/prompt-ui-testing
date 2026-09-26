# Authentication

Start each independent test in a fresh isolated browser session by default. Do not inherit cookies or local/session storage from an earlier case. When authentication is required, log in as part of that case using credentials supplied through a secure environment, or use explicitly supplied storage state when the user requests and the browser capability supports it. Reuse of a persistent profile or authenticated session is an explicit deviation from the default and must be disclosed. Never place credentials, tokens, cookies, storage state, or OTP secrets in the public Skill, examples, reports, or repository.

Ask the user for a secure handoff when authentication is required and unavailable. Report `BLOCKED` if the handoff cannot be completed. Do not bypass authentication or use credentials from unrelated contexts.

Avoid screenshots of password or OTP entry, URL tokens, and personal data. If a browser tool exposes secrets in outputs, do not repeat them in the report. Treat profile and session reuse as sensitive and use only the session authorized for the target test.
