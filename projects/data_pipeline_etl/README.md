# Mountain Peak: Data Pipeline & ETL

**Tier**: Intermediate | **Learning Path**: Data Engineering & Processing  
**Difficulty**: ⭐⭐⭐ (Intermediate) | **Estimated Time**: 3-4 hours

## Overview

Build a production-ready ETL (Extract, Transform, Load) pipeline that demonstrates:
- Extracting data from multiple sources (CSV, JSON, databases)
- Validating and cleaning messy data
- Transforming and enriching data
- Loading into target systems (SQLite, CSV, API)
- Comprehensive error handling and logging

This project teaches real-world data engineering patterns used in production systems.

## Learning Objectives

By completing this project, you'll understand:
- ✅ ETL pipeline architecture and design patterns
- ✅ Data extraction from heterogeneous sources
- ✅ Data validation and quality checks
- ✅ Data transformation and enrichment
- ✅ Incremental vs. full load strategies
- ✅ Error handling and data recovery
- ✅ Monitoring and logging pipelines

## Prerequisites

- Completed: `projects/guess_the_number/` (Python basics)
- Completed: `libraries/Pandas/` (Data manipulation)
- Understanding of: CSV/JSON formats, databases, file I/O
- Tools: Python 3.8+, pandas, sqlite3

## Quick Start

### 1. Setup

Run everything from the **repository root** (not from inside this folder), so the
`projects` package resolves — see `CLAUDE.md` for why.

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r projects/data_pipeline_etl/requirements.txt
```

There's no separate sample-data script to run first: `main.py` generates a small sample
`employees.csv` under `data/raw/` itself on every run if one doesn't already exist.

### 2. Run the Pipeline

```bash
# Run full pipeline
python -m projects.data_pipeline_etl.main

# Run with verbose logging
python -m projects.data_pipeline_etl.main --debug

# Run specific stage
python -m projects.data_pipeline_etl.main --extract
python -m projects.data_pipeline_etl.main --transform
python -m projects.data_pipeline_etl.main --load

# Run tests
python -m pytest projects/data_pipeline_etl/tests/ -v
```

### 3. Example Output

```
$ python -m projects.data_pipeline_etl.main

[INFO] Initializing Data Pipeline...
[INFO] Stage: EXTRACT
[INFO] Extracted 8 rows
[INFO] Stage: TRANSFORM
[INFO] Removed 1 duplicate rows
[INFO] Converted age to int64
[INFO] Stage: LOAD
[INFO] Loaded 8 rows to CSV: data/processed/output.csv
[INFO] Loaded 8 rows to SQLite: data/sql/pipeline.db/employees
[INFO] Pipeline completed successfully

Pipeline Execution Summary:
  Status: SUCCESS
  Rows Extracted: 8
  Rows Transformed: 8
  Rows Loaded: 8
  Success Rate: 100.0%
```

`data/` is created next to wherever you run the command from and is gitignored — delete
it any time and the pipeline will regenerate its sample input on the next run.

## Project Structure

```
projects/data_pipeline_etl/
├── README.md                    # This file
├── requirements.txt             # Project dependencies
├── main.py                      # Pipeline entry point + SamplePipeline example
├── pipeline.py                  # Core Pipeline base class (extract/transform/load + stats)
├── extractors.py                # Data extraction modules (CSV, JSON, SQL, multi-source)
├── transformers.py              # Data transformation logic (dedupe, missing values, types, ...)
├── loaders.py                   # Data loading modules (CSV, SQLite, JSON, multi-target)
└── tests/
    ├── test_pipeline.py         # Pipeline base-class tests
    ├── test_extractors.py       # Extractor tests
    ├── test_transformers.py     # Transformer tests
    └── test_loaders.py          # Loader tests
```

## Key Concepts

### 1. **Extract Phase**
Read data from multiple sources:
```python
# From CSV
df = pd.read_csv("customers.csv")

# From JSON
df = pd.read_json("orders.json")

# From Database
df = pd.read_sql("SELECT * FROM users", conn)
```

### 2. **Transform Phase**
Clean, validate, and enrich data:
```python
# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df["email"].fillna("unknown@example.com", inplace=True)

# Validate data
assert df["age"].min() >= 0
assert df["age"].max() <= 150

# Enrich data
df["year"] = pd.to_datetime(df["date"]).dt.year
```

### 3. **Load Phase**
Write data to target systems:
```python
# To CSV
df.to_csv("output.csv", index=False)

# To SQLite
df.to_sql("customers", conn, if_exists="replace")

# To API (POST)
for idx, row in df.iterrows():
    requests.post("api.example.com/data", json=row.to_dict())
```

### 4. **Error Handling**
Handle data issues gracefully:
```python
try:
    df = extract_data()
    df = transform_data(df)
except ValueError as e:
    logger.error(f"Validation failed: {e}")
    df = load_default_data()  # Fallback
finally:
    save_pipeline_log()
```

### 5. **Configuration**
`SamplePipeline` (in `main.py`) takes a plain config dict naming its sources and targets —
see `create_sample_data()` for the shape it expects:
```python
config = {
    "sources": [{"type": "csv", "path": "data/raw/employees.csv", "options": {}}],
    "targets": [
        {"type": "csv", "path": "data/processed/output.csv"},
        {"type": "sqlite", "path": "data/sql/pipeline.db", "options": {"table_name": "employees"}},
    ],
}
```

## Extended Features (Bonus)

- ✨ **Incremental Loading**: Only load new/changed data (delta loads)
- ✨ **Data Quality Metrics**: Track data quality scores
- ✨ **Retry Logic**: Automatic retry on transient failures
- ✨ **Scheduling**: Use Airflow/APScheduler for scheduled runs
- ✨ **Notifications**: Slack/email alerts for failures
- ✨ **Performance Profiling**: Track pipeline execution time
- ✨ **Data Lineage**: Track data transformation history

## Testing

```bash
# Run all tests (from the repo root)
python -m pytest projects/data_pipeline_etl/tests/ -v

# Run with coverage
python -m pytest projects/data_pipeline_etl/tests/ --cov=projects.data_pipeline_etl --cov-report=html

# Run one test class
python -m pytest projects/data_pipeline_etl/tests/test_pipeline.py::TestPipelineRun -v
```

## Troubleshooting

**Issue**: "No such file or directory: data/raw/employees.csv"
- Solution: this shouldn't happen in normal use — `main.py`'s `create_sample_data()`
  regenerates that file on every run. If you deleted `data/` mid-run, just run the
  pipeline again.

**Issue**: "sqlite3.IntegrityError: UNIQUE constraint failed"
- Solution: Clear database first: `rm data/sql/pipeline.db`

**Issue**: "pandas memory error on large files"
- Solution: Process in batches using `chunksize` parameter in `read_csv`

## Resources

- 📖 [Pandas Documentation](https://pandas.pydata.org/docs/)
- 📖 [SQLite Documentation](https://www.sqlite.org/docs.html)
- 📖 [ETL Best Practices](https://en.wikipedia.org/wiki/Extract,_transform,_load)
- 🎥 [Data Pipeline Tutorials](https://www.youtube.com/results?search_query=etl+pipeline)

## Learning Path

1. **Complete**: `projects/guess_the_number/` - Python basics
2. **Complete**: `projects/ai_agent_chatbot/` - AI/LLMs
3. **Next**: This project (Data Pipeline & ETL)
4. **Then**: `projects/ml_recommendation/` - Machine learning
5. **Advanced**: `projects/web_api_service/` - Full-stack application

## Next Steps

After completing this project:
- Build custom extractors for your data sources
- Implement incremental loading for efficiency
- Deploy pipeline on schedule (Airflow, Cron)
- Add data quality monitoring
- Scale to handle big data (PySpark)

## Contributing

Have improvements? Submit a PR with:
- New feature or bug fix
- Tests for new functionality
- Documentation updates

See `CONTRIBUTING.md` for guidelines.
