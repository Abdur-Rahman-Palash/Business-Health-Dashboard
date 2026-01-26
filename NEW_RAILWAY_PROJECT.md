# 🚀 New Railway Project Setup Guide

## 📋 নতুন Railway প্রজেক্ট তৈরি করুন

### Step 1: Railway এ নতুন প্রজেক্ট তৈরি

#### 1. Railway Dashboard এ যান
1. https://railway.app এ যান
2. Login করুন (GitHub দিয়ে)
3. **"New Project"** বাটনে ক্লিক করুন

#### 2. GitHub Repository সিলেক্ট করুন
1. **"Deploy from GitHub"** সিলেক্ট করুন
2. Repository খুঁজুন: `Abdur-Rahman-Palash/Business-Health-Dashboard`
3. **"Import"** বাটনে ক্লিক করুন

#### 3. Project Configuration
```
Project Name: executive-dashboard-streamlit
Environment: Production
```

### Step 2: Environment Variables সেট করুন

#### Railway Settings এ যান:
1. Project এ যান
2. **"Variables"** ট্যাবে যান
3. এই variables যোগ করুন:

```bash
PYTHON_VERSION=3.9
PORT=8501
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
NODE_ENV=production
```

### Step 3: Build Settings কনফিগার করুন

#### railway.json ফাইল চেক করুন:
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

### Step 4: Deploy করুন

#### Automatic Deploy:
1. Railway স্বয়ংক্রিয়ভাবে deploy শুরু করবে
2. Build logs দেখুন
3. 2-3 মিনিট সময় লাগবে

#### Manual Deploy (যদি লাগে):
1. **"Deployments"** ট্যাবে যান
2. **"New Deployment"** ক্লিক করুন
3. Branch: `main` সিলেক্ট করুন
4. **"Deploy Now"** ক্লিক করুন

---

## 🎯 Expected New URL

### নতুন URL পাবেন:
```
https://executive-dashboard-streamlit-production.up.railway.app
```

অথবা Railway যেকোনো নাম দিতে পারে, যেমন:
```
https://your-project-name.up.railway.app
```

---

## 🔧 যদি সমস্যা হয়

### Build Error হলে:
1. **Build Logs** চেক করুন
2. **requirements-streamlit.txt** আছে কিনা চেক করুন
3. **run_minimal_dashboard_clean.py** আছে কিনা চেক করুন

### Common Issues:
```
Error: ModuleNotFoundError: No module named 'streamlit'
Fix: requirements-streamlit.txt এ streamlit add করুন

Error: File not found: run_minimal_dashboard_clean.py
Fix: File exists কিনা চেক করুন
```

---

## 📊 Success Checklist

### ✅ Successful Deploy:
- [ ] Railway shows "Deployed" status
- [ ] URL accessible
- [ ] Streamlit dashboard loads
- [ ] All features working
- [ ] File upload working
- [ ] No mock data visible

### 🔍 Test These Features:
1. **Dashboard loads:** Clean interface
2. **File upload:** CSV, Excel, PDF tabs
3. **Analysis:** Advanced file analysis
4. **Decision making:** Recommendations visible
5. **Real-time sync:** Backend updates working

---

## 🚀 Quick Start Commands

### যদি CLI ব্যবহার করতে চান:
```bash
# Railway CLI install
npm install -g @railway/cli

# Login
railway login

# New project
railway new

# Link to GitHub
railway link

# Deploy
railway up
```

---

## 🎉 Expected Result

নতুন Railway প্রজেক্টে পাবেন:
- ✅ **Fresh Streamlit Dashboard**
- ✅ **All Advanced Features**
- ✅ **Multi-format File Upload**
- ✅ **Business Analysis**
- ✅ **Decision Making Support**
- ✅ **Real-time Updates**
- ✅ **Clean Production Interface**

---

## 📞 Help

### Railway Support:
- Dashboard: https://railway.app
- Docs: https://docs.railway.app

### যদি আটকে যান:
1. Screenshot error logs
2. Check file structure
3. Verify environment variables
4. Try redeploy

নতুন প্রজেক্টে সব ফিচার কাজ করবে! 🚀
