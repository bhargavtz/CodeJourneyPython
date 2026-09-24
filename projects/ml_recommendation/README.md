# Skyline Explorer: Machine Learning & Recommendation System

**Tier**: Advanced | **Learning Path**: Machine Learning & Model Serving  
**Difficulty**: ⭐⭐⭐⭐ (Advanced) | **Estimated Time**: 4-5 hours

## Overview

Build an end-to-end machine learning system that demonstrates:
- Exploratory data analysis and feature engineering
- Training multiple ML models (scikit-learn & TensorFlow)
- Model evaluation with comprehensive metrics
- REST API for real-time predictions (FastAPI)
- Model serving with versioning and monitoring
- Integration with Data Pipeline ETL and web application

This project brings together data science workflows with production-ready API serving.

## Learning Objectives

By completing this project, you'll understand:
- ✅ ML pipeline architecture (train → evaluate → serve)
- ✅ Feature engineering for prediction tasks
- ✅ Model training and hyperparameter tuning
- ✅ Model evaluation metrics and validation
- ✅ REST API design for ML models
- ✅ Model persistence and versioning
- ✅ Real-world ML system deployment
- ✅ Monitoring and performance tracking

## Prerequisites

- Completed: `projects/guess_the_number/` (Python basics)
- Completed: `projects/ai_agent_chatbot/` (API patterns)
- Completed: `projects/data_pipeline_etl/` (Data processing)
- Understanding of: statistics, linear algebra, scikit-learn
- Tools: Python 3.8+, scikit-learn, pandas, numpy, fastapi

## Quick Start

### 1. Setup

```bash
cd projects/ml_recommendation
pip install -r requirements.txt

# Generate sample data
python prepare_data.py
```

### 2. Train Models

```bash
# Train recommendation model
python models/train.py

# Evaluate models
python models/evaluate.py
```

### 3. Run API Server

```bash
# Start FastAPI server
python api.py

# API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### 4. Example Requests

```bash
# Get recommendation
curl -X POST "http://localhost:8000/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "n_recommendations": 5}'

# Get prediction explanation
curl -X POST "http://localhost:8000/api/v1/explain" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "item_id": 42}'

# Get model metrics
curl "http://localhost:8000/api/v1/metrics"

# Batch predictions
curl -X POST "http://localhost:8000/api/v1/batch-predict" \
  -H "Content-Type: application/json" \
  -d '{"user_ids": [1, 2, 3, 4, 5]}'
```

### 5. Run Tests

```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

## Project Structure

```
projects/ml_recommendation/
├── README.md                    # This file
├── requirements.txt             # Project dependencies
├── .env.example                # Environment template
├── prepare_data.py             # Generate sample dataset
├── api.py                      # FastAPI application
├── config.py                   # Configuration management
│
├── models/
│   ├── __init__.py
│   ├── train.py               # Model training pipeline
│   ├── evaluate.py            # Model evaluation
│   ├── predict.py             # Inference logic
│   ├── collaborative.py       # Collaborative filtering
│   ├── content_based.py       # Content-based filtering
│   └── ensemble.py            # Ensemble methods
│
├── features/
│   ├── __init__.py
│   ├── engineering.py         # Feature engineering functions
│   ├── scaling.py             # Data normalization
│   └── validation.py          # Data validation rules
│
├── data/
│   ├── raw/                   # Original datasets
│   ├── processed/             # Feature-engineered data
│   └── splits/                # Train/val/test splits
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py         # Model testing
│   ├── test_api.py            # API endpoint tests
│   └── test_features.py       # Feature engineering tests
│
└── notebooks/
    ├── exploration.ipynb      # EDA and analysis
    ├── feature_engineering.ipynb
    └── model_comparison.ipynb
```

## Key Concepts

### 1. **Feature Engineering**
Create meaningful features from raw data:
```python
# Example: Create interaction features
user_features = df.groupby('user_id')['rating'].agg(['mean', 'count', 'std'])
item_popularity = df.groupby('item_id').size()
user_bias = user_features['mean'] - df['rating'].mean()
```

### 2. **Model Training**
Train multiple models and compare:
```python
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity

# Collaborative Filtering with NMF
nmf_model = NMF(n_components=50, random_state=42)
user_factors = nmf_model.fit_transform(user_item_matrix)
item_factors = nmf_model.components_.T
```

### 3. **REST API Endpoints**
Serve predictions via FastAPI:
```python
@app.post("/api/v1/recommend")
async def get_recommendations(request: RecommendationRequest):
    predictions = model.predict(request.user_id)
    return {"recommendations": predictions, "confidence": scores}

@app.get("/api/v1/metrics")
async def get_metrics():
    return {"rmse": 0.85, "mae": 0.72, "ndcg": 0.92}
```

### 4. **Model Evaluation**
Comprehensive metrics for recommendation systems:
```python
# Ranking metrics
ndcg_score = ndcg(true_ratings, predicted_ratings, k=10)
recall_at_k = recall_at_k(true_items, recommended_items, k=10)
precision_at_k = precision_at_k(true_items, recommended_items, k=10)

# Rating metrics
rmse = sqrt(mean_squared_error(true_ratings, predictions))
mae = mean_absolute_error(true_ratings, predictions)
```

### 5. **Model Serving**
Package and serve trained models:
```python
# Save model
import joblib
joblib.dump(model, 'models/trained_model.pkl')

# Load and serve
model = joblib.load('models/trained_model.pkl')
predictions = model.predict(user_features)
```

## Integration Points

### With Data Pipeline ETL
```python
# Load data from pipeline
from projects.data_pipeline_etl import Pipeline

pipeline = ETLPipeline(config)
df = pipeline.extract_and_transform()
# Use df for model training
```

### With AI Agent Chatbot
```python
# Agent can query predictions
agent.register_tool({
    "name": "get_recommendations",
    "function": recommend,
    "description": "Get personalized recommendations"
})
```

### With Full-Stack Web App
```python
# API endpoints consumed by frontend
GET    /api/v1/metrics              # Performance dashboard
POST   /api/v1/recommend            # Get recommendations
POST   /api/v1/explain              # Model explanation
POST   /api/v1/batch-predict        # Batch predictions
```

## Extended Features (Bonus)

- ✨ **Cold Start Handling**: Strategies for new users/items
- ✨ **A/B Testing**: Compare model versions
- ✨ **Real-time Updates**: Incremental model updates
- ✨ **Explainability**: SHAP values for model decisions
- ✨ **Caching**: Redis for faster predictions
- ✨ **Monitoring**: Track model performance over time
- ✨ **Feedback Loop**: Learn from user interactions
- ✨ **Multi-armed Bandit**: Exploration vs. exploitation

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test module
pytest tests/test_models.py -v

# Run with markers
pytest -m "not slow" tests/
```

## Troubleshooting

**Issue**: "Module not found: data_pipeline_etl"
- Solution: Ensure `projects/` is in PYTHONPATH: `export PYTHONPATH="${PYTHONPATH}:/path/to/projects"`

**Issue**: "CUDA/GPU not available"
- Solution: Models will fall back to CPU automatically. For TensorFlow, install CPU version.

**Issue**: "Memory error on large dataset"
- Solution: Use batching or streaming approaches for large files.

## Resources

- 📖 [Scikit-learn ML Documentation](https://scikit-learn.org/stable/)
- 📖 [TensorFlow/Keras Guide](https://www.tensorflow.org/guide)
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 📖 [Recommender Systems](https://en.wikipedia.org/wiki/Recommender_system)
- 🎥 [ML System Design Tutorials](https://www.youtube.com/results?search_query=machine+learning+system+design)

## Learning Path

1. **Complete**: `projects/guess_the_number/` - Python basics
2. **Complete**: `projects/ai_agent_chatbot/` - API & LLMs
3. **Complete**: `projects/data_pipeline_etl/` - Data engineering
4. **Next**: This project (ML & Recommendations)
5. **Then**: `projects/web_api_service/` - Full-stack integration
6. **Advanced**: Deploy and monitor in production

## Next Steps

After completing this project:
- Integrate with web application as backend service
- Add real-time dashboard for model monitoring
- Implement A/B testing for model versions
- Deploy with Docker and Kubernetes
- Scale to handle millions of predictions/day

## Contributing

Have improvements? Submit a PR with:
- New ML models or techniques
- Performance optimizations
- Tests for new features
- Documentation updates

See `CONTRIBUTING.md` for guidelines.
