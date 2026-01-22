# 🚀 Streamlit Deployment Guide - Option A (Embed in Next.js)

## 📋 Overview
এই গাইডে আপনি শিখবেন কিভাবে Streamlit dashboard কে Railway এ deploy করে Next.js এ embed করবেন।

---

## 🎯 Step 1: Deploy Streamlit to Railway

### 1.1 Create Railway Account
1. [Railway.app](https://railway.app) এ যান
2. GitHub দিয়ে sign up করুন
3. Free plan select করুন

### 1.2 Prepare File
```bash
# Railway এর জন্য requirements.txt
cp requirements-streamlit.txt requirements.txt

# Railway configuration file
echo '{"name": "executive-dashboard", "services": {"executive-dashboard": {"source": {"project": "."}, "build": {"builder": "NIXPACKS"}, "deploy": {"startCommand": "streamlit run backend/streamlit_app.py --server.port=8501 --server.address=0.0.0.0", "healthcheckPath": "/_stcore/health"}}}' > railway.json
```

### 1.3 Deploy to Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway init
railway up
```

### 1.4 Get Your URL
Deploy হয়ে আপনি পাবেন:
- **Streamlit URL**: `https://your-app-name.railway.app`
- **Health Check**: `https://your-app-name.railway.app/_stcore/health`

---

## 🎯 Step 2: Update Next.js with Your URL

### 2.1 Update StreamlitEmbed Component
```tsx
// src/app/page.tsx এ update করুন
{activeTab === 'streamlit' && (
  <StreamlitEmbed 
    streamlitUrl="https://your-actual-app-name.railway.app"
    height="900px"
    showControls={true}
  />
)}
```

### 2.2 Deploy Next.js to Vercel
```bash
# Git push
git add .
git commit -m "Add Streamlit embed with Railway URL"
git push origin main

# Vercel deploy
vercel --prod
```

---

## 🎯 Step 3: Environment Configuration

### 3.1 Railway Environment Variables
Railway dashboard এ যান:
1. Your project select করুন
2. Variables tab এ যান
3. Add these variables:
   ```
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_ADDRESS=0.0.0.0
   PYTHON_VERSION=3.9
   ```

### 3.2 Vercel Environment Variables
Vercel dashboard এ যান:
1. Your project select করুন
2. Settings → Environment Variables
3. Add:
   ```
   NEXT_PUBLIC_STREAMLIT_URL=https://your-app-name.railway.app
   ```

---

## 🎯 Step 4: Custom Domain (Optional)

### 4.1 Railway Custom Domain
```bash
# Railway এ custom domain add করুন
railway domain add dashboard.yourdomain.com
```

### 4.2 Update Next.js
```tsx
<StreamlitEmbed 
  streamlitUrl="https://dashboard.yourdomain.com"
  height="900px"
  showControls={true}
/>
```

---

## 🎯 Step 5: Testing & Verification

### 5.1 Test Streamlit
```bash
# Test your Streamlit app
curl https://your-app-name.railway.app/_stcore/health
```

### 5.2 Test Next.js
1. Vercel এ deploy করুন
2. `https://executive-dashboard.vercel.app` এ যান
3. "Streamlit Dashboard" tab এ যান
4. Embedded Streamlit দেখুন

---

## 🎯 Result

### ✅ What You Get:
1. **Vercel Frontend**: `https://executive-dashboard.vercel.app`
   - Next.js based
   - Fast loading
   - SEO optimized
   - Mobile responsive

2. **Railway Backend**: `https://your-app.railway.app`
   - Full Streamlit functionality
   - Real-time updates
   - Interactive controls
   - AI features

3. **Perfect Integration**:
   - Streamlit embedded in Next.js
   - Seamless navigation
   - Professional look
   - Best performance

### 🔄 How It Works:
1. User visits Vercel URL
2. Next.js loads with Streamlit embed
3. Streamlit loads from Railway
4. Full functionality available
5. Perfect user experience

---

## 🎯 Benefits

### ✅ Advantages:
- **Best of both worlds**: Next.js + Streamlit
- **Professional**: Clean integration
- **Fast**: CDN + optimized
- **Scalable**: Railway scales automatically
- **Reliable**: Both platforms have uptime
- **SEO friendly**: Next.js handles SEO
- **Mobile ready**: Both platforms responsive

### 🎯 Features Available:
- 📊 Real-time KPI monitoring
- 🎯 Interactive controls
- 💡 AI-powered insights
- 📈 Advanced analytics
- 🔄 Live updates
- 📱 Mobile responsive
- 🌙 Dark/light mode

---

## 🎯 Troubleshooting

### Common Issues:
1. **CORS Error**: Railway এ CORS enable করুন
2. **Loading Issue**: URL correct কিনা check করুন
3. **Blank Screen**: Railway logs check করুন
4. **Slow Loading**: Cache clear করুন

### Debug Commands:
```bash
# Check Railway logs
railway logs

# Check Vercel logs
vercel logs

# Test connection
curl -I https://your-app.railway.app
```

---

## 🎉 Success!

Deploy সফল হলে আপনি পাবেন:
- **Professional dashboard** with perfect integration
- **Live on both platforms** 
- **Full Streamlit functionality**
- **Best user experience**

**🚀 Ready for production!**
