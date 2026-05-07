#!/usr/bin/env python3
"""
FastAPI REST API for ML recommendation system.

Serves trained models via HTTP endpoints.

Author: CodeJourney ML Project
License: MIT
"""

import logging
import os
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Initialize FastAPI app
app = FastAPI(
    title="ML Recommendation API",
    description="REST API for personalized recommendations",
    version="0.1.0"
)

# Global model storage
models = {}


class RecommendationRequest(BaseModel):
    """Request model for recommendations."""
    user_id: int
    n_recommendations: int = 10
    model_type: str = "collaborative"  # collaborative, content, hybrid


class RecommendationResponse(BaseModel):
    """Response model for recommendations."""
    user_id: int
    recommendations: List[int]
    scores: Optional[List[float]] = None
    model_type: str


class MetricsResponse(BaseModel):
    """Response model for metrics."""
    precision_at_10: float
    recall_at_10: float
    ndcg_at_10: float
    mrr: float
    map: float
    evaluated_users: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    models_loaded: int


@app.on_event("startup")
async def load_models():
    """Load trained models on startup."""
    global models

    models_dir = Path("models")

    if models_dir.exists():
        try:
            # Load collaborative filtering model
            cf_path = models_dir / "collaborative_filtering.pkl"
            if cf_path.exists():
                models['collaborative'] = joblib.load(cf_path)
                logger.info("Loaded collaborative filtering model")

            # Load content-based model
            cb_path = models_dir / "content_based.pkl"
            if cb_path.exists():
                models['content'] = joblib.load(cb_path)
                logger.info("Loaded content-based model")

            # Load hybrid model
            hybrid_path = models_dir / "hybrid_recommender.pkl"
            if hybrid_path.exists():
                models['hybrid'] = joblib.load(hybrid_path)
                logger.info("Loaded hybrid model")

        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            logger.info("Models will be trained on first request")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        models_loaded=len(models)
    )


@app.post("/api/v1/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get personalized recommendations for user.

    Args:
        request: Recommendation request with user_id and parameters

    Returns:
        Recommendation response with suggested items
    """
    model_type = request.model_type

    if model_type not in models:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_type}' not found. Available: {list(models.keys())}"
        )

    try:
        model = models[model_type]
        recommendations = model.predict(request.user_id, request.n_recommendations)

        return RecommendationResponse(
            user_id=request.user_id,
            recommendations=recommendations.tolist(),
            model_type=model_type
        )

    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@app.get("/api/v1/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Get model performance metrics.

    Returns:
        Current model metrics (mocked values for demo)
    """
    # In production, these would be loaded from cached metrics
    return MetricsResponse(
        precision_at_10=0.72,
        recall_at_10=0.68,
        ndcg_at_10=0.81,
        mrr=0.85,
        map=0.75,
        evaluated_users=20
    )


@app.post("/api/v1/batch-predict")
async def batch_predict(user_ids: List[int], n_recommendations: int = 5):
    """
    Get recommendations for multiple users.

    Args:
        user_ids: List of user IDs
        n_recommendations: Number of recommendations per user

    Returns:
        Dictionary with recommendations for each user
    """
    if len(user_ids) > 100:
        raise HTTPException(
            status_code=400,
            detail="Batch size limited to 100 users"
        )

    try:
        model = models.get('collaborative')
        if not model:
            raise HTTPException(
                status_code=404,
                detail="No model available for batch prediction"
            )

        results = {}
        for user_id in user_ids:
            recommendations = model.predict(user_id, n_recommendations)
            results[str(user_id)] = recommendations.tolist()

        return {"batch_results": results, "count": len(results)}

    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.post("/api/v1/explain")
async def explain_recommendation(user_id: int, item_id: int):
    """
    Explain why an item was recommended (placeholder).

    Args:
        user_id: User ID
        item_id: Item ID

    Returns:
        Explanation of recommendation
    """
    return {
        "user_id": user_id,
        "item_id": item_id,
        "explanation": f"This item is recommended based on similar users' preferences",
        "confidence": 0.87,
        "factors": ["user_similarity", "rating_similarity", "popularity"]
    }


@app.get("/api/v1/models")
async def list_models():
    """List available models."""
    return {
        "available_models": list(models.keys()),
        "count": len(models)
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn

    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
