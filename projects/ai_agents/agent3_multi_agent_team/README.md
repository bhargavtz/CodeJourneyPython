# Agent 3 — Multi-Agent Team (Writer + Reviewer + Coordinator)

**Concept taught:** multi-agent collaboration. Instead of one agent doing everything,
two specialized agents — each with a narrow job and its own system prompt — pass
messages to each other, and a plain Python `Coordinator` (not itself a model call)
decides when the team is done.

## What it does

Give the team a topic. Internally:

1. **WriterAgent** drafts ~200 words on the topic.
2. **ReviewerAgent** reads the draft and responds with either `APPROVED` or
   `REVISE: <specific feedback>`.
3. **Coordinator** — plain Python, no LLM call — checks the verdict:
   - approved → done, return the draft.
   - needs revision → send the feedback back to the Writer and go to step 1.
4. This repeats up to `MAX_ROUNDS` (3). If it never gets approved, the Coordinator
   returns the last draft anyway, marked `approved=False`, instead of crashing —
   a deliberately different failure mode from Agents 1 and 2, which raise instead.

## Files

| File | Purpose |
|---|---|
| `agents.py` | `WriterAgent` and `ReviewerAgent` — each a single Anthropic call behind a narrow interface (`draft()`, `review()`) |
| `coordinator.py` | `Coordinator` — the loop, `Round`/`TeamResult` dataclasses tracking history |
| `main.py` | CLI: `python -m projects.ai_agents.agent3_multi_agent_team.main "your topic"` |
| `tests/` | Offline tests for each agent in isolation, and for the Coordinator's loop with both agents mocked |

## Setup

```bash
pip install -r projects/ai_agents/requirements.txt   # from the repo root
cp projects/ai_agents/.env.example .env               # add your ANTHROPIC_API_KEY
```

## Run it

```bash
python -m projects.ai_agents.agent3_multi_agent_team.main "Why Python is a good first programming language"
```

Example output (abridged):

```
Topic: Why Python is a good first programming language

Status: APPROVED
Rounds used: 2

--- Final draft ---
Python's readable syntax lets beginners focus on programming concepts
instead of fighting the language itself...
```

## Run the tests

```bash
python -m pytest projects/ai_agents/agent3_multi_agent_team/tests/ -v
```

`test_agents.py` mocks the Anthropic client directly to unit-test each agent alone.
`test_coordinator.py` goes one level up and mocks `coordinator.writer`/`coordinator.reviewer`
themselves, so the loop's control flow (approve immediately / revise once / never approve)
is tested independent of prompt wording.

## Things to try next

- Add a third specialist (e.g. a `FactCheckerAgent`) and have the Coordinator only
  accept a draft once *both* the Reviewer and the Fact Checker approve it.
- Change `Coordinator.run()` to have the Writer and Reviewer see each other's full
  history instead of just the latest feedback — what changes?
- Swap the Writer/Reviewer roles for a different pair (e.g. `CodeGeneratorAgent` +
  `CodeReviewAgent`) — the coordination pattern doesn't care what the agents produce.
