# Prompt Summary

Use the `multi-agent-router` skill as the canonical routing layer.

Before substantive work:

1. Choose `solo`, `single_delegate`, or `multi_agent`.
2. Prefer one strong specialist over multiple agents when one agent can own the task cleanly.
3. Use multi-agent execution only for independent workstreams, distinct review dimensions, or parallel discovery and validation.
4. Keep the parent thread responsible for requirements, constraints, decisions, acceptance criteria, and final synthesis.
5. If you delegate, say why delegation is better than staying solo.
6. If you stay solo despite strong specialist pressure, say why subagents are not better here.
7. If no strong specialist exists but delegation still helps, fall back to `default`, `explorer`, or `worker`.

Treat this summary as derivative of `skills/multi-agent-router/SKILL.md` and `skills/multi-agent-router/router.yaml`.
