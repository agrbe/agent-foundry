# Decision Rules

Use this file when the routing choice is ambiguous.

## Core Model

Pick the smallest execution mode that preserves quality:

- `solo`
  Use when the parent thread can make progress directly and delegation would mainly duplicate repo reading.
- `single_delegate`
  Use when one strong specialist cleanly owns the main task and the parent mostly needs to preserve context, decisions, and final synthesis.
- `multi_agent`
  Use only when workstreams are genuinely independent, review dimensions are distinct, or discovery and validation can run in parallel.

## Specialist Bias

Prefer a strong specialist whenever that specialist materially improves:

- execution speed
- evidence quality
- review quality
- framework or domain correctness
- risk reduction in high-stakes areas

Do not use a specialist just because one exists. The specialist must improve the outcome relative to staying local.

## When To Stay Solo

Stay `solo` when most of these are true:

- the task has one bounded deliverable
- the next step is obvious
- the code path is already known or cheap to inspect
- the work is tightly coupled
- the parent thread would need to reread and reintegrate nearly all delegated context anyway

If a strong specialist still exists, explain why subagents are not better for this case.

## When To Use One Specialist

Prefer `single_delegate` when:

- one specialist can own the primary path
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

If no curated specialist is a strong fit:

- use `explorer` for read-only discovery
- use `default` for bounded delegated work with no strong domain dependence
- use `worker` for bounded write work when delegation still helps and ownership can be kept clean

Fallback to generic roles because the absence of a perfect specialist should not force weak delegation or a bad routing choice.

## Parent Thread Contract

The parent thread always owns:

- task framing
- constraints
- acceptance criteria
- key decisions
- final synthesis

Delegates own bounded execution, evidence gathering, or specialist critique inside those parent-controlled boundaries.
