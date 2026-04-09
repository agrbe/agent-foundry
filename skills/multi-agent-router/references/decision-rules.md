# Decision Rules

Use this file when the routing choice is ambiguous.

## Core Model

Pick the smallest execution mode that preserves quality:

- `solo`
  Use only when no curated specialist cleanly fits or one narrow local-first step must happen before delegation can help.
- `single_delegate`
  Use when one strong specialist cleanly owns the main task and the parent mostly needs to preserve context, decisions, and final synthesis.
- `multi_agent`
  Use only when workstreams are genuinely independent, review dimensions are distinct, or discovery and validation can run in parallel.

## Specialist Default

If a curated specialist matches the task requirements, use that specialist by default.

A clean specialist match means most of these are true:

- the task work mode is listed for that route
- the task domain is listed for that route
- the request aligns with the route's `preferred_for` focus
- none of the route's `avoid_for` constraints clearly apply

Only stay local when no curated specialist fits or a narrow local-first exception applies. Generic fallbacks exist for cases where delegation still helps but the catalog does not contain a matching specialist.

## When To Stay Solo

Stay `solo` when most of these are true:

- no curated specialist cleanly fits
- the next local step is unavoidable before delegation can help
- the code path is already known or cheap to inspect
- the work is tightly coupled
- the parent thread would need to reread and reintegrate nearly all delegated context anyway

If a matching specialist still exists, explain exactly why delegation is not possible or not useful yet.

## When To Use One Specialist

Prefer `single_delegate` when:

- one specialist can own the primary path
- that specialist matches the task requirements
- the task benefits from domain depth
- the main thread’s highest value is preserving context and making decisions
- adding more agents would only create serial handoffs

One strong specialist is usually better than multiple weakly differentiated agents.

## When To Use Multiple Specialists

Use `multi_agent` when:

- the task contains independent review dimensions such as security plus correctness plus test gaps
- ownership splits cleanly across subsystems
- read-only discovery can proceed in parallel with implementation or validation
- separate specialists can contribute without overlapping write scopes

Avoid multi-agent work when the extra agents would only reread the same context or wait on each other.

## Built-In Fallback Rule

If no curated specialist matches the task requirements:

- use `explorer` for read-only discovery
- use `default` for bounded delegated work with no strong domain dependence
- use `worker` for bounded write work when delegation still helps and ownership can be kept clean

Fallback to generic roles only because the catalog lacks a matching specialist, not because staying local feels simpler.

## Parent Thread Contract

The parent thread always owns:

- task framing
- constraints
- acceptance criteria
- key decisions
- final synthesis

Delegates own bounded execution, evidence gathering, or specialist critique inside those parent-controlled boundaries.
