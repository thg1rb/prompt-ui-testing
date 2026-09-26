# Task: Build a Public Prompt-Driven UI Testing Agent Skill

Design and implement a production-quality, reusable, open-source **Agent Skill for prompt-driven black-box UI testing of web applications**.

The Skill must allow users to test web applications primarily through natural-language prompts.

The target application may be:

- a remotely deployed web application
- a development environment
- a testing environment
- a staging environment
- a sandbox environment
- a production environment, subject to additional safety controls
- a web application running locally on the user's machine

Examples:

```text
https://example.com
https://test.example.com
https://staging.example.com

http://localhost:3000
http://localhost:5173
http://127.0.0.1:3000
http://127.0.0.1:8080
```

Testing locally running applications MUST be a first-class supported use case.

The user should NOT need to:

- modify the application under test
- add test files to the application's repository
- write Playwright test specifications
- write CSS selectors
- write XPath selectors
- write browser automation code
- know the implementation details of the target application

The target application must be treated as a **black-box system accessible through its User Interface**.

---

# 1. Privacy and Public-Repository Requirement

This Skill is intended to be reusable and potentially published publicly.

Therefore:

DO NOT include, infer, copy, or reuse any:

- real company names
- organization names
- private project names
- internal system names
- internal URLs
- private API endpoints
- real usernames
- real email addresses
- real transaction identifiers
- real Test Case IDs
- internal naming conventions
- proprietary terminology
- confidential screenshots
- credentials
- secrets
- tokens
- organization-specific workflows

This rule applies to:

- source code
- README files
- documentation
- examples
- sample prompts
- configuration templates
- screenshots
- test fixtures
- comments
- commit-ready files

Use only neutral fictional examples.

Preferred placeholder conventions:

```text
https://example.com
https://test.example.com
http://localhost:3000

TEST-001
TEST-002

Sample User
Test Account
Example Document
```

Generic feature names are acceptable, for example:

```text
Login
Create Account
Profile
Search Records
Document Upload
Settings
Dashboard
```

Never derive examples from private conversation history or an existing organization's internal systems.

---

# 2. Primary Goal

Build a reusable Skill that performs:

```text
Natural Language Prompt
        ↓
Test Understanding
        ↓
Test Planning
        ↓
Browser Interaction
        ↓
UI Validation
        ↓
Evidence Collection
        ↓
PASS / FAIL / BLOCKED / INCONCLUSIVE
        ↓
Test Report
```

The preferred browser automation backend is **Playwright MCP** or another compatible browser automation capability when appropriate.

The Skill defines:

- testing workflow
- validation rules
- evidence rules
- safety rules
- reporting conventions

The browser automation backend performs:

- navigation
- click
- typing
- selection
- upload
- UI inspection
- screenshot capture

---

# 3. Core Principles

The Skill must follow these principles:

```text
Prompt-Driven
Black-Box Testing
No Target Application Modification
Remote + Localhost Support
Semantic Browser Interaction
Evidence-First Testing
Expected vs Actual Validation
Secure by Default
Reusable Across Projects
Public-Safe Documentation
```

---

# 4. Distribution Requirements

Design the Skill so that it can be used as:

1. a reusable public Agent Skill
2. a Project-installed Skill
3. a User/Global-installed Skill where supported
4. a Plugin package where supported and appropriate

Before implementing installation paths, manifests, or package structure:

research the current official documentation for:

- Agent Skills
- Codex Skills
- Project Skills
- User/Global Skills
- OpenAI Plugins
- MCP configuration
- Playwright MCP

Do not rely on outdated installation conventions.

The core Skill should remain portable even when an OpenAI-specific Plugin wrapper is not used.

---

# 5. Suggested Repository Structure

Use a structure similar to:

```text
prompt-ui-tester/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
│
├── skills/
│   └── prompt-ui-testing/
│       ├── SKILL.md
│       │
│       ├── references/
│       │   ├── testing-policy.md
│       │   ├── evidence-policy.md
│       │   ├── validation-policy.md
│       │   ├── browser-strategy.md
│       │   ├── authentication.md
│       │   ├── localhost.md
│       │   └── safety.md
│       │
│       ├── assets/
│       │   ├── report-template.md
│       │   └── project-config.example.yaml
│       │
│       └── scripts/
│           └── ...
│
└── examples/
    ├── basic-test.md
    ├── localhost-test.md
    ├── form-test.md
    ├── upload-test.md
    ├── validation-test.md
    └── project-configuration.md
```

If current standards recommend a different structure, follow the current official standard and document the reason.

---

# 6. Skill Activation

Create a `SKILL.md` whose description allows the Agent to recognize requests such as:

- test this website
- test this UI
- test this deployed application
- test my localhost application
- verify this user flow
- run this UI test
- fill this form and verify the result
- test document upload
- test form validation
- perform browser-based regression testing
- capture test evidence
- verify expected behavior through the UI

It SHOULD NOT automatically activate for:

- unit testing
- API-only testing
- source-code review
- static analysis
- writing Jest tests
- writing Playwright `.spec.ts` files
- ordinary browsing unrelated to testing

---

# 7. Prompt-First User Experience

The primary interface is natural language.

Example:

```text
Test the Create Account flow at:

https://test.example.com

Input:
Name = Sample User
Email = sample@example.com

Expected:
The account is created successfully.

Capture screenshots before submitting and after the result.
```

Local application example:

```text
Test the Create Account flow at:

http://localhost:3000

Input:
Name = Sample User
Email = sample@example.com

Expected:
The account is created successfully.

Capture screenshots before submitting and after the result.
```

The same testing workflow should work for both.

The user should not need to specify browser selectors or automation instructions.

---

# 8. Planning Phase

Before execution, internally derive a Test Plan.

Example:

```text
Goal:
Create an account

Target:
http://localhost:3000

Actions:
1. Open the target application
2. Navigate to Create Account
3. Enter Name
4. Enter Email
5. Capture evidence
6. Submit the form
7. Wait for a meaningful result
8. Validate the expected result
9. Capture final evidence

Expected:
Account creation succeeds
```

Do not require the user to manually provide this structure.

If the user provides explicit test steps, preserve their intent.

---

# 9. Browser Interaction Strategy

Prefer semantic browser interaction.

Use this priority where possible:

```text
Accessible Role + Name
        ↓
Associated Label
        ↓
Visible Text
        ↓
Placeholder
        ↓
Stable DOM Attribute
        ↓
Visual Understanding
        ↓
Coordinates as Last Resort
```

Avoid brittle selectors when unnecessary.

Do not depend primarily on screen coordinates.

---

# 10. Adaptive UI Understanding

Allow reasonable semantic adaptation.

Example instruction:

```text
Open Settings
```

The application may display:

```text
Preferences
```

If context clearly indicates equivalence, the Agent may adapt.

However, never guess when multiple consequential actions are equally plausible.

---

# 11. Supported UI Controls

Support common browser controls such as:

- text inputs
- textareas
- number inputs
- password fields
- checkboxes
- radio buttons
- dropdowns
- selects
- autocomplete fields
- comboboxes
- date pickers
- time pickers
- date-time pickers
- modals
- dialogs
- tabs
- tables
- pagination
- file inputs
- file chooser dialogs
- drag-and-drop upload where supported

---

# 12. File Upload

File upload must be a first-class capability.

Example:

```text
Test document upload at:

https://example.com/documents

Upload:
./test-assets/sample.pdf

Expected:
sample.pdf appears in the document list.
```

Multiple files:

```text
Attach:
- ./test-assets/image-1.jpg
- ./test-assets/image-2.jpg
```

The Agent should:

1. locate the appropriate upload control
2. attach the requested file
3. verify that the UI acknowledges the file
4. capture evidence when appropriate

Never invent missing files.

If a requested file is unavailable, return an appropriate blocked result.

---

# 13. Screenshot Evidence — Mandatory URL Visibility

Every test evidence screenshot MUST visibly show the **actual current URL** of the page being tested.

This is a mandatory requirement.

It applies to:

```text
https://example.com
https://test.example.com
http://localhost:3000
http://127.0.0.1:5173
```

A reviewer must be able to identify the tested environment and page by looking at the screenshot itself.

Do not rely only on:

- filenames
- folders
- external reports
- surrounding text

to communicate the URL.

---

# 14. URL Evidence Strategy

A normal page screenshot may not include browser chrome or the address bar.

Therefore implement a reliable evidence strategy.

Preferred flow:

```text
Get actual current browser URL
        +
Capture raw page screenshot
        ↓
Evidence Composer
        ↓
Final evidence screenshot
with visible URL metadata
```

Example:

```text
┌──────────────────────────────────────────────┐
│ URL: http://localhost:3000/create-account    │
├──────────────────────────────────────────────┤
│                                              │
│          Actual Application Screenshot       │
│                                              │
└──────────────────────────────────────────────┘
```

Requirements:

- obtain the URL from the active browser page
- never fabricate the URL
- never assume that the original navigation URL is still current
- update the URL after redirects
- update the URL after SPA navigation
- ensure URL text is clearly readable
- keep the URL outside important application content
- preserve the original screenshot
- do not alter the application under test

If browser chrome can be captured reliably and clearly shows the current URL, that may satisfy the requirement.

Otherwise use the evidence composition approach.

---

# 15. Screenshot Evidence Policy

Capture evidence at meaningful checkpoints.

Typical screenshots may include:

```text
01-page-loaded.png
02-form-filled.png
03-file-attached.png
04-before-submit.png
05-result.png
```

Every evidence screenshot must include the current URL.

Capture evidence when:

- explicitly requested
- a relevant page has loaded
- important input has been completed
- a file has been attached
- before an important state-changing action
- after submission
- an expected result appears
- validation fails
- an unexpected error occurs

Avoid unnecessary screenshots of secret entry.

---

# 16. Evidence Integrity

Evidence must reflect actual execution.

The Agent MUST NOT:

- fabricate screenshots
- fabricate URLs
- reuse screenshots from another test
- reuse stale screenshots from a previous state
- modify application content in an evidence image
- claim a screenshot exists when it does not
- label a screenshot with the requested URL when the actual browser is somewhere else

An evidence metadata strip may contain:

```text
URL
Timestamp
Test ID
```

URL is mandatory.

Timestamp and Test ID are optional.

Generic Test ID example:

```text
TEST-001
```

---

# 17. Sensitive URL Handling

URLs may sometimes contain sensitive query parameters.

Example:

```text
https://example.com/callback?token=secret-value
```

The Skill must define safe URL redaction.

Example evidence display:

```text
URL: https://example.com/callback?token=[REDACTED]
```

Redaction must:

- preserve the tested host and relevant path
- indicate that content was redacted
- never expose authentication secrets
- never replace the URL with an unrelated value

---

# 18. Expected vs Actual Validation

A test MUST NOT pass just because browser steps completed.

Compare:

```text
Expected Result
        VS
Observed Actual Result
```

Supported statuses:

```text
PASS
FAIL
BLOCKED
INCONCLUSIVE
```

### PASS

Observed UI behavior satisfies the stated expected result.

### FAIL

Observed UI behavior contradicts the expected result.

### BLOCKED

Execution cannot proceed because of an external prerequisite or environment issue.

Examples:

```text
Target application unreachable
Local server not running
Authentication unavailable
Required file missing
Required permission unavailable
```

### INCONCLUSIVE

There is insufficient observable evidence to decide whether the expectation was satisfied.

Never force a PASS or FAIL when evidence is insufficient.

---

# 19. Never Invent Results

The Agent MUST NEVER:

- claim an element was clicked when it was not
- claim a value appeared when it was not observed
- claim a file uploaded when it did not
- claim success based solely on expectation
- fabricate an error message
- fabricate application output
- fabricate evidence
- infer backend success without observable UI evidence

All reported results must come from observed execution.

---

# 20. Reporting

Generate a concise result such as:

```text
Test: Create Account

Environment:
http://localhost:3000

Result:
PASS

Input
- Name: Sample User
- Email: sample@example.com

Expected
- Account creation succeeds

Actual
- Success message appeared
- The new account page was displayed

Evidence
- 01-form-filled.png
- 02-before-submit.png
- 03-result.png
```

Failure example:

```text
Test: Search Records

Result:
FAIL

Expected
- Matching record appears in the results

Actual
- No matching record was displayed

Failure Point
- Search results

Evidence
- 03-search-result.png
```

Do not include private or organization-specific naming conventions in templates.

---

# 21. Step-Level Reporting

When useful:

```text
Step 1 — PASS — Open page
Step 2 — PASS — Enter form data
Step 3 — PASS — Submit
Step 4 — FAIL — Expected confirmation message not found
```

Keep small tests concise.

---

# 22. Authentication

Support common authentication approaches:

- username/password
- existing authenticated browser session
- browser profile reuse
- cookies/session reuse
- SSO
- manual login handoff
- MFA/OTP handoff

Never store credentials inside the public Skill.

Never commit:

- usernames
- passwords
- API keys
- access tokens
- session cookies
- OTP secrets

Use generic environment variable examples such as:

```text
TEST_BASE_URL
TEST_USERNAME
TEST_PASSWORD
```

Do not expose secret values in screenshots or reports.

---

# 23. Optional Project Configuration

The public Skill should work without project-specific configuration when the prompt contains enough information.

Optional configuration example:

```yaml
environment:
  name: Local
  base_url: http://localhost:3000

authentication:
  strategy: existing-session

evidence:
  screenshots: meaningful-steps
  show_url: true

testing:
  destructive_actions: confirm
```

Remote example:

```yaml
environment:
  name: Test
  base_url: https://test.example.com

authentication:
  strategy: existing-session

evidence:
  screenshots: meaningful-steps
  show_url: true

testing:
  destructive_actions: confirm
```

Project configuration must remain separate from the reusable public Skill.

---

# 24. Localhost Support

Local applications are first-class targets.

Support:

```text
http://localhost:3000
http://localhost:5173
http://127.0.0.1:3000
http://127.0.0.1:8080
```

Before testing, determine whether the browser automation environment can reach the target.

Possible outcomes:

### Reachable

Proceed with testing.

### Local server not running

Return:

```text
BLOCKED

Reason:
The target application is not reachable at http://localhost:3000
```

### Tool Environment Cannot Reach User Localhost

Clearly report that the automation/browser environment cannot reach the user's local server.

Do not incorrectly report that the web application itself is broken.

---

# 25. State-Changing Actions

Testing may create or modify data.

Examples:

```text
Create
Update
Delete
Submit
Approve
Reject
Cancel
Account Modification
```

For environments explicitly identified as:

```text
localhost
development
dev
test
testing
staging
sandbox
```

requested test actions may proceed subject to normal safety checks.

For production-like environments, apply stricter confirmation rules before consequential actions.

Never infer authorization merely because the browser can access the page.

---

# 26. Production Protection

Detect signs that the target may be production.

Be conservative with:

- destructive changes
- irreversible changes
- user-account modifications
- data deletion
- financially meaningful actions

Read-only verification can proceed when appropriate.

For consequential actions in an uncertain environment, require explicit user intent.

---

# 27. Sensitive Data

Avoid exposing:

- passwords
- tokens
- authentication codes
- personal identifiers
- confidential data

Do not capture screenshots while entering secrets unless explicitly necessary and safe.

Collect the minimum evidence required.

---

# 28. Error Recovery

Handle normal automation problems intelligently.

Examples:

### Element not ready

Wait and retry within reasonable bounds.

### Loading state

Wait for meaningful UI readiness.

### Modal blocking interaction

Inspect and handle it.

### Minor UI change

Re-evaluate semantically.

### Element genuinely missing

Capture evidence and report the appropriate result.

Never retry indefinitely.

---

# 29. Dynamic Applications

Support:

- SPA navigation
- asynchronous rendering
- delayed responses
- lazy loading
- toast messages
- overlays
- skeleton states
- redirects
- localhost hot reload

Prefer observable UI conditions over arbitrary fixed delays.

---

# 30. Visual Validation

Screenshots are supporting evidence.

Do not claim pixel-perfect visual correctness unless explicit visual-comparison capability exists.

The Skill may validate observable states such as:

```text
Error message visible
Button disabled
Modal visible
Table row exists
Confirmation text appears
Navigation succeeded
```

Keep semantic validation distinct from visual regression testing.

---

# 31. Multiple Tests

When multiple tests are requested:

- keep test cases separated
- isolate evidence
- report each result independently
- identify dependencies
- avoid accidental state leakage when possible

Example generic IDs:

```text
TEST-001
TEST-002
TEST-003
```

---

# 32. Exploratory Mode

Support optional exploratory testing.

Example:

```text
Explore the Create Account form and test obvious validation edge cases.
```

Clearly distinguish:

```text
User-Specified Tests
```

from:

```text
Agent-Generated Exploratory Tests
```

Do not claim exploratory tests came from formal requirements.

---

# 33. Plan-Only Mode

Support:

```text
Plan how you would test this flow, but do not execute anything.
```

Generate a plan without performing state-changing actions.

---

# 34. Dry-Run Mode

Support:

```text
Dry-run this test.
```

Dry-run should:

- parse the prompt
- identify target URL
- create planned steps
- identify required files
- identify authentication needs
- identify consequential actions
- avoid executing the test

---

# 35. Evidence Naming

Use neutral predictable naming.

Example:

```text
TEST-001/
  01-initial-state.png
  02-form-filled.png
  03-before-submit.png
  04-result.png
```

If no Test ID exists, generate a neutral slug.

Never use organization-specific ID conventions in public examples.

---

# 36. Screenshot Helper

If the browser tool cannot capture an address bar, implement a deterministic evidence helper.

Concept:

```text
Actual Page URL
      +
Raw Screenshot
      ↓
Evidence Composer
      ↓
Screenshot with Visible URL
```

The helper must:

- receive the actual URL from the browser
- receive the raw screenshot
- create a dedicated URL strip
- preserve original page pixels
- avoid covering important content
- save the final evidence file

Prefer deterministic code rather than LLM-based image manipulation.

Place helper code under the Skill's `scripts/` directory when appropriate.

---

# 37. Report Template

Provide a reusable report template containing:

```text
Test Name
Environment
Result
Inputs
Expected Result
Actual Result
Step Summary
Evidence
Failure Point
Notes
```

Only include useful sections.

Evidence may additionally show:

```text
01-form-filled.png
URL: http://localhost:3000/create-account

02-result.png
URL: http://localhost:3000/account-created
```

---

# 38. Tool Availability

Prefer Playwright MCP when available.

If unavailable:

1. inspect available browser/computer-use tools
2. determine whether they can execute the requested test reliably
3. ensure mandatory URL-visible screenshots can still be produced
4. clearly communicate limitations

Never claim testing was performed without a compatible execution tool.

---

# 39. Playwright MCP

Document the architecture clearly:

```text
Agent Skill
  → Test reasoning and policy

Playwright MCP
  → Browser control

Evidence Helper
  → URL-visible screenshots
```

Do not unnecessarily reimplement the browser automation engine.

Validate MCP configuration against current official documentation.

---

# 40. Installation

Research and document current supported installation methods for:

### Project Installation

Skill available only within one project.

### User / Global Installation

Skill available across projects where the host supports this installation model.

### Plugin Installation

Package through the current Plugin mechanism when supported.

Do not invent installation commands.

Verify commands and paths against official documentation.

---

# 41. Public Distribution

Prepare the Skill for public open-source distribution.

Include:

- README
- LICENSE
- CHANGELOG
- CONTRIBUTING
- SECURITY
- installation instructions
- architecture explanation
- example prompts
- localhost instructions
- evidence behavior
- troubleshooting
- limitations
- contribution instructions
- versioning strategy

All documentation and examples must use fictional generic data only.

---

# 42. README Examples

## Basic

```text
Test the login flow at:

https://example.com

Use my configured test account.

Expected:
The dashboard appears after successful login.

Capture evidence.
```

## Localhost

```text
Test the application running at:

http://localhost:3000

Open the login page.

Use my configured development test account.

Expected:
The dashboard appears.

Capture screenshots of the login page and dashboard.

Every screenshot must visibly show the current URL.
```

## Form

```text
Open:

https://example.com/profile

Change the display name to:

Sample User

Save the form.

Expected:
A success message appears and the updated value is displayed.
```

## File Upload

```text
Test document upload at:

https://example.com/documents

Upload:

./test-assets/sample.pdf

Expected:
sample.pdf appears in the uploaded-document list.

Capture evidence before and after upload.
```

## Validation

```text
Test the Create Account form.

Leave the Email field empty.

Submit the form.

Expected:
A required-field validation message appears.

Do not create an account.
```

## Localhost Form Test

```text
Test the Create Account page at:

http://127.0.0.1:5173

Input:
Name = Sample User
Email = sample@example.com

Expected:
The account is created successfully.

Capture evidence before and after submission.

Every evidence screenshot must visibly show the current URL.
```

---

# 43. Multilingual Prompts

The Skill must support natural-language instructions in languages other than English.

Do not require English prompts.

Do not blindly translate UI labels.

Use semantic browser context to correlate the user's instruction with the actual UI.

Reports should follow the user's language where practical.

---

# 44. Skill Design

Keep `SKILL.md` concise.

It should contain:

- activation rules
- core workflow
- browser strategy
- localhost support
- critical safety rules
- evidence requirements
- mandatory URL screenshot rule
- output rules
- references to detailed documents

Use:

```text
references/
```

for detailed policies.

Use:

```text
assets/
```

for templates.

Use:

```text
scripts/
```

for deterministic helpers.

---

# 45. Do Not Over-Engineer Version 1

Version 1 should focus on:

```text
Prompt
  ↓
Browser
  ↓
Execute
  ↓
Validate
  ↓
Screenshot + URL
  ↓
Report
```

Do NOT initially build:

- custom dashboards
- databases
- full test-management systems
- proprietary browser engines
- complex multi-agent orchestration
- CI platforms

Prove the basic prompt-driven workflow first.

---

# 46. Test Matrix for the Skill

Validate at least:

1. Remote URL navigation
2. localhost navigation
3. 127.0.0.1 navigation
4. unreachable localhost
5. login
6. text input
7. dropdown
8. checkbox
9. date/time
10. file upload
11. modal
12. redirect
13. SPA navigation
14. expected success
15. expected failure
16. missing element
17. missing file
18. authentication failure
19. dynamic loading
20. multilingual UI
21. production guardrail
22. multiple tests
23. dry-run
24. plan-only
25. Skill non-trigger cases
26. screenshot URL correctness
27. redirected screenshot URL correctness
28. SPA URL correctness
29. sensitive URL redaction
30. URL visible on every evidence screenshot

---

# 47. Screenshot Acceptance Criteria

Screenshot functionality is complete only when:

- [ ] Every evidence image visibly shows its current URL.
- [ ] URL is readable.
- [ ] URL comes from the actual active browser page.
- [ ] Redirects produce the correct new URL.
- [ ] SPA navigation produces the correct current URL.
- [ ] localhost URLs work.
- [ ] 127.0.0.1 URLs work.
- [ ] sensitive URL components can be redacted safely.
- [ ] application content is not altered.
- [ ] URL metadata does not obscure important application content.

---

# 48. Overall Acceptance Criteria

Implementation is complete when:

- [ ] A valid reusable Agent Skill exists.
- [ ] `SKILL.md` follows current standards.
- [ ] Skill activation rules are clear.
- [ ] Natural-language UI testing works conceptually.
- [ ] Remote applications are supported.
- [ ] localhost applications are supported.
- [ ] 127.0.0.1 applications are supported.
- [ ] Target application source code is not modified.
- [ ] End users do not need Playwright test files.
- [ ] Form interaction is supported.
- [ ] File upload is supported.
- [ ] Screenshot evidence is supported.
- [ ] Every evidence screenshot visibly shows its URL.
- [ ] Expected vs Actual validation exists.
- [ ] PASS / FAIL / BLOCKED / INCONCLUSIVE are supported.
- [ ] Authentication guidance is secure.
- [ ] Production protection exists.
- [ ] Project configuration is separated from the public Skill.
- [ ] Project installation is documented.
- [ ] User/Global installation is documented where supported.
- [ ] Plugin distribution is documented where supported.
- [ ] README uses fictional generic examples only.
- [ ] No organization-specific or private information exists anywhere in the repository.
- [ ] Repository is suitable for public open-source publication.

---

# 49. Development Process

Follow this sequence.

## Phase 1 — Research

Research current official documentation for:

- Agent Skills
- Codex Skills
- `SKILL.md`
- Project Skill installation
- User/Global Skill installation
- OpenAI Plugins
- MCP configuration
- Playwright MCP
- screenshot capabilities
- browser URL retrieval
- localhost networking limitations

Prefer current first-party sources.

## Phase 2 — Privacy Review

Before implementation:

inspect all proposed examples and configuration.

Confirm that they contain only:

- fictional names
- generic Test IDs
- example.com
- localhost
- generic feature terminology

Reject any private or organization-derived example.

## Phase 3 — Design

Propose:

- 3 public-friendly Skill names
- final Skill name
- description
- architecture
- repository structure
- dependency model
- evidence strategy
- localhost strategy
- security model
- configuration model

## Phase 4 — Implement

Create the complete repository implementation.

Do not stop at an outline.

## Phase 5 — Validate

Validate:

- Skill format
- manifests
- links
- configuration
- screenshot URL behavior
- localhost support
- evidence integrity
- safety rules
- privacy/publication readiness

## Phase 6 — Privacy Audit

Before finishing, search the entire repository for:

- real domains
- organization names
- private URLs
- credentials
- internal identifiers
- proprietary terminology
- accidental private examples

Replace anything found with neutral fictional placeholders.

## Phase 7 — Dogfood

Test representative generic scenarios against:

```text
https://example.com
```

or another appropriate disposable public/local test application, and:

```text
http://localhost:<port>
```

where available.

Do not use private organization systems for public repository examples.

## Phase 8 — Documentation

Complete:

- README
- installation
- architecture
- usage examples
- localhost usage
- evidence handling
- screenshot URL behavior
- security
- troubleshooting
- contribution guide

---

# 50. Final Deliverable

When complete, report:

1. selected Skill name
2. what the Skill does
3. repository structure
4. architecture decisions
5. Playwright MCP integration
6. localhost support
7. screenshot URL implementation
8. Project installation
9. User/Global installation
10. Plugin/public distribution
11. generic example prompts
12. security considerations
13. privacy/publication audit results
14. known limitations
15. validation performed
16. recommended next iteration

Do not merely describe the implementation.

Create the complete Skill in the current repository.

Before declaring completion, explicitly confirm:

> The repository was reviewed for public release and contains no private, organization-specific, project-specific, credential, internal URL, or proprietary example data.
