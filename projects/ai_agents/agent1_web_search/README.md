# Agent 1 — Web Search Agent

**Concept taught:** tool use / function calling — the single most important agent pattern.
Everything else in this module (`agent2` .. `agent5`) builds on this loop.

## What it does

You ask a question. The agent (Claude) decides for itself whether it already knows the
answer or needs to search the web first. If it needs to search, it calls the `web_search`
tool, reads the results, and either answers or searches again — up to 5 rounds — before
giving you a final answer with the URLs it used.

## The core loop

```
1. Send the user's question + the web_search tool definition to Claude.
2. Claude replies with either:
     a) a direct text answer -> done, return it
     b) a request to call web_search(query=...) -> go to step 3
3. Run web_search() locally, get back titles/URLs/snippets.
4. Send those results back to Claude as a "tool_result".
5. Repeat from step 2.
```

This is implemented in [`agent.py`](./agent.py) — read `WebSearchAgent.ask()` first, it's
~25 lines and it's the whole pattern.

## Files

| File | Purpose |
|---|---|
| `search_tool.py` | The actual search function (DuckDuckGo, no API key needed) + the JSON schema Claude uses to know the tool exists and what arguments it takes |
| `agent.py` | `WebSearchAgent` — the tool-use loop described above |
| `main.py` | CLI: `python -m projects.ai_agents.agent1_web_search.main "your question"` |
| `tests/` | Offline tests (search backend and Anthropic client are both mocked — no network or API key needed to run them) |

## Setup

From the **repository root**:

```bash
pip install -r projects/ai_agents/requirements.txt
cp projects/ai_agents/.env.example .env   # then edit .env and add your ANTHROPIC_API_KEY
```

## Run it

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

## Run the tests

```bash
python -m pytest projects/ai_agents/agent1_web_search/tests/ -v
```

These tests never make a network call or hit the Anthropic API — `search_tool.DDGS` and
`agent.Anthropic` are both patched with mocks, so they run in CI with no keys configured.

## Things to try next

- Add a second tool (e.g. a `fetch_url` tool that downloads and summarizes one page) and
  watch Claude choose between them.
- Print `response.usage` after each call to see how tokens accumulate across rounds.
- Lower `MAX_TOOL_ROUNDS` to 1 and see the `AgentError` fire on a question that needs two
  searches.
- Compare this to `agent2_react_reasoning/` next door, which implements the *same idea*
  (reason → act → observe → repeat) by hand, without the SDK's `tools=` parameter, so you
  can see what the SDK is doing for you under the hood.
