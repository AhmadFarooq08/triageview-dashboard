# 🏥 TriageView: AI-Powered Veteran Mental Health Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url-here.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Advanced AI-powered clinical decision support system for veteran mental health triage and risk assessment.**

![TriageView Dashboard](docs/dashboard-preview.png)

## 🎯 Overview

TriageView is a comprehensive clinical decision support dashboard designed specifically for veteran mental health professionals. It combines evidence-based risk assessment algorithms with AI-powered insights to help clinicians prioritize care, identify high-risk cases, and make informed treatment decisions.

### ✨ Key Features

- **🤖 AI-Powered Clinical Insights**: Gemini AI integration for population analysis and individual assessments
- **📊 Risk-Based Prioritization**: Hierarchical scoring system using C-SSRS, PHQ-9, GAD-7, and PCL-5
- **🎯 Real-Time Triage Queue**: Dynamic veteran prioritization with color-coded risk levels
- **📈 Advanced Analytics**: Interactive visualizations for population health monitoring
- **📋 Individual Assessments**: Comprehensive veteran profiles with clinical recommendations
- **📥 Export & Documentation**: Generate clinical reports with AI summaries
- **🔍 Advanced Filtering**: Multi-dimensional filtering for targeted case management

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini AI API key (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AhmadFarooq08/triageview-dashboard.git
   cd triageview-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini AI API key**
   - Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the API key in `triage_dashboard_2.py` (line 38)
   ```python
   GEMINI_API_KEY = "your-api-key-here"
   ```

4. **Run the application**
   ```bash
   streamlit run triage_dashboard_2.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`

## 🏗️ Architecture

### Core Components

```
TriageView/
├── 🎛️ Dashboard Interface (Streamlit)
├── 🤖 AI Integration (Gemini API)
├── 📊 Risk Assessment Engine
├── 📈 Analytics & Visualization
└── 📋 Clinical Documentation
```

### Risk Assessment Algorithm

TriageView uses a hierarchical 6-point risk scoring system:

1. **Level 6 - Critical Behavior**: Recent suicidal behavior (C-SSRS)
2. **Level 5 - Critical Ideation**: Active suicidal ideation with plan
3. **Level 4 - High Self-Harm**: PHQ-9 Q9 positive
4. **Level 3 - High Symptom**: Severe depression/anxiety/PTSD scores
5. **Level 2 - Medium Risk**: Moderate symptoms or compounding factors
6. **Level 1 - Low Risk**: Minimal symptoms

### Data Model

The system processes comprehensive veteran profiles including:

- **Demographics**: Age, gender, military branch, service era
- **Clinical Assessments**: PHQ-9, GAD-7, PCL-5, C-SSRS scores
- **Risk Factors**: Housing, social support, substance use
- **Treatment History**: Previous care, assigned clinicians
- **Social Determinants**: Transportation, emergency contacts

## 🎨 User Interface

### Dashboard Sections

1. **🤖 AI Clinical Overview**
   - Population-level insights and trends
   - Interactive Q&A with clinical AI
   - Evidence-based recommendations

2. **📊 Analytics Overview**
   - Risk level distribution charts
   - Daily intake volume trends
   - Clinician workload analysis

3. **📈 Key Performance Indicators**
   - Real-time metrics and alerts
   - Population health statistics
   - Clinical outcome tracking

4. **🎯 Triage Queue**
   - Prioritized veteran list
   - Quick action buttons
   - Advanced filtering options

5. **🔍 Individual Analysis**
   - Detailed veteran profiles
   - AI-generated assessments
   - Clinical documentation tools

## 🔧 Configuration

### Environment Variables

For production deployment, set these environment variables:

```bash
GEMINI_API_KEY=your-gemini-api-key
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Customization Options

The dashboard supports various customization options:

- **Color Themes**: Modify `COLORS` dictionary in the main file
- **Risk Thresholds**: Adjust scoring criteria in `calculate_risk_score()`
- **AI Prompts**: Customize clinical prompts for specific use cases
- **Data Fields**: Add or modify veteran profile fields

## 📊 Sample Data

The application includes a synthetic dataset generator that creates realistic veteran mental health profiles for demonstration purposes. The data includes:

- **100 synthetic veterans** with realistic demographic distributions
- **Correlated clinical scores** based on evidence-based patterns
- **Diverse risk profiles** representing real-world veteran populations
- **Social determinants** reflecting veteran-specific challenges

> ⚠️ **Note**: All data is synthetic and generated for demonstration purposes only.

## 🤖 AI Integration

### Gemini AI Features

- **Population Analysis**: Comprehensive clinical insights across veteran cohorts
- **Individual Assessments**: Detailed risk analysis for specific veterans
- **Clinical Q&A**: Interactive questioning about population data
- **Report Generation**: AI-enhanced clinical documentation

### API Usage

The application uses Gemini 1.5 Flash model for optimal performance:

```python
# Example AI integration
def generate_ai_summary(data, summary_type="overview"):
    prompt = "Clinical assessment prompt..."
    return call_gemini_api(prompt, "gemini-1.5-flash")
```

## 🚀 Deployment

### Streamlit Community Cloud

1. **Fork this repository** to your GitHub account
2. **Visit [Streamlit Community Cloud](https://share.streamlit.io/)**
3. **Connect your GitHub account**
4. **Deploy the app** by selecting your repository
5. **Set environment variables** in the Streamlit dashboard

### Local Development

```bash
# Install in development mode
pip install -e .

# Run with hot reload
streamlit run triage_dashboard_2.py --server.runOnSave true
```

### Docker Deployment

```bash
# Build the container
docker build -t triageview .

# Run the container
docker run -p 8501:8501 triageview
```

## 📋 Clinical Use Cases

### Primary Applications

1. **Emergency Triage**: Rapid identification of high-risk veterans
2. **Care Coordination**: Efficient assignment of clinical resources
3. **Population Health**: Monitoring trends and outcomes
4. **Quality Improvement**: Data-driven clinical decision making

### Workflow Integration

TriageView integrates seamlessly into existing clinical workflows:

- **Intake Processing**: Automated risk assessment during initial screening
- **Clinical Handoffs**: Comprehensive summaries for care transitions
- **Documentation**: AI-assisted clinical note generation
- **Reporting**: Automated compliance and outcome reporting

## 🔒 Privacy & Security

### Data Protection

- **Synthetic Data Only**: No real patient information in demo version
- **Local Processing**: All calculations performed client-side
- **API Security**: Secure communication with AI services
- **Compliance Ready**: Designed for HIPAA compliance in production

### Security Features

- **Input Validation**: Comprehensive data sanitization
- **Error Handling**: Graceful failure management
- **Rate Limiting**: API usage optimization
- **Session Management**: Secure state handling

## 🤝 Contributing

We welcome contributions from the clinical and technical community!

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```
4. **Make your changes**
5. **Run tests**
   ```bash
   pytest tests/
   ```
6. **Submit a pull request**

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure clinical accuracy in risk assessments

## 📚 Clinical Evidence

### Assessment Tools

- **PHQ-9**: Validated depression screening tool
- **GAD-7**: Anxiety disorder assessment scale  
- **PCL-5**: PTSD Checklist for DSM-5
- **C-SSRS**: Columbia Suicide Severity Rating Scale

### Risk Factors

The dashboard incorporates evidence-based risk factors:

- Mental health symptom severity
- Social determinants of health
- Military service-related factors
- Access to care barriers

## 🆘 Support

### Getting Help

- **Documentation**: Check this README and inline help
- **Issues**: [Report bugs or request features](https://github.com/yourusername/triageview-dashboard/issues)
- **Discussions**: [Community discussions](https://github.com/yourusername/triageview-dashboard/discussions)

### Clinical Support

For clinical questions about risk assessment:

- Review the evidence base for each assessment tool
- Consult with licensed mental health professionals
- Follow your organization's clinical protocols

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Veterans Affairs**: Clinical protocols and evidence base
- **Google AI**: Gemini API for clinical insights
- **Streamlit**: Dashboard framework
- **Clinical Contributors**: Mental health professionals providing guidance

## 📞 Contact

- **Project Lead**: [Your Name](mailto:your.email@example.com)
- **Clinical Advisory**: [Clinical Contact](mailto:clinical@example.com)
- **Technical Support**: [Create an Issue](https://github.com/yourusername/triageview-dashboard/issues)

---

**⚠️ Clinical Disclaimer**: This tool is designed to support clinical decision-making, not replace it. All clinical decisions should be made by licensed healthcare professionals using their clinical judgment and following appropriate protocols.

**🔬 Research Use**: This dashboard is intended for research, training, and demonstration purposes. For clinical use, ensure compliance with all applicable regulations and obtain appropriate approvals.
