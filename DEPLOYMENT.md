# 🚀 Deployment Guide

This guide provides step-by-step instructions for deploying TriageView on various platforms.

## 📋 Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account with repository access
- [ ] Gemini AI API key ([Get one free here](https://makersuite.google.com/app/apikey))
- [ ] Internet connection for dependency installation

## 🌐 Streamlit Community Cloud (Recommended)

### Step 1: Prepare Your Repository

1. **Fork or create the repository**
   ```bash
   git clone https://github.com/yourusername/triageview-dashboard.git
   cd triageview-dashboard
   ```

2. **Update the API key** (temporarily for testing)
   - Open `triage_dashboard_2.py`
   - Update line 38 with your API key:
   ```python
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

3. **Commit and push to GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment setup"
   git push origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Visit [Streamlit Community Cloud](https://share.streamlit.io/)**

2. **Sign in with GitHub**

3. **Click "New app"**

4. **Configure deployment:**
   - **Repository**: `yourusername/triageview-dashboard`
   - **Branch**: `main`
   - **Main file path**: `triage_dashboard_2.py`
   - **App URL**: Choose your custom URL

5. **Advanced Settings** (Optional):
   - **Python version**: `3.9`
   - **Environment variables**: Add `GEMINI_API_KEY` for security

6. **Click "Deploy!"**

### Step 3: Secure Your API Key (Recommended)

1. **Remove API key from code**:
   ```python
   GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
   ```

2. **Add to Streamlit secrets**:
   - Go to your app settings
   - Add under "Secrets":
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

## 🐳 Docker Deployment

### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/triageview-dashboard.git
   cd triageview-dashboard
   ```

2. **Set environment variables**
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

3. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Open browser to `http://localhost:8501`

### Option 2: Docker Build and Run

1. **Build the image**
   ```bash
   docker build -t triageview .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 -e GEMINI_API_KEY="your-api-key" triageview
   ```

## ☁️ Cloud Platform Deployment

### AWS ECS/Fargate

1. **Build and push to ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
   docker build -t triageview .
   docker tag triageview:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/triageview:latest
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/triageview:latest
   ```

2. **Create ECS task definition**
   ```json
   {
     "family": "triageview",
     "containerDefinitions": [
       {
         "name": "triageview",
         "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/triageview:latest",
         "portMappings": [
           {
             "containerPort": 8501,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "GEMINI_API_KEY",
             "value": "your-api-key"
           }
         ]
       }
     ]
   }
   ```

### Google Cloud Run

1. **Build and deploy**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/triageview
   gcloud run deploy --image gcr.io/PROJECT-ID/triageview --platform managed --set-env-vars GEMINI_API_KEY="your-api-key"
   ```

### Azure Container Instances

1. **Deploy to ACI**
   ```bash
   az container create \
     --resource-group myResourceGroup \
     --name triageview \
     --image yourusername/triageview \
     --ports 8501 \
     --environment-variables GEMINI_API_KEY="your-api-key"
   ```

## 🖥️ Local Development Setup

### Using Python Virtual Environment

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/triageview-dashboard.git
   cd triageview-dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set API key**
   ```bash
   export GEMINI_API_KEY="your-api-key"  # On Windows: set GEMINI_API_KEY=your-api-key
   ```

5. **Run the application**
   ```bash
   streamlit run triage_dashboard_2.py
   ```

### Using Conda

1. **Create conda environment**
   ```bash
   conda create -n triageview python=3.9
   conda activate triageview
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run application**
   ```bash
   streamlit run triage_dashboard_2.py
   ```

## 🔐 Security Configuration

### API Key Management

**✅ Secure Methods:**
- Environment variables
- Streamlit secrets
- Cloud secret managers (AWS Secrets Manager, Google Secret Manager)
- Kubernetes secrets

**❌ Avoid:**
- Hardcoding in source code
- Committing to version control
- Plain text files

### Environment Variables

Create a `.env` file (add to `.gitignore`):
```bash
GEMINI_API_KEY=your-api-key-here
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 📊 Performance Optimization

### Streamlit Configuration

Add to `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false

[global]
developmentMode = false
```

### Caching Configuration

The app uses `@st.cache_data` for:
- Synthetic data generation
- API responses (with TTL)
- Chart generation

## 🔍 Monitoring & Troubleshooting

### Health Checks

**Streamlit Health Endpoint:**
```bash
curl http://localhost:8501/_stcore/health
```

**Application Health:**
```bash
curl http://localhost:8501/  # Should return 200 OK
```

### Common Issues

1. **API Key Issues**
   - Verify key is correctly set
   - Check API quota limits
   - Ensure internet connectivity

2. **Port Conflicts**
   - Change port in configuration
   - Kill existing processes: `pkill -f streamlit`

3. **Dependency Errors**
   - Update pip: `pip install --upgrade pip`
   - Clear cache: `pip cache purge`
   - Reinstall: `pip install -r requirements.txt --force-reinstall`

### Logs and Debugging

**View Streamlit logs:**
```bash
streamlit run triage_dashboard_2.py --logger.level debug
```

**Docker logs:**
```bash
docker logs triageview
```

## 🔄 Updates and Maintenance

### Updating the Application

1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Update dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Restart application**
   ```bash
   # For Streamlit Cloud: automatic deployment
   # For Docker: docker-compose restart
   # For local: Ctrl+C and restart
   ```

### Backup and Recovery

**Important files to backup:**
- Application code
- Configuration files
- API keys/secrets
- Custom modifications

## 📞 Support

If you encounter issues during deployment:

1. **Check the logs** for error messages
2. **Verify all prerequisites** are met
3. **Test locally** before cloud deployment
4. **Create an issue**
