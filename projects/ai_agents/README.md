# AI Agents — Learn Agentic AI in Python

**Tier**: Intermediate → Advanced | **Learning Path**: AI Agents & LLMs
**Prerequisites**: comfortable with Python classes, type hints, and JSON; helpful (not
required) to have done `projects/ai_agent_chatbot/` first.

This folder is a hands-on curriculum for the six ideas almost every "AI agent" (and every
non-agent "just call an LLM in a script" system) you'll meet is built from: **fixed
workflows**, **tool use**, **reasoning loops**, **multi-agent collaboration**,
**memory/RAG**, and **planning**. Each idea gets its own self-contained subfolder with
working code, its own README, and tests you can run with no API key at all.

> **What is an "agent," really?** In this module, an agent is: an LLM call, inside a
> loop, that can affect something outside itself (run a tool, talk to another agent,
> read/write memory, execute a plan) and decide what to do next based on the result.
> Agent 0 is deliberately **not** that — it's here so you see the simpler alternative
> before you reach for a loop.

## The six modules

| # | Folder | Concept | One-line description |
|---|---|---|---|
| 0 | [`agent0_workflows/`](./agent0_workflows) | **Fixed workflows (not agents)** | A fixed sequence of LLM calls with a plain-Python gate check (prompt chaining), and a classify-then-dispatch pipeline (routing) — no loop, no autonomy. |
| 1 | [`agent1_web_search/`](./agent1_web_search) | **Tool use** | The model decides when to search the web, reads the results, and answers with citations. |
| 2 | [`agent2_react_reasoning/`](./agent2_react_reasoning) | **ReAct reasoning** | The same "reason → act → observe" loop as Agent 1, written by hand with regex parsing instead of an API's `tools=` parameter. |
| 3 | [`agent3_multi_agent_team/`](./agent3_multi_agent_team) | **Multi-agent collaboration** | A Writer and a Reviewer pass drafts and feedback back and forth until a Coordinator (plain Python) is satisfied. |
| 4 | [`agent4_memory_rag/`](./agent4_memory_rag) | **Memory / RAG** | Answers are grounded in a small, from-scratch vector store (bag-of-words + cosine similarity) instead of the model's own knowledge. |
| 5 | [`agent5_planner_executor/`](./agent5_planner_executor) | **Planning & autonomy** | The model commits to a full multi-step plan up front; a separate executor works through it without checking back in. |

**Suggested order**: 0 → 1 → 2 → 3 → 4 → 5. Start with Agent 0 so "agent" doesn't become a
reflex — plenty of real problems are better solved by the workflows in that folder than by
a loop. Agents 1 and 2 then teach the same reasoning idea two ways so you can compare a
framework-assisted loop to a hand-rolled one; 3-5 each add a new capability on top of that
base loop.

## Setup (once, for all six modules)

Run everything from the **repository root** (not from inside this folder — see
"Why `python -m`" below).

```bash
pip install -r projects/ai_agents/requirements.txt
cp projects/ai_agents/.env.example .env
# then edit .env and set ANTHROPIC_API_KEY
```

You need exactly one API key: **`ANTHROPIC_API_KEY`**, from
<https://console.anthropic.com/>. Agent 1 additionally installs `ddgs` for web search, but
that backend needs no API key of its own. Nothing else in this module talks to any other
external service.

Optional overrides (all have working defaults — see `.env.example`):

| Variable | Default | Used by |
|---|---|---|
| `ANTHROPIC_API_KEY` | *(required)* | all six modules |
| `AI_AGENTS_MODEL` | `claude-sonnet-5` | all six modules |
| `AI_AGENTS_MAX_TOKENS` | `1024` | all six modules |
| `AI_AGENTS_MEMORY_PATH` | `agent4_memory_rag/memory_store.json` | Agent 4 only |

Model IDs change over time — if `claude-sonnet-5` isn't valid for your account, check the
current list at <https://docs.anthropic.com/> and set `AI_AGENTS_MODEL` accordingly.

## Running an agent

Every module is run the same way, as a module, from the repo root:

```bash
python -m projects.ai_agents.agent0_workflows.main chain "some long text to summarize" Spanish
python -m projects.ai_agents.agent1_web_search.main "What is the latest stable Python release?"
python -m projects.ai_agents.agent2_react_reasoning.main "What is the capital of France, and what is 12 * 8?"
python -m projects.ai_agents.agent3_multi_agent_team.main "Why Python is a good first programming language"
python -m projects.ai_agents.agent4_memory_rag.main "What is projects/ai_agents?"
python -m projects.ai_agents.agent5_planner_executor.main "Explain a 20% tip on a $45.50 bill and save it to a file"
```

Run any of them with no arguments and it uses the sample question shown above, so you can
verify your setup works before writing your own prompt.

### Why `python -m ...` instead of `python main.py`?

Each agent imports shared code from `projects/utils/` and, in a couple of cases, from its
own sibling modules using absolute imports (`from projects.ai_agents.agent1_web_search...`).
That only resolves correctly if the **repository root** is on `sys.path`, which is exactly
what `python -m package.path.to.module` guarantees when run from the root. `cd`-ing into a
subfolder and running `python main.py` directly will raise `ModuleNotFoundError`.

## Running the tests

Every agent's tests mock the Anthropic client (and, for Agent 1, the search backend too),
so **none of them make network calls or need a real API key**:

```bash
python -m pytest projects/ai_agents/ -v
```

Or scope it to one agent while you're working on it:

```bash
python -m pytest projects/ai_agents/agent3_multi_agent_team/tests/ -v
```

## Repository conventions these agents follow

Consistent with the rest of this repo (see the root `CLAUDE.md` / `CONTRIBUTING.md`):

- Absolute imports rooted at `projects.` (not relative `from agent import ...`), so
  `pytest projects/` works from the repo root without any path hacks.
- Shared error handling via `projects/utils/errors.BaseProjectError` — every agent raises
  its own `AgentError` subclass (`WorkflowError` in Agent 0) rather than a bare exception.
- Shared logging via `projects/utils/logging_config.setup_logger()`.
- Google-style docstrings and type hints throughout.
- `tests/test_*.py`, class-based, one test class per unit under test.

## Cost and rate limits

Every `main.py` invocation makes at least one real API call once you supply a key (2+ for
Agent 0, Agent 3, and Agent 5, since each coordinates multiple model calls per run). These
are small requests, but they are not free and are subject to your account's rate limits —
the tests never hit the API, but running the agents themselves does.

## Reading guide: what to focus on first

Every folder has more "plumbing" code than "concept" code, and it's easy to spend your
first read on the wrong half. Per folder, in priority order:

1. **The README, in full.** It tells you the one idea the folder exists to teach, before
   you look at a single line of code.
2. **`agent.py` (or `coordinator.py` / `prompt_chain.py` / `router.py`)** — this is the
   concept. It's short (well under 150 lines everywhere in this module) on purpose. Read
   it slowly, ideally next to the diagram in that folder's README.
3. **One test file, e.g. `tests/test_agent.py`** — tests double as worked examples: they
   show you exactly what a call into this code looks like and what comes back, without
   needing a real API key to try it yourself.
4. **The tool/plumbing files last** (`search_tool.py`, `tools.py`, `memory_store.py`,
   `executor.py`, `planner.py`). Skim these on your first pass through a folder — they're
   "how do we call a search API" or "how do we evaluate an expression safely," not "how
   does this agent pattern work." Come back to them once the concept in step 2 has
   clicked; several of them (see the table below) are also good standalone Python
   exercises in their own right.
5. **Skip on your first pass**: `main.py` (it's just CLI argument plumbing — `sys.argv`
   handling — the same shape in every folder) and `__init__.py` files (one-line docstrings,
   nothing to learn there).

## Python concepts index

This module isn't only for learning agents — every file is also plain Python, and several
demonstrate a core language or standard-library feature clearly enough to be worth reading
for that alone, independent of the AI angle. If you're here mainly to get better at Python:

| Concept | Where to see it |
|---|---|
| `@dataclass` (plus `field(default_factory=...)`) | `agent3_multi_agent_team/coordinator.py` (`Round`, `TeamResult`), `agent5_planner_executor/planner.py` (`Step`) |
| Custom exception hierarchies (`class X(SomeBase)`) | `projects/utils/errors.py`, and every `agent.py`'s `AgentError`/`WorkflowError` |
| `typing.NamedTuple` vs. `@dataclass` (and when to pick each) | `agent3_multi_agent_team/agents.py` (`ReviewVerdict`) next to `coordinator.py`'s dataclasses |
| Regular expressions for parsing free-text model output | `agent2_react_reasoning/agent.py` (`_ACTION_RE`, `_FINAL_ANSWER_RE`), `agent5_planner_executor/planner.py` (`_JSON_ARRAY_RE`) |
| `json.loads` / `json.dumps` and defensive parsing of untrusted text | `agent5_planner_executor/planner.py` (`_parse_steps`), `agent4_memory_rag/memory_store.py` (persistence) |
| `pathlib.Path` for file I/O (instead of raw `open()`) | `agent4_memory_rag/memory_store.py`, `agent5_planner_executor/executor.py` |
| `collections.Counter` for word-frequency vectors | `agent4_memory_rag/memory_store.py` (`_vectorize`) |
| Context managers (`with ... as ...`) | `agent1_web_search/search_tool.py` (`with ddgs_client() as ddgs`) |
| A restricted `eval()` sandbox (and why the restriction matters) | `agent2_react_reasoning/tools.py` and `agent5_planner_executor/executor.py`, both `calculator()` |
| `@staticmethod` / `@classmethod` and when each is the right choice | `agent1_web_search/agent.py` (`_extract_text`), `agent4_memory_rag/memory_store.py`'s `Document.from_dict` |
| Dunder methods for custom containers (`__len__`, so `len(store)` just works) | `agent4_memory_rag/memory_store.py` (`MemoryStore.__len__`) |
| List/dict comprehensions and generator expressions | throughout — e.g. `agent1_web_search/agent.py`'s `_run_tool` dispatch, `agent4_memory_rag/memory_store.py`'s `_cosine_similarity` |
| `unittest.mock` (`MagicMock`, `patch`, `side_effect` vs. `return_value`) | every `tests/test_agent.py` — the tests are as much a mocking tutorial as an agent tutorial |
| `pytest` fixtures (`tmp_path`) for filesystem-touching tests | `agent4_memory_rag/tests/test_memory_store.py`, `agent5_planner_executor/tests/test_executor.py` |

## Where to go from here

Each subfolder's README ends with a "Things to try next" section — those are the fastest
way to turn reading this code into understanding it. A natural next step after all six is
combining ideas: e.g. give the Agent 3 team a web-search tool (Agent 1), make Agent 5's
planner re-plan using retrieved memory (Agent 4), or rebuild Agent 0's router as an actual
agent that loops instead of running exactly two calls.
