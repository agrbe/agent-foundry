---
name: multi-agent-router
description: Decide whether a user task should stay in the main Codex thread, be delegated to one specialist, or be split across multiple subagents. Use when Codex needs to classify work before substantive execution, choose between solo and delegated execution, prefer a strong specialist whenever it materially improves the outcome, or keep the parent thread focused on requirements, decisions, and final synthesis while subagents handle bounded work.
---

# Multi-Agent Router

## Overview

Route work before doing substantive execution. This skill is the canonical control surface for task routing in this repository. Use it to decide whether the task should run as `solo`, `single_delegate`, or `multi_agent`, then choose the narrowest strong specialist that improves execution without fragmenting the main thread.

Keep the parent thread responsible for:
- requirements
- constraints
- acceptance criteria
- key decisions
- final synthesis

Treat any prompt summary or prose-only document as derivative guidance, not the source of truth.

## Workflow

1. Load `router.yaml` before substantial work.
   Use it as the authoritative routing configuration for modes, policies, built-in fallbacks, categories, and curated specialist routes.

2. Normalize the task.
   Identify:
   - primary deliverable
   - likely work mode
   - technical domain
   - uncertainty level
   - verification load
   - coordination risk

3. Choose an execution mode.
   - `solo`: keep the work in the main thread when delegation would mostly duplicate context gathering.
   - `single_delegate`: prefer one strong specialist when one agent cleanly owns the task.
   - `multi_agent`: use multiple specialists only when there are independent review dimensions, separable ownership, or parallel discovery and validation work.

4. Prefer a strong specialist over a generic role.
   Read the relevant category or `agent_routes` entry in `router.yaml`.
   If a curated specialist materially improves execution, use it.
   If no strong specialist match exists but delegation still helps, fall back to `default`, `explorer`, or `worker` according to the built-in fallback rules.

5. Keep the critical path local.
   Do not delegate the immediate blocking step if the parent thread needs that answer before it can continue. Delegate bounded sidecar work and non-overlapping specialist work instead.

6. Set explicit delegate boundaries.
   Every delegated thread must have:
   - one objective
   - a clear read/write boundary
   - expected evidence or deliverables
   - an integration-ready return summary

7. Explain the routing decision when required.
   - If you delegate, state why delegation is better than staying solo.
   - If you stay `solo` despite strong specialist pressure, state why subagents are not better for this task.
   - Do not surface routine routing commentary unless `router.yaml` says the decision should be visible.

8. Synthesize back into one parent-thread decision.
   Merge delegated outputs, resolve conflicts explicitly, and present one final answer that matches the user’s requested deliverable.

## Decision Rules

- Prefer `single_delegate` over `multi_agent` when one specialist owns the main path cleanly.
- Prefer `multi_agent` only when workstreams are genuinely independent or parallel review adds clear value.
- Prefer read-only discovery specialists before write-capable delegates when the path is still uncertain.
- Do not treat file count alone as a delegation trigger.
- Do not choose multiple write-capable delegates unless ownership boundaries are strict and non-overlapping.
- Do not use a weak specialist match just to avoid staying local. If delegation still helps, use a built-in fallback role.

## Bundled Resources

- `router.yaml`
  Authoritative routing configuration for execution modes, policy defaults, categories, curated specialists, and structured examples.
- `references/decision-rules.md`
  Read when the routing choice is ambiguous or the task sits near the `solo` / delegated boundary.
- `references/agent-taxonomy.md`
  Read when you need the category view to narrow the best specialist after choosing the execution mode.
- `references/prompt-summary.md`
  Use when an environment needs a short prompt-facing summary of the router policy.
- `scripts/validate_router.py`
  Run after router changes to verify that routing metadata matches `registry.yaml` and that structured routing examples use canonical agent ids.

## Output Expectations

When the routing decision is visible, summarize it with:
- `mode`
- `work_mode`
- `domain`
- selected agent(s), if any
- why delegation is or is not better than staying solo
- why you did not add more agents
- confidence
