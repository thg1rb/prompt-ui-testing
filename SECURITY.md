# Security

Use this Skill only on targets and data for which you are authorized. An open browser session or accessible control does not itself grant permission for state-changing tests. Provide explicit intent before consequential production actions, and prefer disposable test data.

Browser actions can change application state, including when a test is not intended to be destructive. Treat delete, approval, rejection, account changes, and other irreversible actions as consequential. Do not run them on production-like or uncertain targets without explicit user intent. The Skill does not grant access or establish authorization. A separately configured browser or MCP provider has its own permissions and behavior.

Do not commit credentials, tokens, cookies, OTP values, browser profiles, private URLs, or screenshots of sensitive pages. Keep project configuration separate from the public Skill. Use a secure handoff for authentication and avoid screenshots during secret entry.

The evidence helper redacts URL credentials, query values, fragments, and likely secret path values in the metadata strip. It preserves the raw screenshot, which can itself contain confidential application data; store, share, and delete evidence according to the target's data policy. Redaction is not a substitute for reviewing the page image before sharing it.

If you find a vulnerability in the Skill or helper, report it privately through the repository host's security advisory mechanism once the project is published. Do not include live credentials or private target data in an issue.
