---
name: confidence-score-workflow
description: 'Score how well-defined a task is, ask exactly one clarifying question at a time, and decide when to proceed. Use for requirement clarification and confidence-gated execution in any agent or orchestrator workflow where ambiguity in the user request could lead to wasted work, incorrect implementation, or destructive changes.'
user-invocable: false
---

# Confidence Score Workflow

Reusable methodology for assessing task clarity and deciding whether to ask
clarifying questions, proceed with documented assumptions, or proceed only after
confirmation.

## Purpose

- Quantify how well-defined a task is on a 0.00 — 1.00 scale.
- Drive clarification with **one** question at a time, never a batch.
- Make uncertainty transparent to the user every turn.
- Avoid premature implementation when critical inputs are missing.

## Outcome

- A confidence score from 0.00 to 1.00 with a one-line rationale, reported at the
  top of every assistant reply that participates in the workflow.
- A structured clarification loop that continues until the readiness threshold
  is reached.
- An explicit proceed decision that lists any assumptions when proceeding below
  full confidence.

## Core Rubric

| Range       | Meaning                                                     | Action                                                                                  |
| ----------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 0.00 — 0.30 | Critical information missing.                               | Ask one clarifying question. Do **not** propose a plan.                                 |
| 0.31 — 0.60 | Significant gaps remain.                                    | Ask one clarifying question. Do **not** propose a plan.                                 |
| 0.61 — 0.84 | Minor gaps remain; assumptions possible but not preferred.  | Ask one clarifying question. Do **not** propose a plan.                                 |
| 0.85 — 0.94 | Mostly clear.                                               | Ask the next single question **and** offer the option to proceed with assumptions.      |
| 0.95 — 1.00 | Fully specified.                                            | Present plan / task breakdown and request confirmation before execution.                |

## Procedure

### 1. Define Task-Specific Dimensions

1. Pick 3 — 6 dimensions whose weights sum to **1.00**.
2. Keep dimensions concrete and observable (something that can be answered with
   "yes / partial / no").
3. Always include at least one dimension covering **output format / acceptance
   criteria** and one covering **scope / target files**.

### 2. Score Each Dimension

1. Use `0` when the dimension is missing or unknown.
2. Use the full weight when the dimension is fully specified.
3. Use partial credit (e.g. half the weight) for partially defined inputs.
4. Sum across dimensions and round to two decimals.

### 3. Report Score Every Turn

Use this header line at the very top of every reply that is part of the
workflow:

```text
Confidence: 0.XX / 1.00 — <one-line rationale naming the weakest dimension>
```

### 4. Act by Rubric Threshold

1. `0.00 — 0.84`: ask exactly one clarifying question.
2. `0.85 — 0.94`: ask one clarifying question **and** offer a
   proceed-with-assumptions option.
3. `0.95 — 1.00`: provide the plan / task breakdown and ask for explicit
   confirmation before any non-trivial edit, command, or delegation.

### 5. Clarification Loop

After each user answer:

1. Update the affected dimension scores.
2. Recompute the total and report the new confidence line.
3. Ask the next single clarifying question, or move to confirmation if the
   threshold is reached.

## Clarifying Question Format

```text
Clarifying question (k of N estimated)

<single concrete question>

Why I need this: <one sentence>

Options (if applicable):
- (A) ...
- (B) ...
- (C) Other — please specify
```

## Best Practices

- Do **not** inflate scores to proceed faster.
- State what is known **and** unknown in the rationale.
- Ask exactly one question per turn.
- Document assumptions explicitly if proceeding in the `0.85 — 0.94` band.
- Recompute the score after every clarification — never leave a stale score.
- Skip the workflow for trivial, fully-specified, read-only requests (e.g.
  "show me the contents of file X"). Engage it when the task involves writing
  code, running commands, delegating to specialists, or making irreversible
  changes.

## Anti-patterns

- Multiple clarifying questions in one turn.
- Reporting the score without a rationale.
- Proceeding below the threshold without an explicit assumptions block.
- A static score that is not updated after new user input.
- Using the workflow as a stalling tactic on obviously clear requests.

## Agent Integration Template

Paste the block below into an agent definition and fill in the dimensions:

```markdown
## Confidence Score Integration

This agent follows `.github/skills/confidence-score-workflow/SKILL.md`.

Task-specific dimensions (weights sum to 1.00):
- <Dimension 1> (0 — 0.XX)
- <Dimension 2> (0 — 0.XX)
- <Dimension 3> (0 — 0.XX)
- ...

The agent reports `Confidence: 0.XX / 1.00 — <rationale>` at the top of every
reply, asks one clarifying question at a time below the 0.95 threshold, and
only proposes a plan / delegates to specialists once confidence reaches
0.95 — 1.00 (or 0.85 — 0.94 with explicit user-approved assumptions).
```
