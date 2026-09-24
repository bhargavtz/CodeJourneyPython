# Agent 5 — Planner-Executor Agent

**Concept taught:** planning + autonomous execution — the pattern behind "autonomous agent"
projects like AutoGPT. Instead of deciding one action at a time (Agents 1 and 2), this agent
commits to a full plan up front and then works through it without checking back in.

## What it does

1. **Plan**: given a goal, Claude returns a JSON list of 2-5 steps, each naming a tool
   (`note`, `calculator`, or `write_file`) and the input for that tool.
2. **Execute**: the `Executor` runs each step *locally, with no further model calls*,
   building up a scratchpad of what happened.
3. **Summarize**: once every step has run, Claude is called one last time with the full
   step-by-step report and asked to explain in plain language what was accomplished.

```
goal ──▶ Planner (1 model call) ──▶ [Step, Step, Step]
                                          │
                                          ▼
                              Executor runs each step
                              locally (no model calls)
                                          │
                                          ▼
                         Summarizer (1 model call) ──▶ final report
```

## Files

| File | Purpose |
|---|---|
| `planner.py` | `Planner.plan()` — prompts for a JSON step list, parses it (including through markdown code fences), raises `PlanningError` on malformed output |
| `executor.py` | `Executor` — the `note` / `calculator` / `write_file` tools, a scratchpad, and a sandboxed `outputs/` directory |
| `agent.py` | `PlannerExecutorAgent` — wires Planner → Executor → summary call together, `RunResult` dataclass |
| `main.py` | CLI: `python -m projects.ai_agents.agent5_planner_executor.main "your goal"` |
| `tests/` | `test_executor.py` needs no mocking at all (no LLM involved); `test_planner.py` and `test_agent.py` mock the Anthropic client |

## Setup

```bash
pip install -r projects/ai_agents/requirements.txt   # from the repo root
cp projects/ai_agents/.env.example .env               # add your ANTHROPIC_API_KEY
```

## Run it

```bash
python -m projects.ai_agents.agent5_planner_executor.main \
  "Explain what a 20% tip on a \$45.50 bill is, and save the explanation to a file"
```

Example output (abridged):

```
--- Plan ---
1. [calculator] Compute the tip amount
2. [write_file] Save a plain-language explanation

--- Step results ---
1. 9.100000000000001
2. Wrote 118 characters to step_2.txt

--- Summary ---
Calculated a 20% tip of $9.10 on a $45.50 bill and saved a short
explanation of the calculation to step_2.txt.
```

Files written by `write_file` steps land in `agent5_planner_executor/outputs/` (created
automatically, gitignored).

## Run the tests

```bash
python -m pytest projects/ai_agents/agent5_planner_executor/tests/ -v
```

## Things to try next

- This agent never re-plans: if step 2 depends on step 1's *actual* result and the plan
  guessed wrong, it just presses on. Try adding a check in `agent.py` that re-calls the
  Planner with the scratchpad so far if a step's result looks like an error.
- Add a `read_file` tool so later steps can use what earlier `write_file` steps produced.
- Compare this to `agent1_web_search`: that agent re-decides after *every* tool call
  (fully reactive); this one decides *once* and executes blindly (fully deliberative).
  Most production agents live somewhere in between — what would a hybrid look like?
