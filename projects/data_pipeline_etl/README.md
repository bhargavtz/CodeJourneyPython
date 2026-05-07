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

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Prepare sample data
python setup_sample_data.py
```

### 2. Run the Pipeline

```bash
# Run full pipeline
python main.py

# Run with verbose logging
DEBUG=1 python main.py

# Run specific stage
python main.py --extract
python main.py --transform
python main.py --load

# Run tests
pytest tests/ -v
```

### 3. Example Output

```
$ python main.py

[INFO] Starting ETL Pipeline
[INFO] Stage: EXTRACT
[INFO] Extracted 10,000 rows from customers.csv
[INFO] Extracted 5,423 rows from orders.json
[INFO] Stage: TRANSFORM
[INFO] Validating customer data...
[INFO] Found 42 invalid emails - flagging for review
[INFO] Enriching customer data with geography...
[INFO] Stage: LOAD
[INFO] Loading 15,381 rows to SQLite
[INFO] Pipeline completed successfully
[INFO] Summary: Processed 15,381 rows in 3.2 seconds
```

## Project Structure

```
projects/data_pipeline_etl/
├── README.md                    # This file
├── requirements.txt             # Project dependencies
├── main.py                      # Pipeline entry point
├── pipeline.py                  # Core pipeline logic
├── extractors.py               # Data extraction modules
├── transformers.py             # Data transformation logic
├── loaders.py                  # Data loading modules
├── validators.py               # Data validation rules
├── config.py                   # Configuration management
├── setup_sample_data.py        # Generate sample datasets
├── data/
│   ├── raw/                    # Input data (raw)
│   ├── processed/              # Output data (processed)
│   └── sql/                    # Database files
├── tests/
│   ├── test_pipeline.py        # Pipeline tests
│   ├── test_extractors.py      # Extractor tests
│   ├── test_transformers.py    # Transformer tests
│   └── test_loaders.py         # Loader tests
└── notebooks/
    └── etl_walkthrough.ipynb   # Interactive tutorial
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
Manage pipeline settings:
```python
# config.py
config = {
    "extractors": ["customers.csv", "orders.json"],
    "transformers": ["deduplicate", "validate_emails"],
    "loaders": ["sqlite", "csv"],
    "batch_size": 1000,
    "error_handling": "skip_invalid_rows"
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
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test
pytest tests/test_pipeline.py::TestExtract::test_read_csv -v

# Run with markers
pytest -m "not slow" tests/
```

## Troubleshooting

**Issue**: "No such file or directory: data/raw/customers.csv"
- Solution: Run `python setup_sample_data.py` to generate sample data

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
