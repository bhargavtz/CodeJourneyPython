# Agent 4 — Memory / RAG Agent

**Concept taught:** Retrieval-Augmented Generation (RAG), built entirely from the standard
library so the mechanism is visible. Most tutorials jump straight to a vector database and
an embeddings API; this one shows what those tools are actually doing underneath.

## What it does

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

## Files

| File | Purpose |
|---|---|
| `memory_store.py` | `MemoryStore` — tokenizer, bag-of-words vectorizer, cosine similarity, and JSON persistence. Zero third-party dependencies. |
| `agent.py` | `MemoryAgent` — retrieves top-`k` passages, builds the "answer only from context" prompt, calls Claude |
| `main.py` | CLI: `ask` (default) and `remember` subcommands |
| `tests/` | `test_memory_store.py` is fully offline (pure Python, no mocks needed at all); `test_agent.py` mocks only the Anthropic client, using a real in-memory store |

## Setup

```bash
pip install -r projects/ai_agents/requirements.txt   # from the repo root
cp projects/ai_agents/.env.example .env               # add your ANTHROPIC_API_KEY
```

## Run it

```bash
# Ask a question (uses the pre-seeded facts about this repo)
python -m projects.ai_agents.agent4_memory_rag.main "What is projects/ai_agents?"

# Teach it something new — persisted to memory_store.json next to this README
python -m projects.ai_agents.agent4_memory_rag.main remember "The repo's license is MIT."
python -m projects.ai_agents.agent4_memory_rag.main "What license does this repo use?"
```

Example output:

```
Q: What is projects/ai_agents?

projects/ai_agents/ contains five educational agent implementations, covering
tool use, ReAct reasoning, multi-agent collaboration, memory/RAG, and planning [1].
```

Set `AI_AGENTS_MEMORY_PATH` (see `.env.example`) to point the store at a different file.

## Run the tests

```bash
python -m pytest projects/ai_agents/agent4_memory_rag/tests/ -v
```

## Things to try next

- Ask a question sharing only common words (like "the", "is") with a stored fact and
  inspect the similarity score — bag-of-words treats every word as equally meaningful,
  so stray overlaps in stop words can nudge the score above zero. Real embedding models
  don't have this problem because they represent *meaning*, not just word counts.
- Swap `_vectorize`/`_cosine_similarity` in `memory_store.py` for a real embeddings call
  (e.g. `client.messages` alternatives or a dedicated embeddings API) and compare
  retrieval quality on synonyms your bag-of-words version misses (e.g. "car" vs.
  "automobile").
- Add a `forget(doc_id)` method to `MemoryStore` and wire it into `main.py`.
