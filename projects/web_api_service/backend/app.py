#!/usr/bin/env python3
"""
Final Frontier: Full-Stack Web Application Backend.

FastAPI application integrating:
- AI Agent (from Phase 3 Tier 1)
- Data Pipeline (from Phase 3 Tier 1)
- ML Models (from Phase 3 Tier 2a)

Author: CodeJourney Final Project
License: MIT
"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
import jwt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================================
# Pydantic Models
# ============================================================================

class UserCreate(BaseModel):
    """User creation request."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """User response."""
    id: int
    email: str
    full_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """Login request."""
    email: str
    password: str


class RecommendationRequest(BaseModel):
    """ML recommendation request."""
    user_id: int
    n_recommendations: int = 10


class RecommendationResponse(BaseModel):
    """ML recommendation response."""
    user_id: int
    recommendations: list[int]
    model_type: str
    generated_at: datetime


class ChatMessage(BaseModel):
    """Chat message."""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response."""
    response: str
    session_id: str
    timestamp: datetime


class DataUploadResponse(BaseModel):
    """Data upload response."""
    dataset_id: int
    dataset_name: str
    rows_processed: int
    status: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    services: dict


# ============================================================================
# Mock Database & Services (In production, use SQLAlchemy)
# ============================================================================

# In-memory storage for demo
users_db = {}
predictions_db = []
conversations_db = {}
sessions_counter = 0


class AuthService:
    """Authentication service."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(email: str, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token."""
        if expires_delta is None:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        expire = datetime.utcnow() + expires_delta
        to_encode = {"sub": email, "exp": expire}

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> str:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return email
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


class MLService:
    """Machine learning service."""

    @staticmethod
    async def get_recommendations(user_id: int, n: int = 10) -> list[int]:
        """Get ML recommendations (mock)."""
        # In production, load from Skyline Explorer
        import random
        return random.sample(range(100), min(n, 100))

    @staticmethod
    async def get_metrics() -> dict:
        """Get model metrics."""
        return {
            "precision_at_10": 0.72,
            "recall_at_10": 0.68,
            "ndcg_at_10": 0.81,
            "model_version": "1.0.0"
        }


class AgentService:
    """AI Agent service."""

    @staticmethod
    async def chat(message: str, session_id: Optional[str] = None) -> tuple[str, str]:
        """Chat with AI Agent (mock)."""
        # In production, integrate with Phase 3 Tier 1 Agent
        global sessions_counter

        if session_id is None:
            sessions_counter += 1
            session_id = f"session_{sessions_counter}"

        # Store conversation
        if session_id not in conversations_db:
            conversations_db[session_id] = []

        conversations_db[session_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.utcnow()
        })

        # Generate response (mock)
        response = f"I understood your message: '{message}'. This is a demo response."

        conversations_db[session_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.utcnow()
        })

        return response, session_id


class PipelineService:
    """Data pipeline ETL service."""

    @staticmethod
    async def process_data(file_path: str, dataset_name: str) -> dict:
        """Process data through pipeline (mock)."""
        # In production, integrate with Phase 3 Tier 1 Pipeline
        return {
            "dataset_id": 1,
            "dataset_name": dataset_name,
            "rows_processed": 1000,
            "status": "completed",
            "processed_at": datetime.utcnow()
        }


# ============================================================================
# Dependencies
# ============================================================================

async def get_current_user(token: str = None) -> str:
    """Get current user from token."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    email = AuthService.verify_token(token)
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    return email


# ============================================================================
# Startup/Shutdown
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle."""
    logger.info("🚀 Final Frontier Backend Starting")
    logger.info("✓ AI Agent Service Ready")
    logger.info("✓ ML Models Service Ready")
    logger.info("✓ Data Pipeline Service Ready")

    yield

    logger.info("🛑 Shutting Down")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Final Frontier - Full-Stack AI/ML Platform",
    description="Production-ready SaaS platform integrating AI Agents, ML Models, and Data Pipelines",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health & Diagnostics Routes
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        services={
            "ml_service": "operational",
            "pipeline_service": "operational",
            "agent_service": "operational",
            "database": "operational"
        }
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Final Frontier Backend",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


# ============================================================================
# Authentication Routes
# ============================================================================

@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register new user."""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = AuthService.hash_password(user.password)

    users_db[user.email] = {
        "id": len(users_db) + 1,
        "email": user.email,
        "full_name": user.full_name,
        "password_hash": hashed_password,
        "created_at": datetime.utcnow()
    }

    logger.info(f"User registered: {user.email}")

    return UserResponse(
        id=users_db[user.email]["id"],
        email=user.email,
        full_name=user.full_name,
        created_at=users_db[user.email]["created_at"]
    )


@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Login user and return token."""
    if credentials.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = users_db[credentials.email]

    if not AuthService.verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = AuthService.create_access_token(credentials.email)

    logger.info(f"User logged in: {credentials.email}")

    return TokenResponse(
        access_token=token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_me(token: str = None):
    """Get current user info."""
    email = await get_current_user(token)
    user = users_db[email]

    return UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        created_at=user["created_at"]
    )


# ============================================================================
# ML Routes
# ============================================================================

@app.post("/api/v1/ml/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest, token: str = None):
    """Get ML recommendations."""
    await get_current_user(token)

    recommendations = await MLService.get_recommendations(
        request.user_id,
        request.n_recommendations
    )

    prediction_log = {
        "user_id": request.user_id,
        "recommendations": recommendations,
        "timestamp": datetime.utcnow()
    }
    predictions_db.append(prediction_log)

    return RecommendationResponse(
        user_id=request.user_id,
        recommendations=recommendations,
        model_type="collaborative_filtering",
        generated_at=datetime.utcnow()
    )


@app.get("/api/v1/ml/metrics")
async def get_metrics(token: str = None):
    """Get model metrics."""
    await get_current_user(token)
    return await MLService.get_metrics()


# ============================================================================
# Chat Routes
# ============================================================================

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatMessage, token: str = None):
    """Chat with AI Agent."""
    email = await get_current_user(token)

    response, session_id = await AgentService.chat(
        request.message,
        request.session_id
    )

    return ChatResponse(
        response=response,
        session_id=session_id,
        timestamp=datetime.utcnow()
    )


@app.get("/api/v1/chat/history/{session_id}")
async def get_chat_history(session_id: str, token: str = None):
    """Get chat conversation history."""
    await get_current_user(token)

    if session_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"session_id": session_id, "messages": conversations_db[session_id]}


# ============================================================================
# Data Pipeline Routes
# ============================================================================

@app.post("/api/v1/data/upload", response_model=DataUploadResponse)
async def upload_data(
    file_path: str = "/tmp/sample.csv",
    dataset_name: str = "uploaded_data",
    token: str = None
):
    """Upload and process data."""
    await get_current_user(token)

    result = await PipelineService.process_data(file_path, dataset_name)

    logger.info(f"Data processed: {dataset_name}")

    return DataUploadResponse(**result)


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

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
