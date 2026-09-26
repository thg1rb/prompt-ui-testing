# Localhost and local development

Treat `http://localhost:<port>` and `http://127.0.0.1:<port>` as normal test targets. Do not assume the agent process and browser process share a network namespace. Check reachability **from the browser environment** before classifying a local target.

- If reachable, continue with the same workflow as a remote URL.
- If the local server is stopped or refuses the connection in a browser on the user's machine, report `BLOCKED` with the tested URL and ask the user to start or expose the server.
- If the browser runs remotely or in a container and cannot reach the user's loopback address, report `BLOCKED` as a connectivity topology issue. Do not say the application itself is broken. Use a user-provided accessible endpoint or documented host bridge when available; never silently rewrite the target URL.

Local hot reload may replace the page during a test. Reinspect after reload and recapture the active URL. Do not claim evidence from a page that changed during screenshot capture.
