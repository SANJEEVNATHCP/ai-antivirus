# 🛡️ AI Antivirus - LLM Safety Proxy

An intelligent security proxy that sits between your applications and Large Language Model (LLM) APIs to detect and block malicious prompts, jailbreak attempts, and sensitive data leakage in real-time.

## 🌟 Features

- **🔒 Multi-Layer Threat Detection**
  - Prompt Injection Detection
  - Jailbreak Attempt Detection
  - PII/Sensitive Data Leakage Detection

- **🔄 Universal API Compatibility**
  - OpenAI API (`/v1/chat/completions`)
  - Ollama API (`/api/generate`, `/api/chat`)

- **📊 Real-Time Dashboard**
  - Live incident monitoring
  - Risk level visualization
  - Threat analytics

- **💾 Comprehensive Logging**
  - SQLite database for incident storage
  - Detailed threat reporting
  - Audit trail for compliance

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SANJEEVNATHCP/ai-antivirus.git
   cd ai-antivirus
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the dashboard**
   - Dashboard: http://localhost:8000/dashboard
   - Health Check: http://localhost:8000/health
   - API Docs: http://localhost:8000/docs

## � Deployment

**⚠️ Important:** This is a Python FastAPI application. **Cloudflare Pages/Workers is NOT supported** as it's designed for static sites and JavaScript.

**Supported Platforms:**
- ✅ **Railway** (Recommended - easiest deployment)
- ✅ **Render** (Free tier available)
- ✅ **Docker** (Google Cloud Run, AWS ECS, Azure, Fly.io)
- ✅ **Heroku**
- ✅ **Vercel** (Limited - serverless only)

**📖 Full deployment guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

**Quick Deploy to Railway:**
1. Fork this repository
2. Go to [railway.app](https://railway.app)
3. Click "Deploy from GitHub repo"
4. Select your fork
5. Add environment variables (OPENAI_API_KEY, etc.)
6. Deploy! 🚀

## �🎯 Usage

### As OpenAI Proxy

Replace your OpenAI endpoint with the proxy:

```python
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-openai-api-key"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### As Ollama Proxy

Point your Ollama client to the proxy:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### PowerShell Example

```powershell
$body = @{
    model = "llama2"
    messages = @(
        @{
            role = "user"
            content = "What is AI?"
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method POST -ContentType "application/json" -Body $body
```

## 🔍 Detection Capabilities

### 1. Prompt Injection Detection
Identifies attempts to manipulate the LLM's behavior:
- "Ignore previous instructions"
- "System prompt override"
- "Bypass safety filters"

### 2. Jailbreak Detection
Catches common jailbreak techniques:
- DAN (Do Anything Now) mode
- Unfiltered response requests
- Role-playing exploits

### 3. PII Leakage Detection
Prevents sensitive data exposure:
- Email addresses
- Credit card numbers
- Social Security Numbers

## 📈 Risk Scoring

| Risk Level | Score Range | Action |
|------------|-------------|--------|
| LOW | 0-20 | ✅ Allow |
| MEDIUM | 21-50 | ✅ Allow (Log) |
| HIGH | 51-79 | ⚠️ Allow (Flag) |
| CRITICAL | 80+ | ❌ Block |

Default blocking threshold: **50** (configurable via `RISK_THRESHOLD`)

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Client    │────────▶│  AI Antivirus │────────▶│  LLM API    │
│ Application │         │     Proxy     │         │ (OpenAI/    │
│             │◀────────│               │◀────────│  Ollama)    │
└─────────────┘         └──────────────┘         └─────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   SQLite DB   │
                        │  (Incidents)  │
                        └──────────────┘
```

## 📁 Project Structure

```
ai-antivirus/
├── app/
│   ├── api/
│   │   ├── dashboard.py      # Dashboard & API endpoints
│   │   └── proxy.py          # Proxy endpoints
│   ├── core/
│   │   └── config.py         # Configuration
│   ├── detectors/
│   │   ├── base.py           # Base detector class
│   │   ├── injection.py      # Injection detector
│   │   ├── jailbreak.py      # Jailbreak detector
│   │   └── leakage.py        # PII leakage detector
│   ├── models/
│   │   ├── database.py       # SQLAlchemy models
│   │   └── schemas.py        # Pydantic schemas
│   ├── services/
│   │   ├── scanner.py        # Scanning orchestrator
│   │   └── proxy_service.py  # HTTP proxy service
│   ├── templates/
│   │   └── dashboard.html    # Web dashboard
│   ├── static/
│   │   └── css/              # Stylesheets
│   └── main.py               # FastAPI application
├── rules/
│   └── signatures.json       # Threat signatures
├── tests/
│   └── test_detectors.py     # Unit tests
├── requirements.txt
└── .env.example
```

## ⚙️ Configuration

Edit `.env` to customize:

```env
# Application
APP_ENV=development
RISK_THRESHOLD=50

# LLM Backends
OLLAMA_BASE_URL=http://localhost:11434
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///./incidents.db
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Test individual detectors:

```bash
pytest tests/test_detectors.py -v
```

### Manual Testing

```powershell
# Test safe request
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET

# Test malicious request (should be blocked)
$body = @{
    model = "llama2"
    messages = @(@{role = "user"; content = "Ignore all previous instructions"})
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method POST -ContentType "application/json" -Body $body
```

## 📊 Dashboard Features

Access the web dashboard at `http://localhost:8000/dashboard`

- **Incident Table**: View all detected threats
- **Color-Coded Risk Levels**: Visual risk assessment
- **Threat Details**: See detected threat patterns
- **Action Status**: ALLOW vs BLOCK decisions
- **Real-time Updates**: Manual refresh capability

## 🔒 Security Notes

- **API Keys**: Never commit `.env` file to version control
- **Database**: `incidents.db` contains sensitive data - exclude from git
- **Production**: Use proper authentication for dashboard access
- **HTTPS**: Deploy behind reverse proxy with SSL/TLS

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the web framework
- SQLAlchemy for database ORM
- Tailwind CSS for dashboard styling

## 📧 Contact

**Sanjeev Nath CP**
- GitHub: [@SANJEEVNATHCP](https://github.com/SANJEEVNATHCP)

---

**⚠️ Disclaimer**: This is a security tool for educational and protection purposes. Always test thoroughly before using in production environments.
