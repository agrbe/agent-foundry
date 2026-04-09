# Prompt Summary

Use the `multi-agent-router` skill as the canonical routing layer.

Before substantive work:

1. Choose `solo`, `single_delegate`, or `multi_agent`.
2. If one curated specialist cleanly matches the task, delegate to that specialist by default.
3. Use multi-agent execution only for independent workstreams, distinct review dimensions, or parallel discovery and validation.
4. Keep the parent thread responsible for requirements, constraints, decisions, acceptance criteria, and final synthesis.
5. If you delegate, say why delegation is better than staying solo.
6. If you stay solo despite a matching specialist, say exactly why delegation is not possible or not useful yet.
7. Only fall back to `default`, `explorer`, or `worker` when no curated specialist matches the task requirements.

Treat this summary as derivative of `skills/multi-agent-router/SKILL.md` and `skills/multi-agent-router/router.yaml`.
