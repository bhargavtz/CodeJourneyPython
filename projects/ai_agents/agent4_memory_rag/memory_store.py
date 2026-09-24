"""
A tiny, dependency-free vector store — the "R" in RAG, built from scratch.

Real systems use a proper vector database (Chroma, FAISS, pgvector, Pinecone)
with dense embeddings from a model. Here every document is instead turned
into a bag-of-words vector (a dict of ``{word: count}``) using nothing but
the standard library, and similarity is plain cosine similarity over those
vectors. It is much weaker than real embeddings (no notion of synonyms or
meaning) but it makes the whole retrieval step readable in about 40 lines,
which is the point: once this is clear, swapping in a real embeddings API
is a one-function change (see the README's "Things to try next").
"""

import json
import logging
import math
import re
import uuid
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> List[str]:
    """Lowercase and split text into simple alphanumeric tokens."""
    return _TOKEN_RE.findall(text.lower())


def _vectorize(text: str) -> Dict[str, int]:
    """Turn text into a bag-of-words vector: {token: count}."""
    return dict(Counter(_tokenize(text)))


def _cosine_similarity(vec_a: Dict[str, int], vec_b: Dict[str, int]) -> float:
    """Cosine similarity between two sparse bag-of-words vectors."""
    shared_tokens = vec_a.keys() & vec_b.keys()
    dot_product = sum(vec_a[token] * vec_b[token] for token in shared_tokens)

    norm_a = math.sqrt(sum(count * count for count in vec_a.values()))
    norm_b = math.sqrt(sum(count * count for count in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


@dataclass
class Document:
    """A single stored piece of text plus its precomputed vector."""

    doc_id: str
    text: str
    vector: Dict[str, int] = field(repr=False)

    def to_dict(self) -> Dict[str, object]:
        return {"doc_id": self.doc_id, "text": self.text, "vector": self.vector}

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Document":
        return cls(doc_id=data["doc_id"], text=data["text"], vector=data["vector"])


class MemoryStore:
    """An in-memory (optionally file-persisted) bag-of-words document store."""

    def __init__(self, path: Optional[str] = None):
        """Initialize the store, loading existing documents from `path` if present.

        Args:
            path: Optional JSON file to load from / save to. If None, the
                store is purely in-memory for the life of the process.
        """
        self._path = Path(path) if path else None
        self._documents: Dict[str, Document] = {}

        if self._path and self._path.exists():
            self._load()

    def __len__(self) -> int:
        return len(self._documents)

    def add(self, text: str, doc_id: Optional[str] = None) -> str:
        """Add a document to the store and persist it (if a path is configured).

        Args:
            text: The document text to remember.
            doc_id: Optional explicit id; a UUID is generated if omitted.

        Returns:
            The document's id.
        """
        doc_id = doc_id or uuid.uuid4().hex[:8]
        self._documents[doc_id] = Document(doc_id=doc_id, text=text, vector=_vectorize(text))
        logger.info("Stored document %s (%d chars)", doc_id, len(text))

        if self._path:
            self._save()
        return doc_id

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
        """Return the `top_k` documents most similar to `query`.

        Args:
            query: The search text.
            top_k: Maximum number of results to return.

        Returns:
            A list of (Document, similarity_score) tuples, highest score first.
            Documents with zero similarity are excluded.
        """
        query_vector = _vectorize(query)
        scored = [
            (doc, _cosine_similarity(query_vector, doc.vector)) for doc in self._documents.values()
        ]
        scored = [pair for pair in scored if pair[1] > 0]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return scored[:top_k]

    def _save(self) -> None:
        data = [doc.to_dict() for doc in self._documents.values()]
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, indent=2))

    def _load(self) -> None:
        data = json.loads(self._path.read_text())
        for entry in data:
            doc = Document.from_dict(entry)
            self._documents[doc.doc_id] = doc
        logger.info("Loaded %d documents from %s", len(self._documents), self._path)
