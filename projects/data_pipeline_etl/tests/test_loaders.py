"""Unit tests for projects.data_pipeline_etl.loaders."""

import sqlite3

import pandas as pd
import pytest

from projects.data_pipeline_etl.loaders import (
    CSVLoader,
    JSONLoader,
    Loader,
    MultiTargetLoader,
    SQLiteLoader,
)


class TestLoaderBaseClass:
    def test_load_is_not_implemented(self):
        with pytest.raises(NotImplementedError):
            Loader().load(pd.DataFrame(), "target")


class TestCSVLoader:
    def test_writes_a_real_csv_file(self, tmp_path):
        target = tmp_path / "out" / "people.csv"
        df = pd.DataFrame({"name": ["Alice", "Bob"]})

        CSVLoader().load(df, str(target))

        assert target.exists()
        assert pd.read_csv(target)["name"].tolist() == ["Alice", "Bob"]

    def test_creates_parent_directories(self, tmp_path):
        target = tmp_path / "nested" / "dir" / "out.csv"
        CSVLoader().load(pd.DataFrame({"a": [1]}), str(target))
        assert target.exists()


class TestSQLiteLoader:
    def test_writes_to_a_real_sqlite_file(self, tmp_path):
        target = tmp_path / "pipeline.db"
        df = pd.DataFrame({"name": ["Alice", "Bob"]})

        SQLiteLoader().load(df, str(target), table_name="people")

        conn = sqlite3.connect(str(target))
        rows = conn.execute("SELECT name FROM people").fetchall()
        conn.close()
        assert rows == [("Alice",), ("Bob",)]


class TestJSONLoader:
    def test_writes_a_real_json_file(self, tmp_path):
        target = tmp_path / "out.json"
        df = pd.DataFrame({"name": ["Alice"]})

        JSONLoader().load(df, str(target))

        assert target.exists()
        assert "Alice" in target.read_text()


class TestMultiTargetLoader:
    def test_loads_to_multiple_targets(self, tmp_path):
        df = pd.DataFrame({"name": ["Alice"]})
        targets = [
            {"type": "csv", "path": str(tmp_path / "out.csv")},
            {"type": "json", "path": str(tmp_path / "out.json")},
        ]

        MultiTargetLoader().load_to_targets(df, targets)

        assert (tmp_path / "out.csv").exists()
        assert (tmp_path / "out.json").exists()

    def test_raises_on_unknown_target_type(self, tmp_path):
        with pytest.raises(ValueError):
            MultiTargetLoader().load_to_targets(
                pd.DataFrame({"a": [1]}), [{"type": "xml", "path": str(tmp_path / "x")}]
            )
