# Authentication

Use an existing authorized browser session when supplied. Other supported routes include an explicitly provided username/password through a secure environment, browser profile or cookie/session reuse where authorized, and manual handoff for SSO or MFA/OTP. Never place credentials, tokens, cookies, or OTP secrets in the public Skill, examples, reports, or repository.

Ask the user for a secure handoff when authentication is required and unavailable. Report `BLOCKED` if the handoff cannot be completed. Do not bypass authentication or use credentials from unrelated contexts.

Avoid screenshots of password or OTP entry, URL tokens, and personal data. If a browser tool exposes secrets in outputs, do not repeat them in the report. Treat profile and session reuse as sensitive and use only the session authorized for the target test.
