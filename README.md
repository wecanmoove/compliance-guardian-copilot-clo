# Compliance Guardian Copilot — Python Edition

AI-powered SaaS for governance, risk management, compliance, and operational resilience.

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local dev)

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/wecanmoove/Compliance-Guardian-Copilot-clo
cd Compliance-Guardian-Copilot-clo

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Check status
docker-compose ps
curl http://localhost:8000/health
```

### Option 2: Local Python

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL locally (or adjust DATABASE_URL in .env to SQLite)
# Option: Use SQLite (default fallback)

# Run app
python -m uvicorn src.main:app --reload --port 8000
```

## 📚 API Endpoints

### Upload & Analyze Contract
```bash
curl -X POST http://localhost:8000/api/contracts/upload \
  -F "file=@contract.pdf" \
  -F "business_owner=John Doe" \
  -F "department=Legal"
```

Response:
```json
{
  "contract_id": "uuid",
  "file_name": "contract.pdf",
  "highest_risk_level": "high",
  "summary": "Document analyzed: 5 risks identified. Compliance: 60%..."
}
```

### Get Contract Details
```bash
curl http://localhost:8000/api/contracts/{contract_id}
```

### Get Risk Findings
```bash
curl http://localhost:8000/api/contracts/{contract_id}/findings
```

### Chat with Copilot
```bash
# Create conversation
curl -X POST http://localhost:8000/api/conversations/

# Send message
curl -X POST http://localhost:8000/api/conversations/{conv_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "What are the top risks in this contract?"}'
```

## 📊 Features

✅ Document Upload & Analysis
- PDF, Word, TXT, Markdown support
- Automatic text extraction
- OCR-ready (future)

✅ Risk Detection Engine
- 7 predefined compliance rules
- Rule-based analysis (0-100 scoring)
- Customizable rule engine

✅ Policy Compliance Tracking
- Compare against security requirements
- Gap identification
- Compliance scoring

✅ Copilot IA
- Multi-turn conversations
- Context-aware responses
- Cites findings & evidence

✅ Executive Reporting
- Risk summaries
- Action items
- Compliance dashboard

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         FastAPI Backend (Python)             │
├─────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────────┐   │
│  │   API Routes │  │  Copilot Agent   │   │
│  │  - Contracts │  │  (LangGraph RAG) │   │
│  │  - Findings  │  │                  │   │
│  │  - Chat      │  └──────────────────┘   │
│  └──────────────┘                         │
│         ↓                                   │
│  ┌──────────────────────────────────────┐ │
│  │  Services Layer                       │ │
│  │  - Analyzer (Risk rules)             │ │
│  │  - Policy Checker (Gap detection)    │ │
│  │  - Parser (Document extraction)      │ │
│  └──────────────────────────────────────┘ │
│         ↓                                   │
│  ┌──────────────────────────────────────┐ │
│  │  SQLAlchemy ORM + SQLite/PostgreSQL  │ │
│  └──────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## 📁 Project Structure

```
src/
├── main.py              # FastAPI app entry
├── config.py            # Settings
├── db.py                # Database config
├── api/
│   ├── contracts.py     # Contract routes
│   └── conversations.py # Copilot chat
├── models/
│   ├── contracts.py     # Contract entity
│   ├── findings.py      # Risk findings
│   ├── conversations.py # Chat history
│   └── incidents.py     # Incident tracking
├── services/
│   ├── analyzer.py      # Risk detection
│   ├── policy.py        # Policy compliance
│   └── parser.py        # Document extraction
└── utils/
    └── parser.py        # Text extraction

docker-compose.yml       # Services orchestration
Dockerfile              # Container build
requirements.txt        # Dependencies
```

## 🔧 Environment Variables

```
DATABASE_URL=postgresql://user:pass@db:5432/compliance_guardian
REDIS_URL=redis://redis:6379
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEBUG=True
ENVIRONMENT=development
PORT=8000
```

## 📈 Roadmap

### Phase 1 (MVP - ✅ Done)
- Contract upload & analysis
- Risk detection engine
- Policy compliance tracking
- Basic copilot (text-based)

### Phase 2 (Next - Ready)
- Frontend (React + Material UI)
- Advanced RAG (embeddings)
- Custom rule editor
- Vendor risk scoring

### Phase 3 (Future)
- Incident management
- SLA tracking
- Integrations (Teams, Slack, Power BI)
- Reporting dashboard

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src
```

## 🚢 Deployment

### Kubernetes
```bash
kubectl apply -f k8s/
```

### Cloud
- ☁️ AWS ECS (Fargate)
- ☁️ Azure Container Instances
- ☁️ GCP Cloud Run

## 📄 License

MIT License - See LICENSE file

## 🤝 Contributing

See CONTRIBUTING.md

## 📧 Support

- 📖 [Documentation](./docs/)
- 🐛 [Issues](https://github.com/wecanmoove/Compliance-Guardian-Copilot-clo/issues)
- 💬 [Discussions](https://github.com/wecanmoove/Compliance-Guardian-Copilot-clo/discussions)

---

**Built by:** wecanmoove  
**Reference:** https://github.com/wecanmoove/compliance-guardian-app
