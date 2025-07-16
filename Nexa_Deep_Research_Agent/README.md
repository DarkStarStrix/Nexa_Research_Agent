# 🔬 Nexa Research Agent

> **AI-Powered Research Automation Platform**  
> Generate comprehensive, well-sourced research reports on any topic using advanced LLMs and web search capabilities.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Redis](https://img.shields.io/badge/Redis-7.0-red.svg)](https://redis.io)
[![Stripe](https://img.shields.io/badge/Stripe-Integrated-purple.svg)](https://stripe.com)

---

## **Overview**

Nexa Research Agent is an intelligent research automation platform that transforms simple topic queries into comprehensive, well-structured research reports. Using a sophisticated pipeline of LLM reasoning, web search, and content synthesis, it delivers publication-quality research in minutes.

### **Key Features**

- **Intelligent Planning**: LLM-powered research plan generation with logical topic breakdown
- **Advanced Search**: Exa.ai integration for high-quality web search and content discovery  
- **Iterative Research**: Multi-iteration search loops with reflection and refinement
- **Professional Synthesis**: AI-powered report compilation with proper citations
- **High Performance**: Redis caching, async processing, and rate limiting
- **Flexible Pricing**: Stripe-integrated subscription tiers (Free, Pro, Custom)
- **Enterprise Ready**: Authentication, rate limiting, and comprehensive monitoring

---

## **Architecture**

```mermaid
graph TB
    A[User Query] --> B[Research Planner]
    B --> C[Paragraph Tasks]
    C --> D[Research Engine]
    D --> E[Exa.ai Search]
    D --> F[LLM Reflection]
    E --> F
    F --> D
    D --> G[Report Synthesizer]
    G --> H[Final Report]
    
    I[Redis Cache] --> B
    I --> D
    I --> G
    
    J[Stripe] --> K[Tier Management]
    K --> C
    K --> D
```

### **Data Flow**

1. **Topic → LLM Plan**: OpenRouter models generate structured research plans
2. **Paragraph Fan-out**: Async task distribution for parallel processing  
3. **Research Loop**: Iterative search ↔ reflect cycles (≤ 3 iterations)
4. **Synthesis**: LLM-powered paragraph and report compilation
5. **Caching & Return**: Redis caching with tier-based TTL

---

## **Technology Stack**

| **Component**     | **Technology** | **Purpose**                                       |
|-------------------|----------------|---------------------------------------------------|
| **API Framework** | FastAPI        | High-performance async API                        |
| **LLM Provider**  | OpenRouter     | Multi-model routing (DeepSeek-R1, Claude-3, Qwen) |
| **Search Engine** | Exa.ai         | Neural web search with content extraction         |
| **Cache Layer**   | Redis          | Query caching and rate limiting                   |
| **Database**      | PostgreSQL     | User management and session storage               |
| **Vector DB**     | Qdrant         | Semantic search and embeddings                    |
| **Payments**      | Stripe         | Subscription management and billing               |
| **Validation**    | Pydantic v2    | Runtime type checking and data validation         |
| **Deployment**    | Docker         | Containerized deployment                          |

---

## **Quick Start**

### **Prerequisites**

- Python 3.11+
- Docker & Docker Compose
- Redis, PostgreSQL, Qdrant
- API Keys: OpenRouter, Exa.ai, Stripe

### **1. Clone & Setup**

```bash
git clone https://github.com/your-org/nexa-research-agent.git
cd nexa-research-agent

# Copy environment template
cp .env.example .env
```

### **2. Configure Environment**

Edit `.env` with your API keys:

```bash
# Required API Keys
OPENROUTER_API_KEY=your_openrouter_key
EXA_API_KEY=your_exa_key
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Database URLs (auto-configured with Docker)
REDIS_URL=redis://localhost:6379
POSTGRES_URL=postgresql://user:pass@localhost/nexa
QDRANT_URL=http://localhost:6333
```

### **3. Start Services**

```bash
# Start all services with Docker Compose
docker-compose up -d

# Or run locally using uv package management
uv install
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **4. Verify Installation**

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
```

---

## **API Documentation**

### **Core Endpoints**

#### **Research Query**
```http
POST /api/v1/query
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "topic": "The impact of artificial intelligence on healthcare diagnostics",
  "user_id": "user_123"
}
```

**Response:**
```json
{
  "success": true,
  "report": {
    "topic": "The impact of artificial intelligence on healthcare diagnostics",
    "markdown": "# The Impact of AI on Healthcare Diagnostics\n\n## Executive Summary...",
    "sources": ["https://example.com/source1", "https://example.com/source2"],
    "created_at": "2024-01-15T10:30:00Z",
    "user_id": "user_123",
    "tier": "pro",
    "word_count": 2847
  },
  "cached": false
}
```

#### **Create Subscription**
```http
POST /api/v1/subscribe
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "tier": "pro"
}
```

#### **Health Check**
```http
GET /health
```

### **Interactive Documentation**

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## **Configuration**

### **Model Routing**

Customize LLM models in `config.py`:

```python
MODEL_ROUTING = {
    ModelType.REASONER: "deepseek/deepseek-r1",        # Planning
    ModelType.SEARCHER: "deepseek/deepseek-r1",        # Search queries  
    ModelType.REFLECTOR: "qwen/qwen-2-72b-instruct",   # Result analysis
    ModelType.SUMMARIZER: "anthropic/claude-3-haiku",  # Content synthesis
    ModelType.COMPILER: "anthropic/claude-3-sonnet"    # Final compilation
}
```

## **Development**

### **Project Structure**

```
nexa-research-agent/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration and environment variables
├── api/
│   ├── routes.py           # API endpoints and routing
│   └── deps.py             # Authentication and dependencies
├── core/
│   ├── planner.py          # Research plan generation
│   ├── research.py         # Search and research loops
│   ├── summarizer.py       # Report synthesis
│   └── cache.py            # Redis cache management
├── services/
│   ├── exa_client.py       # Exa.ai search integration
│   ├── openrouter_client.py # LLM client wrapper
│   ├── stripe_client.py    # Stripe payment integration
│   └── user_service.py     # User management
├── schemas/                # Pydantic data models
├── cli/                    # Admin command-line tools
└── tests/                  # Test suite
```

### **Running Tests**

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### **Development Mode**

```bash
# Enable debug mode
export XR_DEBUG=true

# Start with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## **Admin Tools**

### **CLI Management**

```bash
# Flush Redis cache
python -m cli.admin flush-cache

# Create user
python -m cli.admin create-user user_123 user@example.com --tier pro

# Upgrade user tier
python -m cli.admin upgrade-user user_123 custom
```

### **Admin Endpoints**

```bash
# Flush cache (admin only)
POST /api/v1/admin/flush_cache

# Trigger vector DB reindex
POST /api/v1/admin/reindex
```

---

## **Deployment**

### **Docker Production**

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Scale API instances
docker-compose up --scale api=3
```

### **Environment Variables**

**Required for Production:**

```bash
OPENROUTER_API_KEY=your_production_key
EXA_API_KEY=your_production_key
STRIPE_SECRET_KEY=sk_live_your_live_key
REDIS_URL=redis://your-redis-cluster
POSTGRES_URL=postgresql://your-postgres-cluster
```

### **Monitoring & Logging**

- **Health Checks**: `/health` endpoint for load balancer monitoring
- **Metrics**: Built-in FastAPI metrics and request logging
- **Error Tracking**: Structured error logging with correlation IDs

---

## **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Workflow**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure tests pass: `pytest`
5. Commit with conventional commits: `git commit -m "feat: add amazing feature"`
6. Push and create a Pull Request

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Support**

- **Documentation**: [docs.nexa-research.com](https://docs.nexa-research.com)
- **Issues**: [GitHub Issues](https://github.com/your-org/nexa-research-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/nexa-research-agent/discussions)
- **Email**: support@nexa-research.com

---

## **Performance**

- **Response Time**: < 30s for typical research queries
- **Throughput**: 100+ concurrent requests with proper scaling
- **Cache Hit Rate**: 60-80% for popular topics
- **Uptime**: 99.9% SLA with proper infrastructure

---

## **Roadmap**

- [ ] **Q1 2024**: Multi-language support
- [ ] **Q2 2024**: Custom data source integration  
- [ ] **Q3 2024**: Real-time collaborative research
- [ ] **Q4 2024**: Advanced analytics and insights

---

## **Acknowledgments**

- **OpenRouter** for multi-model LLM access
- **Exa.ai** for neural search capabilities
- **Stripe** for seamless payment processing
- **FastAPI** for the excellent async framework
- **The AI Research Community** for inspiration and collaboration

---

<div align="center">

**Built with by the Nexa Research Team**

[Website](https://nexa-research.com) • [Documentation](https://docs.nexa-research.com) • [Blog](https://blog.nexa-research.com)

</div>

---

**Note**: If you encounter dependency resolution issues, you can bypass locking and syncing by running:

```bash
pip install --frozen
```
