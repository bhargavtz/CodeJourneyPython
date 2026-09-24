"""Offline tests for the from-scratch bag-of-words vector store."""

import json

from projects.ai_agents.agent4_memory_rag.memory_store import MemoryStore


class TestMemoryStoreInMemory:
    def test_add_and_search_ranks_by_relevance(self):
        store = MemoryStore()
        store.add("Python is a popular programming language.", doc_id="python")
        store.add("Bananas are a good source of potassium.", doc_id="banana")

        results = store.search("Tell me about the Python programming language")

        assert len(results) == 1
        doc, score = results[0]
        assert doc.doc_id == "python"
        assert score > 0

    def test_search_excludes_zero_similarity_documents(self):
        store = MemoryStore()
        store.add("Completely unrelated sentence about gardening.")

        results = store.search("quantum computing")

        assert results == []

    def test_search_respects_top_k(self):
        store = MemoryStore()
        for i in range(5):
            store.add(f"Document number {i} about cats and dogs.")

        results = store.search("cats and dogs", top_k=2)

        assert len(results) == 2

    def test_len_reflects_document_count(self):
        store = MemoryStore()
        assert len(store) == 0
        store.add("one")
        store.add("two")
        assert len(store) == 2


class TestMemoryStorePersistence:
    def test_documents_survive_a_reload(self, tmp_path):
        path = tmp_path / "memory.json"

        store = MemoryStore(path=str(path))
        doc_id = store.add("Persisted fact about the repository.")

        assert path.exists()
        reloaded = MemoryStore(path=str(path))
        assert len(reloaded) == 1

        results = reloaded.search("repository fact")
        assert results[0][0].doc_id == doc_id

    def test_persisted_file_is_valid_json(self, tmp_path):
        path = tmp_path / "memory.json"
        store = MemoryStore(path=str(path))
        store.add("Some fact")

        data = json.loads(path.read_text())
        assert isinstance(data, list)
        assert data[0]["text"] == "Some fact"
