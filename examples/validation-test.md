# Validation behavior

```text
Use $prompt-ui-testing to test the Create Account form at http://127.0.0.1:5173.
Leave Email empty and submit the form.
Expected: a required-field message appears and no account is created.
Capture URL-visible evidence of the validation result.
```

The result should be based on what the UI actually shows. If the UI cannot establish whether an account was created, report that part as `INCONCLUSIVE`.
