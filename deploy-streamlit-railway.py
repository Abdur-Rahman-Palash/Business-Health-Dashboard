#!/usr/bin/env python3
"""
Deploy Streamlit Dashboard to Railway
"""

import requests
import json
import os
from datetime import datetime

def create_railway_deployment():
    """Create Railway deployment for Streamlit dashboard"""
    
    # Railway API configuration
    railway_token = os.getenv('RAILWAY_TOKEN')  # Set your Railway token
    
    if not railway_token:
        print("❌ RAILWAY_TOKEN environment variable not set")
        print("Please set: export RAILWAY_TOKEN=your_token")
        return
    
    # Create new project
    headers = {
        'Authorization': f'Bearer {railway_token}',
        'Content-Type': 'application/json'
    }
    
    # Project configuration
    project_data = {
        "name": "streamlit-executive-dashboard",
        "projectId": "streamlit-dashboard"
    }
    
    try:
        # Create project
        response = requests.post(
            'https://backboard.railway.app/graphql/v2',
            headers=headers,
            json={
                "query": """
                mutation projectCreate($input: ProjectCreateInput!) {
                    projectCreate(input: $input) {
                        id
                        name
                    }
                }
                """,
                "variables": {
                    "input": {
                        "name": "streamlit-executive-dashboard"
                    }
                }
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Railway project created successfully")
            print(f"Project ID: {result.get('data', {}).get('projectCreate', {}).get('id')}")
        else:
            print(f"❌ Failed to create project: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def create_requirements_file():
    """Create requirements.txt for Railway deployment"""
    
    requirements = """streamlit==1.29.0
pandas==2.1.4
numpy==1.24.3
plotly==5.17.0
requests==2.31.0
python-docx==1.1.0
PyPDF2==3.0.1
openpyxl==3.1.2
"""
    
    with open('requirements-railway.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ requirements-railway.txt created")

def create_railway_config():
    """Create railway.json for Streamlit deployment"""
    
    config = {
        "name": "streamlit-executive-dashboard",
        "services": {
            "streamlit-dashboard": {
                "source": {
                    "project": "."
                },
                "build": {
                    "builder": "NIXPACKS",
                    "buildCommand": "pip install -r requirements-railway.txt"
                },
                "deploy": {
                    "startCommand": "streamlit run run_minimal_dashboard_clean.py --server.port=$PORT --server.address=0.0.0.0",
                    "healthcheckPath": "/_stcore/health",
                    "healthcheckTimeout": 100,
                    "restartPolicyType": "ON_FAILURE"
                }
            }
        }
    }
    
    with open('railway-streamlit.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ railway-streamlit.json created")

def main():
    print("🚀 Streamlit Dashboard Railway Deployment")
    print("=" * 50)
    
    # Create requirements file
    create_requirements_file()
    
    # Create Railway config
    create_railway_config()
    
    print("\n📋 Next Steps:")
    print("1. Install Railway CLI: npm install -g @railway/cli")
    print("2. Login: railway login")
    print("3. Deploy: railway up --config railway-streamlit.json")
    print("4. Your dashboard will be available at: https://your-app-name.up.railway.app")
    
    print("\n🔧 Alternative: Manual Deployment")
    print("1. Go to railway.app")
    print("2. Create new project")
    print("3. Upload your code")
    print("4. Set environment variables")
    print("5. Deploy")

if __name__ == "__main__":
    main()
