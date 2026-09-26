# Optional project settings

The Skill works without a configuration file when the prompt supplies the target and test details. If a team wants reusable settings, copy the [generic YAML example](../skills/prompt-ui-testing/assets/project-config.example.yaml) into its own private project and adapt it there.

```text
Use $prompt-ui-testing with the configured Local environment.
Plan-only: describe how you would test the Create Account flow with Name = Sample User.
Do not execute browser actions.
```

No parser is required for the example YAML. The agent reads the supplied settings as context; it must still use the user's prompt and actual browser state for test decisions and evidence.
