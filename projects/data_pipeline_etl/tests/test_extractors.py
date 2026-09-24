"""Unit tests for projects.data_pipeline_etl.extractors."""

import sqlite3

import pandas as pd
import pytest

from projects.data_pipeline_etl.extractors import (
    CSVExtractor,
    Extractor,
    JSONExtractor,
    MultiSourceExtractor,
    SQLExtractor,
)


class TestExtractorBaseClass:
    """Test the abstract Extractor base class."""

    def test_extract_is_not_implemented(self):
        with pytest.raises(NotImplementedError):
            Extractor().extract("anything")


class TestCSVExtractor:
    """Test CSVExtractor."""

    def test_extract_reads_a_real_csv_file(self, tmp_path):
        csv_path = tmp_path / "people.csv"
        csv_path.write_text("name,age\nAlice,30\nBob,25\n")

        df = CSVExtractor().extract(str(csv_path))

        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]
        assert df.iloc[0]["name"] == "Alice"

    def test_extract_raises_when_file_missing(self, tmp_path):
        missing_path = tmp_path / "does_not_exist.csv"
        with pytest.raises(FileNotFoundError):
            CSVExtractor().extract(str(missing_path))

    def test_extract_respects_dtype(self, tmp_path):
        csv_path = tmp_path / "people.csv"
        csv_path.write_text("id,age\n1,30\n2,25\n")

        df = CSVExtractor().extract(str(csv_path), dtype={"id": str})

        assert isinstance(df["id"].iloc[0], str)
        assert df["age"].dtype != object  # untouched columns still infer normally


class TestJSONExtractor:
    """Test JSONExtractor."""

    def test_extract_reads_a_real_json_file(self, tmp_path):
        json_path = tmp_path / "people.json"
        json_path.write_text('[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]')

        df = JSONExtractor().extract(str(json_path))

        assert len(df) == 2
        assert set(df.columns) == {"name", "age"}

    def test_extract_raises_when_file_missing(self, tmp_path):
        missing_path = tmp_path / "does_not_exist.json"
        with pytest.raises(FileNotFoundError):
            JSONExtractor().extract(str(missing_path))


class TestSQLExtractor:
    """Test SQLExtractor."""

    def test_extract_requires_a_connection(self):
        with pytest.raises(ValueError):
            SQLExtractor().extract("db", query="SELECT 1", connection=None)

    def test_extract_reads_from_a_real_connection(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE people (name TEXT, age INTEGER)")
        conn.execute("INSERT INTO people VALUES ('Alice', 30), ('Bob', 25)")
        conn.commit()

        df = SQLExtractor().extract("db", query="SELECT * FROM people", connection=conn)

        assert len(df) == 2
        conn.close()


class TestMultiSourceExtractor:
    """Test MultiSourceExtractor."""

    def test_extract_from_sources_concatenates_csv_and_json(self, tmp_path):
        csv_path = tmp_path / "a.csv"
        csv_path.write_text("name,age\nAlice,30\n")
        json_path = tmp_path / "b.json"
        json_path.write_text('[{"name": "Bob", "age": 25}]')

        sources = [
            {"type": "csv", "path": str(csv_path)},
            {"type": "json", "path": str(json_path)},
        ]

        result = MultiSourceExtractor().extract_from_sources(sources)

        assert len(result) == 2
        assert set(result["name"]) == {"Alice", "Bob"}

    def test_extract_from_sources_returns_empty_dataframe_for_no_sources(self):
        result = MultiSourceExtractor().extract_from_sources([])
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_extract_from_sources_raises_on_unknown_type(self):
        with pytest.raises(ValueError):
            MultiSourceExtractor().extract_from_sources([{"type": "xml", "path": "x"}])
