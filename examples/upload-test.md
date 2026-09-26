# File upload

```text
Use $prompt-ui-testing to test document upload at https://example.com/documents.
Upload ./test-assets/sample.pdf.
Expected: sample.pdf appears in the document list.
Capture evidence after attaching and after the final result.
```

The file path is an example. The agent must verify that the supplied file exists and return `BLOCKED` if it does not.
