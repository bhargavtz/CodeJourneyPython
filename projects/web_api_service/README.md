# Final Frontier: Full-Stack AI/ML Web Application

**Tier**: Expert | **Learning Path**: Full-Stack Development & System Architecture  
**Difficulty**: ⭐⭐⭐⭐⭐ (Expert) | **Estimated Time**: 5-6 hours

## Overview

Build a production-ready, full-stack SaaS platform that integrates:
- **AI Agent** (from Phase 3 Tier 1): Natural language interface for data exploration
- **Data Pipeline** (from Phase 3 Tier 1): ETL for data processing
- **ML Models** (from Phase 3 Tier 2a): Recommendation and prediction engine
- **Web API** (FastAPI): Async REST API with authentication and business logic
- **Web Frontend**: Interactive dashboard with real-time features
- **Database**: Persistent data storage with SQLite/PostgreSQL
- **Containerization**: Docker for reproducible deployments

This is the capstone project demonstrating real-world software engineering.

## Learning Objectives

By completing this project, you'll master:
- ✅ Full-stack application architecture
- ✅ REST API design with FastAPI
- ✅ User authentication (JWT tokens, password security)
- ✅ Database design with SQLAlchemy ORM
- ✅ Microservice integration patterns
- ✅ Frontend-backend communication
- ✅ Containerization with Docker
- ✅ API security and rate limiting
- ✅ Error handling and logging
- ✅ Testing strategies (unit, integration, E2E)

## Prerequisites

- Completed all Phase 3 Tier 1 & 2 projects
- Understanding of: REST APIs, databases, async Python, web security
- Tools: Python 3.8+, PostgreSQL (optional), Docker, Git

## Quick Start

### 1. Setup

```bash
cd projects/web_api_service

# Install dependencies
pip install -r requirements.txt

# Setup database
python -m database.init

# Create environment file
cp .env.example .env
# Edit .env with your configuration
```

### 2. Run with Docker (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### 3. Run Locally

```bash
# Start FastAPI backend
python backend/app.py
# Server runs at http://localhost:8000

# In another terminal, start simple HTTP server for frontend
cd frontend
python -m http.server 3000

# Open browser at http://localhost:3000
```

### 4. API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Example Workflows

#### Register & Login
```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123"}'
# Returns: {"access_token": "eyJ0..."}
```

#### Get ML Recommendations
```bash
curl -X POST "http://localhost:8000/api/v1/ml/recommend" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"n_recommendations":5}'
```

#### Chat with AI Agent
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message":"What are my recommendations?","session_id":"abc123"}'
```

#### Upload and Process Data
```bash
curl -X POST "http://localhost:8000/api/v1/data/upload" \
  -H "Authorization: Bearer <token>" \
  -F "file=@data.csv" \
  -F "dataset_name=mydata"
```

## Project Structure

```
projects/web_api_service/
├── README.md                    # This file
├── requirements.txt             # Dependencies
├── requirements-dev.txt         # Development dependencies
├── .env.example                # Environment template
├── docker-compose.yml          # Multi-container orchestration
├── Dockerfile                  # Backend container image
│
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── dependencies.py        # Dependency injection
│   │
│   ├── routes/
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── ml.py             # ML prediction endpoints
│   │   ├── data.py           # Data management
│   │   ├── chat.py           # AI Agent chat
│   │   └── health.py         # Health check
│   │
│   ├── models/
│   │   ├── user.py           # User database model
│   │   ├── prediction.py      # Prediction logs
│   │   ├── dataset.py        # Dataset metadata
│   │   └── conversation.py   # Chat history
│   │
│   ├── services/
│   │   ├── auth_service.py   # Authentication logic
│   │   ├── ml_service.py     # ML model orchestration
│   │   ├── pipeline_service.py # ETL coordination
│   │   ├── agent_service.py  # AI Agent integration
│   │   └── data_service.py   # Data operations
│   │
│   ├── middleware/
│   │   ├── auth.py           # JWT authentication
│   │   ├── logging.py        # Request logging
│   │   └── error_handler.py  # Error handling
│   │
│   └── tests/
│       ├── test_auth.py      # Auth tests
│       ├── test_routes.py    # API route tests
│       ├── test_services.py  # Service tests
│       └── test_e2e.py       # End-to-end tests
│
├── frontend/
│   ├── index.html             # Main page
│   ├── css/
│   │   └── styles.css         # Application styles
│   ├── js/
│   │   ├── app.js            # Main app logic
│   │   ├── api.js            # API client
│   │   ├── auth.js           # Auth helpers
│   │   └── chat.js           # Chat interface
│   └── pages/
│       ├── dashboard.html    # Analytics dashboard
│       ├── predictions.html  # ML predictions
│       ├── chat.html         # AI Agent chat
│       ├── upload.html       # Data upload
│       └── settings.html     # User settings
│
├── database/
│   ├── __init__.py
│   ├── models.py             # SQLAlchemy models
│   ├── schema.sql            # Database schema
│   └── init.py               # Database initialization
│
├── .github/workflows/
│   ├── test.yml             # Test on push
│   ├── deploy.yml           # Deploy on release
│   └── security.yml         # Security scanning
│
└── docs/
    ├── API.md               # API documentation
    ├── ARCHITECTURE.md      # System design
    ├── DEPLOYMENT.md        # Deployment guide
    └── TROUBLESHOOTING.md   # Common issues
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    WEB BROWSER                          │
│                  (Frontend - Vue/Vanilla JS)            │
├─────────────────────────────────────────────────────────┤
│                    HTTP/WebSocket                       │
├─────────────────────────────────────────────────────────┤
│               FASTAPI REST API (Uvicorn)               │
│  Routes: /auth, /ml, /data, /chat, /health             │
├──────────────┬──────────────┬──────────────┬────────────┤
│ Auth Service │ ML Service   │ Pipeline SVC │ Agent SVC  │
│  (JWT, Pass) │ (Models API) │   (ETL)      │ (Chat LLM) │
├──────────────┴──────────────┴──────────────┴────────────┤
│              EXTERNAL SERVICES                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │ML Models │ │Pipelines │ │AI Agent  │ │Claude API  │ │
│  │(Skyline) │ │(Mountain)│ │(River)   │ │ (LLM)      │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
├─────────────────────────────────────────────────────────┤
│                 DATABASE (PostgreSQL)                   │
│  Tables: users, predictions, datasets, conversations   │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### 1. **Authentication & Security**
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- API key management

### 2. **ML Model Integration**
- Load trained models from Skyline Explorer
- Real-time predictions
- Batch processing
- Model versioning

### 3. **Data Pipeline Integration**
- Trigger ETL jobs on demand
- Monitor pipeline execution
- Error handling and recovery
- Result persistence

### 4. **AI Agent Chat**
- Multi-turn conversations
- Context awareness
- Tool use integration
- Session management

### 5. **Frontend Dashboard**
- Real-time updates (WebSockets)
- Data visualization
- User-friendly interface
- Responsive design

### 6. **API Features**
- Automatic documentation (Swagger)
- Request validation
- Error handling
- Rate limiting
- CORS configuration

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=html

# Specific test file
pytest tests/test_auth.py -v

# Integration tests
pytest tests/test_e2e.py -v
```

## Deployment

### Local Docker
```bash
docker-compose up -d
```

### Production Deployment
- Use environment variables for secrets
- Enable HTTPS/SSL
- Configure reverse proxy (Nginx)
- Use PostgreSQL instead of SQLite
- Enable monitoring and logging
- Setup CI/CD pipeline

See `DEPLOYMENT.md` for detailed instructions.

## Troubleshooting

**Issue**: "Module not found: data_pipeline_etl"
- Ensure PYTHONPATH includes projects directory
- `export PYTHONPATH="${PYTHONPATH}:/path/to/projects"`

**Issue**: "Database connection failed"
- Check PostgreSQL is running
- Verify connection string in .env
- Run `python -m database.init`

**Issue**: "ML models not found"
- Train models first: `cd ../ml_recommendation && python models/train.py`
- Verify models/ directory exists

## Resources

- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 📖 [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- 📖 [Docker Guide](https://docs.docker.com/)
- 📖 [JWT Authentication](https://tools.ietf.org/html/rfc7519)
- 📖 [REST API Best Practices](https://restfulapi.net/)

## Learning Path Completion

1. ✅ `projects/guess_the_number/` - Python basics
2. ✅ `projects/ai_agent_chatbot/` - AI/LLMs
3. ✅ `projects/data_pipeline_etl/` - Data engineering
4. ✅ `projects/ml_recommendation/` - ML & APIs
5. ✅ `projects/web_api_service/` - Full-stack integration

**Congratulations!** You've completed the entire CodeJourneyPython learning path!

## Next Steps

- Deploy to cloud (AWS, GCP, Azure, Heroku)
- Add more features (notifications, advanced analytics, etc.)
- Scale to handle high traffic
- Implement advanced security measures
- Monitor and optimize performance
- Build mobile app version

## Contributing

Have improvements? Submit a PR with:
- New features or bug fixes
- Performance optimizations
- Security enhancements
- Documentation improvements

See `CONTRIBUTING.md` for guidelines.
