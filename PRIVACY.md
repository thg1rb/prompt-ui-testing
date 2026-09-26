# Privacy

This project provides Agent Skill instructions and a small evidence helper. It does not run a hosted service, retain user records, collect telemetry, or send test data to the project maintainers.

## Information handled during a test

A user may ask an Agent to visit a target URL, enter test values, inspect page content, or choose a local file. These may include personal data if the user supplies it or the page displays it. The purposes are to perform the requested UI test, compare observed results with expectations, and create requested evidence. The Agent host and any configured browser capability, including a separately configured Playwright MCP provider, may process prompts, URLs, page text, screenshots, and test values. They are the recipients needed to perform the task; their additional recipients, collection, and retention are governed by those providers' own policies. This project does not control or verify those practices.

The Skill's evidence workflow can create a raw screenshot and a composed screenshot in the evidence directory selected for the test. The files remain in that local execution environment until the user deletes them; the helper does not impose a retention period or upload evidence. The user controls the evidence location, access, and deletion. The project maintainers do not receive copies by default.

## URL and screenshot handling

The evidence helper redacts URL user information, query values, fragments, and likely token-bearing path segments in the visible URL strip. It retains a raw screenshot and does not remove sensitive information already rendered in the page pixels. Both raw and composed images may therefore contain personal or confidential content.

## Choices and responsibilities

Use authorized targets and disposable test data. Avoid entering real credentials or personal data, and review screenshots before sharing them. Users can limit processing by choosing the target, inputs, host, and browser provider; they may omit evidence capture or delete local evidence files. A compatible browser capability, such as separately configured Playwright MCP, may receive page content and perform requested actions under its own provider's terms. Missing browser capability should result in an execution limitation, not a claimed test result.

This policy describes the project files' behavior; it does not replace the policies of the Agent host, browser provider, or target application.

## Contact

For questions about this project, use the public [GitHub Issues page](https://github.com/thg1rb/prompt-ui-testing/issues). Do not include credentials, private URLs, personal data, or sensitive screenshots in a public issue.
