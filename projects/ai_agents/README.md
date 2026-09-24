# AI Agents — Learn Agentic AI in Python

**Tier**: Intermediate → Advanced | **Learning Path**: AI Agents & LLMs
**Prerequisites**: comfortable with Python classes, type hints, and JSON; helpful (not
required) to have done `projects/ai_agent_chatbot/` first.

This folder is a hands-on curriculum for the six ideas almost every "AI agent" (and every
non-agent "just call an LLM in a script" system) you'll meet is built from: **fixed
workflows**, **tool use**, **reasoning loops**, **multi-agent collaboration**,
**memory/RAG**, and **planning**. Each idea gets its own self-contained subfolder with
working code and tests you can run with no API key at all — everything you need to know
about all six lives in this one file, so there is nowhere else you need to look.

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

### Why `python -m ...` instead of `python main.py`?

Each module imports shared code from `projects/utils/` and, in a couple of cases, from its
own sibling modules using absolute imports (`from projects.ai_agents.agent1_web_search...`).
That only resolves correctly if the **repository root** is on `sys.path`, which is exactly
what `python -m package.path.to.module` guarantees when run from the root. `cd`-ing into a
subfolder and running `python main.py` directly will raise `ModuleNotFoundError`.

## Running the tests

Every module's tests mock the Anthropic client (and, for Agent 1, the search backend too),
so **none of them make network calls or need a real API key**:

```bash
python -m pytest projects/ai_agents/ -v
```

Or scope it to one module while you're working on it:

```bash
python -m pytest projects/ai_agents/agent3_multi_agent_team/tests/ -v
```

## Repository conventions these agents follow

Consistent with the rest of this repo (see the root `CLAUDE.md` / `CONTRIBUTING.md`):

- Absolute imports rooted at `projects.` (not relative `from agent import ...`), so
  `pytest projects/` works from the repo root without any path hacks.
- Shared error handling via `projects/utils/errors.BaseProjectError` — every module raises
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

1. **This file's section for that folder.** It tells you the one idea the folder exists
   to teach, before you look at a single line of code.
2. **`agent.py` (or `coordinator.py` / `prompt_chain.py` / `router.py`)** — this is the
   concept. It's short (well under 150 lines everywhere in this module) on purpose. Read
   it slowly, ideally next to that folder's diagram below.
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

---

## Agent 0 — Workflows (Prompt Chaining & Routing)

**Concept taught:** the two patterns you should reach for *before* building a full agent.
Read this one first, even though the folder numbering makes it look like an afterthought —
it's the missing "easier option" that every other folder in this module skips past.

**Why this folder exists:** Agents 1-5 are all, in one way or another, a **loop**: the
model gets another turn, decides what to do next, and the number of steps isn't known in
advance. That's powerful, but it's also slower, harder to test, and harder to debug than
it needs to be for a lot of real tasks. Plenty of problems are better solved with a
**fixed sequence of LLM calls** that a human designed — no loop, no autonomy, the model
never decides "what happens next." That's a **workflow**, and this folder has two of the
most common ones.

**1. Prompt chaining** (`prompt_chain.py`) — break one task into ordered steps, each a
separate (smaller, more reliable) LLM call, with a plain **Python** check — a "gate" — in
between that can stop the chain early:

```
text ──▶ [Call 1: summarize] ──▶ summary ──▶ [Gate: is it short enough?]
                                                    │ no            │ yes
                                                    ▼                ▼
                                          stop, report          [Call 2: translate]
                                          gate_passed=False           │
                                                                        ▼
                                                              gate_passed=True
```

The gate (`PromptChainWorkflow._passes_gate`) is not an LLM call — it's an ordinary
`if len(summary.split()) <= max_summary_words`. That's the point: cheap, instant,
deterministic checks between expensive, non-deterministic model calls.

**2. Routing** (`router.py`) — classify the input first, then hand it to a
category-specific prompt instead of one prompt trying to handle every case:

```
message ──▶ [Call 1: classify] ──▶ category ──▶ [Call 2: category's own system prompt] ──▶ response
```

If the classifier ever returns something that isn't one of the known categories,
`classify()` falls back to `"general"` instead of raising — a misrouted message should
degrade gracefully, not crash the whole workflow.

**Files**

| File | Purpose |
|---|---|
| `prompt_chain.py` | `PromptChainWorkflow` — summarize → gate → translate |
| `router.py` | `RouterWorkflow` — classify → dispatch to a category's system prompt |
| `main.py` | CLI: `chain` and `route` subcommands |
| `tests/` | Offline tests (Anthropic client mocked); the chain tests specifically assert the *second* call never happens when the gate fails |

**Run it**

```bash
python -m projects.ai_agents.agent0_workflows.main chain "some long text to summarize" Spanish
python -m projects.ai_agents.agent0_workflows.main route "My payment failed twice today"
```

Run with no arguments and it defaults to the `chain` demo on a sample paragraph about Python.

**Run the tests**

```bash
python -m pytest projects/ai_agents/agent0_workflows/tests/ -v
```

**Things to try next**
- Lower `max_summary_words` until the gate starts rejecting real summaries, and watch
  `main.py chain` report the rejection instead of crashing.
- Add a third stage to the chain (e.g. summarize → translate → shorten-to-one-sentence)
  and a second gate between the new steps.
- Add a fourth category to `router.py`'s `ROUTE_SYSTEM_PROMPTS` and update
  `CLASSIFY_SYSTEM_PROMPT`'s category list (it's generated from the dict, so nothing else
  needs to change).
- Once both feel familiar, go compare them to Agent 2 below: same building blocks (a
  system prompt, a user message, parsing the reply), but Agent 2 keeps looping based on
  what the model says instead of following a fixed number of steps. That difference —
  fixed steps vs. model-decided steps — is the line between a workflow and an agent.

---

## Agent 1 — Web Search Agent

**Concept taught:** tool use / function calling — the single most important agent
pattern. Everything else in this module (Agents 2-5) builds on this loop.

**What it does:** you ask a question. The agent (Claude) decides for itself whether it
already knows the answer or needs to search the web first. If it needs to search, it
calls the `web_search` tool, reads the results, and either answers or searches again — up
to 5 rounds — before giving you a final answer with the URLs it used.

**The core loop:**

```
1. Send the user's question + the web_search tool definition to Claude.
2. Claude replies with either:
     a) a direct text answer -> done, return it
     b) a request to call web_search(query=...) -> go to step 3
3. Run web_search() locally, get back titles/URLs/snippets.
4. Send those results back to Claude as a "tool_result".
5. Repeat from step 2.
```

This is implemented in `agent.py` — read `WebSearchAgent.ask()` first, it's ~25 lines and
it's the whole pattern.

**Files**

| File | Purpose |
|---|---|
| `search_tool.py` | The actual search function (DuckDuckGo, no API key needed) + the JSON schema Claude uses to know the tool exists and what arguments it takes |
| `agent.py` | `WebSearchAgent` — the tool-use loop described above |
| `main.py` | CLI: `python -m projects.ai_agents.agent1_web_search.main "your question"` |
| `tests/` | Offline tests (search backend and Anthropic client are both mocked — no network or API key needed to run them) |

**Run it**

```bash
python -m projects.ai_agents.agent1_web_search.main "What is the most recent stable Python release?"
```

Example output:

```
Q: What is the most recent stable Python release?

Python 3.13 is the most recent stable release as of this search...
Sources: https://www.python.org/downloads/
```

(Run without arguments and it falls back to that same sample question.)

**Run the tests**

```bash
python -m pytest projects/ai_agents/agent1_web_search/tests/ -v
```

These tests never make a network call or hit the Anthropic API — `search_tool.DDGS` and
`agent.Anthropic` are both patched with mocks, so they run in CI with no keys configured.

**Things to try next**
- Add a second tool (e.g. a `fetch_url` tool that downloads and summarizes one page) and
  watch Claude choose between them.
- Print `response.usage` after each call to see how tokens accumulate across rounds.
- Lower `MAX_TOOL_ROUNDS` to 1 and see the `AgentError` fire on a question that needs two
  searches.
- Compare this to Agent 2 below, which implements the *same idea* (reason → act → observe
  → repeat) by hand, without the SDK's `tools=` parameter, so you can see what the SDK is
  doing for you under the hood.

---

## Agent 2 — ReAct Reasoning Agent

**Concept taught:** the ReAct pattern (Reason + Act), written by hand with regular
expressions and plain-text parsing — no `tools=` API parameter. This is what tool-use
libraries and SDKs are automating *for* you; seeing it done manually once makes every
"agent framework" you meet afterwards much less mysterious.

**What it does:** the model is instructed (entirely through its system prompt — no
API-level tool support) to respond in a strict `Thought / Action / Observation` format:

```
Thought: I need to know the capital of France.
Action: knowledge_lookup[capital of france]
```

The agent parses that text with a regex, runs the matching Python function locally,
appends `Observation: Paris` to the conversation, and sends it back. This repeats until
the model instead responds with:

```
Thought: I now have everything I need.
Final Answer: Paris
```

**Files**

| File | Purpose |
|---|---|
| `tools.py` | `calculator()` and `knowledge_lookup()` — plain Python functions, no schema, no API involvement |
| `agent.py` | `ReActAgent` — builds the transcript, calls the model, parses `Action:`/`Final Answer:` with regex, dispatches to `tools.py` |
| `main.py` | CLI: `python -m projects.ai_agents.agent2_react_reasoning.main "your question"` |
| `tests/` | Offline tests — the Anthropic client is mocked with canned ReAct-formatted text, so parsing logic and tool dispatch are fully covered without any API key |

**Run it**

```bash
python -m projects.ai_agents.agent2_react_reasoning.main "What is the capital of France, and what is 12 * 8?"
```

Example transcript (abridged):

```
Thought: I need the capital of France first.
Action: knowledge_lookup[capital of france]
Observation: Paris

Thought: Now the arithmetic.
Action: calculator[12 * 8]
Observation: 96

Thought: I have both answers.
Final Answer: The capital of France is Paris, and 12 * 8 = 96.
```

**Run the tests**

```bash
python -m pytest projects/ai_agents/agent2_react_reasoning/tests/ -v
```

**Things to try next**
- Break the format on purpose (delete the `Action:` line requirement from the system
  prompt) and watch the "no Action or Final Answer" recovery message in `agent.py` kick in.
- Add a third tool to `tools.py` and to `TOOL_DESCRIPTIONS` — nothing else needs to change.
- Compare `_ACTION_RE` / `_FINAL_ANSWER_RE` in `agent.py` with how Agent 1 gets the same
  information as structured JSON from `response.stop_reason` and
  `block.type == "tool_use"` instead of parsing text — that's the difference between a
  model with native tool-use support and one without.

---

## Agent 3 — Multi-Agent Team (Writer + Reviewer + Coordinator)

**Concept taught:** multi-agent collaboration. Instead of one agent doing everything, two
specialized agents — each with a narrow job and its own system prompt — pass messages to
each other, and a plain Python `Coordinator` (not itself a model call) decides when the
team is done.

**What it does:** give the team a topic. Internally:

1. **WriterAgent** drafts ~200 words on the topic.
2. **ReviewerAgent** reads the draft and responds with either `APPROVED` or
   `REVISE: <specific feedback>`.
3. **Coordinator** — plain Python, no LLM call — checks the verdict:
   - approved → done, return the draft.
   - needs revision → send the feedback back to the Writer and go to step 1.
4. This repeats up to `MAX_ROUNDS` (3). If it never gets approved, the Coordinator
   returns the last draft anyway, marked `approved=False`, instead of crashing — a
   deliberately different failure mode from Agents 1 and 2, which raise instead.

**Files**

| File | Purpose |
|---|---|
| `agents.py` | `WriterAgent` and `ReviewerAgent` — each a single Anthropic call behind a narrow interface (`draft()`, `review()`) |
| `coordinator.py` | `Coordinator` — the loop, `Round`/`TeamResult` dataclasses tracking history |
| `main.py` | CLI: `python -m projects.ai_agents.agent3_multi_agent_team.main "your topic"` |
| `tests/` | Offline tests for each agent in isolation, and for the Coordinator's loop with both agents mocked |

**Run it**

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

**Run the tests**

```bash
python -m pytest projects/ai_agents/agent3_multi_agent_team/tests/ -v
```

`test_agents.py` mocks the Anthropic client directly to unit-test each agent alone.
`test_coordinator.py` goes one level up and mocks `coordinator.writer`/`coordinator.reviewer`
themselves, so the loop's control flow (approve immediately / revise once / never approve)
is tested independent of prompt wording.

**Things to try next**
- Add a third specialist (e.g. a `FactCheckerAgent`) and have the Coordinator only accept
  a draft once *both* the Reviewer and the Fact Checker approve it.
- Change `Coordinator.run()` to have the Writer and Reviewer see each other's full history
  instead of just the latest feedback — what changes?
- Swap the Writer/Reviewer roles for a different pair (e.g. `CodeGeneratorAgent` +
  `CodeReviewAgent`) — the coordination pattern doesn't care what the agents produce.

---

## Agent 4 — Memory / RAG Agent

**Concept taught:** Retrieval-Augmented Generation (RAG), built entirely from the standard
library so the mechanism is visible. Most tutorials jump straight to a vector database and
an embeddings API; this one shows what those tools are actually doing underneath.

**What it does:**

1. **Remember**: text you give it is turned into a *bag-of-words vector* — just a
   `{word: count}` dict — and stored (optionally persisted to a JSON file).
2. **Ask**: your question is vectorized the same way, compared against every stored
   document with cosine similarity, and the top matches are handed to Claude as numbered
   context passages.
3. The system prompt tells Claude to answer **only** from those passages and to say so
   plainly if they don't contain the answer — the core promise of RAG: answers you can
   trace back to a source, not the model's general knowledge.

The store comes pre-seeded with a few facts about this repository, so you can ask it
questions immediately without adding anything first.

**Files**

| File | Purpose |
|---|---|
| `memory_store.py` | `MemoryStore` — tokenizer, bag-of-words vectorizer, cosine similarity, and JSON persistence. Zero third-party dependencies. |
| `agent.py` | `MemoryAgent` — retrieves top-`k` passages, builds the "answer only from context" prompt, calls Claude |
| `main.py` | CLI: `ask` (default) and `remember` subcommands |
| `tests/` | `test_memory_store.py` is fully offline (pure Python, no mocks needed at all); `test_agent.py` mocks only the Anthropic client, using a real in-memory store |

**Run it**

```bash
# Ask a question (uses the pre-seeded facts about this repo)
python -m projects.ai_agents.agent4_memory_rag.main "What is projects/ai_agents?"

# Teach it something new — persisted to memory_store.json next to this folder
python -m projects.ai_agents.agent4_memory_rag.main remember "The repo's license is MIT."
python -m projects.ai_agents.agent4_memory_rag.main "What license does this repo use?"
```

Example output:

```
Q: What is projects/ai_agents?

projects/ai_agents/ contains six educational agent/workflow implementations, covering
fixed workflows, tool use, ReAct reasoning, multi-agent collaboration, memory/RAG,
and planning [1].
```

Set `AI_AGENTS_MEMORY_PATH` (see `.env.example`) to point the store at a different file.

**Run the tests**

```bash
python -m pytest projects/ai_agents/agent4_memory_rag/tests/ -v
```

**Things to try next**
- Ask a question sharing only common words (like "the", "is") with a stored fact and
  inspect the similarity score — bag-of-words treats every word as equally meaningful, so
  stray overlaps in stop words can nudge the score above zero. Real embedding models don't
  have this problem because they represent *meaning*, not just word counts.
- Swap `_vectorize`/`_cosine_similarity` in `memory_store.py` for a real embeddings call
  and compare retrieval quality on synonyms your bag-of-words version misses (e.g. "car"
  vs. "automobile").
- Add a `forget(doc_id)` method to `MemoryStore` and wire it into `main.py`.

---

## Agent 5 — Planner-Executor Agent

**Concept taught:** planning + autonomous execution — the pattern behind "autonomous
agent" projects like AutoGPT. Instead of deciding one action at a time (Agents 1 and 2),
this agent commits to a full plan up front and then works through it without checking
back in.

**What it does:**

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

**Files**

| File | Purpose |
|---|---|
| `planner.py` | `Planner.plan()` — prompts for a JSON step list, parses it (including through markdown code fences), raises `PlanningError` on malformed output |
| `executor.py` | `Executor` — the `note` / `calculator` / `write_file` tools, a scratchpad, and a sandboxed `outputs/` directory |
| `agent.py` | `PlannerExecutorAgent` — wires Planner → Executor → summary call together, `RunResult` dataclass |
| `main.py` | CLI: `python -m projects.ai_agents.agent5_planner_executor.main "your goal"` |
| `tests/` | `test_executor.py` needs no mocking at all (no LLM involved); `test_planner.py` and `test_agent.py` mock the Anthropic client |

**Run it**

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

**Run the tests**

```bash
python -m pytest projects/ai_agents/agent5_planner_executor/tests/ -v
```

**Things to try next**
- This agent never re-plans: if step 2 depends on step 1's *actual* result and the plan
  guessed wrong, it just presses on. Try adding a check in `agent.py` that re-calls the
  Planner with the scratchpad so far if a step's result looks like an error.
- Add a `read_file` tool so later steps can use what earlier `write_file` steps produced.
- Compare this to Agent 1: that agent re-decides after *every* tool call (fully reactive);
  this one decides *once* and executes blindly (fully deliberative). Most production
  agents live somewhere in between — what would a hybrid look like?

---

## Where to go from here

Each module's "Things to try next" above is the fastest way to turn reading this code into
understanding it. A natural next step after all six is combining ideas: e.g. give the
Agent 3 team a web-search tool (Agent 1), make Agent 5's planner re-plan using retrieved
memory (Agent 4), or rebuild Agent 0's router as an actual agent that loops instead of
running exactly two calls.
