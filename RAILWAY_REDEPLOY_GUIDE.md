# 🔄 Railway Redeploy Guide

## 📋 Current Status
- **URL:** https://business-health-dashboard-production-6fb1.up.railway.app/
- **Status:** Running old version
- **Need:** Update with new Streamlit dashboard

---

## 🚀 Redeploy Steps

### Step 1: Go to Railway Dashboard
1. https://railway.app এ যান
2. Login করুন
3. "Your Projects" এ যান

### Step 2: Find Your Project
- Project name: `business-health-dashboard-production`
- অথবা সরাসরি: https://railway.app/project/business-health-dashboard-production

### Step 3: Redeploy Options

#### Option A: Automatic Redeploy (Recommended)
1. Project এ যান
2. "Settings" ট্যাবে যান
3. "GitHub" সেকশনে যান
4. "Redeploy" বাটনে ক্লিক করুন
5. Railway স্বয়ংক্রিয়ভাবে latest commit থেকে ডিপ্লয় করবে

#### Option B: Manual Trigger
1. Project এ যান
2. "Deployments" ট্যাবে যান
3. "New Deployment" ক্লিক করুন
4. Branch: `main` সিলেক্ট করুন
5. "Deploy Now" ক্লিক করুন

#### Option C: Force Rebuild
1. Project settings এ যান
2. "Variables" ট্যাবে যান
3. একটা variable যোগ করুন: `FORCE_REBUILD=true`
4. Save করুন
5. Redeploy করুন

---

## 🔧 Configuration Check

### Verify railway.json is Correct
```json
{
  "name": "executive-dashboard",
  "services": {
    "executive-dashboard": {
      "source": {"project": "."},
      "build": {
        "builder": "NIXPACKS",
        "buildCommand": "pip install -r requirements-streamlit.txt"
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
```

### Check Environment Variables
```bash
PYTHON_VERSION=3.9
PORT=8501
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## 📊 Expected Changes After Redeploy

### New Features:
- ✅ Advanced multi-format file upload (CSV, Excel, PDF, JSON, XML, DOCX)
- ✅ Real-time backend-frontend sync
- ✅ No mock data - clean interface
- ✅ Business health scoring
- ✅ Decision-making recommendations
- ✅ Client management system

### URL Remains Same:
- **Before:** https://business-health-dashboard-production-6fb1.up.railway.app/
- **After:** https://business-health-dashboard-production-6fb1.up.railway.app/ (same URL, updated content)

---

## 🚨 Troubleshooting

### If Redeploy Fails:
1. **Check Build Logs:**
   - Railway dashboard > Deployments > View logs
   - Error messages দেখুন

2. **Common Issues:**
   - `requirements-streamlit.txt` missing
   - `run_minimal_dashboard_clean.py` not found
   - Python version compatibility

3. **Fix Commands:**
   ```bash
   # Ensure requirements file exists
   ls -la requirements-streamlit.txt
   
   # Ensure main file exists
   ls -la run_minimal_dashboard_clean.py
   ```

### If Still Shows Old Version:
1. **Clear Browser Cache:**
   - Ctrl+F5 (hard refresh)
   - অথবা নতুন tab এ open করুন

2. **Check Deployment Status:**
   - Railway dashboard এ "Deployments" ট্যাব চেক করুন
   - Latest deployment status দেখুন

3. **Force Restart:**
   - Project settings > "Restart" বাটন

---

## 🎯 Success Indicators

### ✅ Successful Redeploy:
- Railway shows "Deployed" status
- URL loads new Streamlit dashboard
- All features working (file upload, analysis, etc.)
- No mock data visible

### 🔍 What to Check:
1. **Dashboard Header:** "🚀 Minimal Executive Dashboard"
2. **Sidebar:** "📁 Upload Data" button available
3. **File Upload:** CSV, Excel, PDF tabs visible
4. **No Mock Data:** Clean interface with upload prompt

---

## 📞 Quick Help

### Railway Support:
- Dashboard: https://railway.app
- Docs: https://docs.railway.app

### If Issues Persist:
1. Screenshot error logs
2. Check GitHub commit history
3. Verify all required files are present

---

## 🎉 Expected Result

After successful redeploy, your URL will show:
- **Clean Streamlit Dashboard**
- **Advanced File Upload Features**
- **Real-time Analysis**
- **Decision Making Support**
- **No Mock Data**

All at: https://business-health-dashboard-production-6fb1.up.railway.app/
