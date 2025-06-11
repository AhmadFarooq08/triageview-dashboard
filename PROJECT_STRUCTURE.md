# 📁 Project Structure

This document outlines the complete file structure and organization of the TriageView project.

## 🗂️ Directory Overview

```
triageview-dashboard/
├── 📄 README.md                    # Main project documentation
├── 📋 requirements.txt             # Python dependencies
├── 🐍 triage_dashboard_2.py        # Main application file
├── ⚙️ setup.py                     # Automated setup script
├── 🚀 DEPLOYMENT.md                # Deployment instructions
├── 📖 PROJECT_STRUCTURE.md         # This file
├── 📜 LICENSE                      # MIT license
├── 🚫 .gitignore                   # Git ignore rules
├── 🐳 Dockerfile                   # Docker container config
├── 🐙 docker-compose.yml           # Docker Compose setup
├── 🖥️ launch.sh                    # Unix launch script (generated)
├── 🖥️ launch.bat                   # Windows launch script (generated)
├── 📁 .streamlit/                  # Streamlit configuration
│   ├── ⚙️ config.toml              # App configuration
│   └── 🔐 secrets.toml             # API keys (not in git)
├── 📁 .github/                     # GitHub workflows
│   └── 📁 workflows/
│       └── 🔄 streamlit.yml        # CI/CD pipeline
└── 📁 docs/                        # Documentation assets
    └── 🖼️ dashboard-preview.png     # Screenshot for README
```

## 📋 File Descriptions

### Core Application Files

#### `triage_dashboard_2.py`
**Main Streamlit application** containing:
- Dashboard interface and layout
- AI integration with Gemini API
- Risk assessment algorithms
- Data visualization components
- Clinical documentation tools

**Key Functions:**
- `generate_synthetic_data()` - Creates realistic veteran profiles
- `calculate_risk_score()` - Implements hierarchical risk scoring
- `call_gemini_ai()` - Handles AI API communication
- `create_visualizations()` - Generates interactive charts

#### `requirements.txt`
**Python dependencies** for the project:
```txt
streamlit==1.28.2     # Web application framework
pandas==2.1.4         # Data manipulation
numpy==1.24.3         # Numerical computing
plotly==5.17.0        # Interactive visualizations
requests==2.31.0      # HTTP library for API calls
```

#### `setup.py`
**Automated setup script** that:
- Checks Python version compatibility
- Installs dependencies
- Configures API keys
- Creates launch scripts
- Tests installation

### Configuration Files

#### `.streamlit/config.toml`
**Streamlit application settings:**
```toml
[global]
developmentMode = false

[server]
runOnSave = true
port = 8501

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#5B9BD3"          # Medical blue theme
backgroundColor = "#F8F8F8"        # Light gray background
secondaryBackgroundColor = "#FFFFFF"
textColor = "#333333"
font = "sans serif"
```

#### `.streamlit/secrets.toml` (Generated)
**Secure API key storage:**
```toml
GEMINI_API_KEY = "your-api-key-here"
```
> ⚠️ This file is automatically added to `.gitignore` for security

### Docker Configuration

#### `Dockerfile`
**Container configuration** featuring:
- Python 3.9 slim base image
- Optimized layer caching
- Non-root user for security
- Health check endpoint
- Streamlit port exposure

#### `docker-compose.yml`
**Multi-container orchestration:**
- Service definition for TriageView
- Environment variable management
- Volume mounting for data persistence
- Health check configuration
- Restart policies

### Documentation

#### `README.md`
**Comprehensive project documentation** including:
- Project overview and features
- Installation instructions
- Usage examples
- API documentation
- Contributing guidelines
- Clinical evidence base

#### `DEPLOYMENT.md`
**Detailed deployment guide** covering:
- Streamlit Community Cloud deployment
- Docker deployment options
- Cloud platform configurations
- Security best practices
- Troubleshooting guide

#### `PROJECT_STRUCTURE.md`
**This file** - Complete project organization guide

### Development & CI/CD

#### `.github/workflows/streamlit.yml`
**GitHub Actions workflow** for:
- Automated testing on push/PR
- Code quality checks with flake8
- Security scanning with Trivy
- Application startup testing
- Deployment validation

#### `.gitignore`
**Git ignore rules** excluding:
- Python cache files (`__pycache__/`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Secret files (`.streamlit/secrets.toml`)
- Operating system files (`.DS_Store`)
- Build artifacts

### Generated Files

#### `launch.sh` / `launch.bat`
**Platform-specific launch scripts** created by `setup.py`:

**Unix/Mac (`launch.sh`):**
```bash
#!/bin/bash
echo 'Starting TriageView Dashboard...'
streamlit run triage_dashboard_2.py
```

**Windows (`launch.bat`):**
```bat
@echo off
echo Starting TriageView Dashboard...
streamlit run triage_dashboard_2.py
pause
```

## 🏗️ Architecture Overview

### Application Layers

```
┌─────────────────────────┐
│    🎨 Presentation      │ ← Streamlit UI Components
├─────────────────────────┤
│    🧠 AI Integration    │ ← Gemini API Services
├─────────────────────────┤
│    📊 Business Logic    │ ← Risk Assessment Engine
├─────────────────────────┤
│    📁 Data Layer        │ ← Synthetic Data Generation
└─────────────────────────┘
```

### Component Relationships

```
Main App (triage_dashboard_2.py)
├── UI Components
│   ├── Sidebar Filters
│   ├── Analytics Dashboard
│   ├── Triage Queue
│   └── Individual Analysis
├── AI Services
│   ├── Population Summaries
│   ├── Individual Assessments
│   └── Q&A System
├── Risk Engine
│   ├── C-SSRS Processing
│   ├── PHQ-9/GAD-7/PCL-5 Scoring
│   └── Social Determinants
└── Data Management
    ├── Synthetic Data Generator
    ├── Export Functions
    └── Session State
```

## 🔄 Data Flow

### 1. Application Startup
```
setup.py → Install Dependencies → Configure API → Test Installation
```

### 2. Main Application Flow
```
Data Generation → Risk Scoring → UI Rendering → User Interaction
```

### 3. AI Integration Flow
```
User Request → Prompt Generation → Gemini API → Response Processing → UI Display
```

### 4. Deployment Flow
```
GitHub Push → CI/CD Pipeline → Streamlit Cloud → Live Application
```

## 📦 Dependencies

### Production Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive data visualization
- **requests**: HTTP library for API calls

### Development Dependencies (Optional)
- **pytest**: Testing framework
- **flake8**: Code linting
- **black**: Code formatting
- **mypy**: Type checking

## 🔐 Security Considerations

### Sensitive Files (Excluded from Git)
- `.streamlit/secrets.toml` - API keys
- `.env` - Environment variables
- `config.py` - Local configuration
- `api_keys.txt` - Development keys

### Security Best Practices
- API keys stored in secrets, not code
- Input validation for all user inputs
- HTTPS enforcement in production
- Regular dependency updates
- Security scanning in CI/CD

## 🚀 Deployment Targets

### Development
- **Local**: `streamlit run triage_dashboard_2.py`
- **Docker**: `docker-compose up`

### Staging/Production
- **Streamlit Cloud**: Automated deployment from GitHub
- **AWS**: ECS, Fargate, or Lambda
- **Google Cloud**: Cloud Run or App Engine
- **Azure**: Container Instances or App Service

## 📊 Monitoring

### Application Metrics
- User interactions and page views
- AI API usage and response times
- Error rates and performance metrics
- Feature usage analytics

### Health Checks
- **Streamlit**: `/_stcore/health`
- **Application**: Custom health endpoint
- **Dependencies**: Service availability checks

## 🎯 Future Enhancements

### Planned Additions
- `tests/` - Comprehensive test suite
- `data/` - Real data integration
- `models/` - Custom ML models
- `api/` - REST API endpoints
- `docs/` - Extended documentation

### Scalability Considerations
- Database integration for real data
- Caching layer for improved performance
- Load balancing for high availability
- Microservices architecture migration

---

This structure provides a solid foundation for a production-ready clinical decision support system while maintaining simplicity for development and deployment.
