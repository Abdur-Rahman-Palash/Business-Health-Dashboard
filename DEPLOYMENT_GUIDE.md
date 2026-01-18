# 🚀 Executive Dashboard Deployment Guide

## 📋 Overview
এই গাইডে আপনি শিখবেন কিভাবে আপনার Executive Dashboard কে Vercel এবং Hostinger এ deploy করবেন।

---

## 🌐 Vercel Deployment (Next.js Frontend)

### Step 1: GitHub Repository Setup
```bash
# আপনার প্রজেক্ট GitHub এ push করুন
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### Step 2: Vercel Configuration
1. [Vercel.com](https://vercel.com) এ যান
2. "Add New Project" ক্লিক করুন
3. আপনার GitHub repository import করুন
4. Auto-detect হবে Next.js framework
5. Environment variables add করুন:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-domain.com
   ```

### Step 3: Build Settings
`vercel.json` ফাইলে আছে:
```json
{
  "version": 2,
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install"
}
```

### Step 4: Deploy
- "Deploy" বাটনে ক্লিক করুন
- 2-3 মিনিটের মধ্যে deploy হয়ে যাবে
- URL পাবেন: `https://executive-dashboard.vercel.app`

---

## 🔧 Hostinger Deployment (Static Files)

### Step 1: Build for Production
```bash
# Next.js build করুন
npm run build

# Static files generate করুন
npm run export
```

### Step 2: Configure for Static Export
`next.config.ts` ফাইলে add করুন:
```typescript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
```

### Step 3: Upload to Hostinger
1. `out` folder টি zip করুন
2. Hostinger cPanel এ লগইন করুন
3. File Manager এ যান
4. `public_html` ফোল্ডারে unzip করুন
5. Domain এ ভিজিট করুন

---

## 🔄 Backend API Deployment Options

### Option 1: Vercel Serverless Functions
```python
# api.py ফাইল vercel.json সহকারে deploy হবে
# স্বয়ংক্রিয়ভাবে Vercel এ API endpoint তৈরি হবে
```

### Option 2: Railway/Heroku
```bash
# Railway deploy
railway login
railway init
railway up

# Heroku deploy
heroku create your-dashboard-api
git push heroku main
```

### Option 3: PythonAnywhere
1. PythonAnywhere account তৈরি করুন
2. Web app তৈরি করুন
3. `simple_backend.py` upload করুন
4. Manual configuration করুন

---

## 🔗 API Integration

### Frontend API Configuration
`src/services/mock-api.ts` ফাইলে:
```typescript
// Development
const API_BASE = 'http://localhost:8001';

// Production (Vercel)
const API_BASE = 'https://your-backend-domain.com';

// Production (Serverless)
const API_BASE = 'https://executive-dashboard.vercel.app/api';
```

### CORS Configuration
Backend এ CORS enable করুন:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://executive-dashboard.vercel.app", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔄 Routing & Page Reload

### Next.js Routing (Vercel)
- ✅ Automatic routing works
- ✅ Page reload works perfectly
- ✅ Dynamic routes supported
- ✅ Static generation

### Static Hosting (Hostinger)
- ✅ Client-side routing works
- ✅ Page reload works
- ⚠️ Need proper server configuration

### Server Configuration (Hostinger)
`.htaccess` ফাইল:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```

---

## 📱 Mobile Responsiveness

Both deployments support:
- ✅ Responsive design
- ✅ Touch interactions
- ✅ Mobile navigation
- ✅ Optimized performance

---

## 🔒 Environment Variables

### Development
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Production (Vercel)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

### Production (Hostinger)
```bash
NEXT_PUBLIC_API_URL=/api  # Relative path for same domain
```

---

## 🚀 Quick Deploy Commands

### Vercel (Frontend)
```bash
vercel --prod
```

### Railway (Backend)
```bash
railway up
```

### Hostinger (Static)
```bash
npm run build
npm run export
# Upload out folder to Hostinger
```

---

## 📊 Live Demo URLs

After deployment:
- **Frontend**: `https://executive-dashboard.vercel.app`
- **Backend API**: `https://your-backend-domain.com`
- **API Docs**: `https://your-backend-domain.com/docs`

---

## 🔧 Troubleshooting

### Common Issues:
1. **CORS Error**: Backend এ proper CORS configuration করুন
2. **API Not Found**: Environment variables check করুন
3. **Build Error**: Dependencies install করুন
4. **Routing Issue**: `.htaccess` ফাইল configure করুন

### Debug Steps:
```bash
# Check build
npm run build

# Check API
curl http://localhost:8001/health

# Check deployment logs
vercel logs
```

---

## 🎯 Best Practices

1. **Always test locally first**
2. **Use environment variables**
3. **Enable HTTPS**
4. **Monitor performance**
5. **Set up analytics**
6. **Regular backups**

---

## 📞 Support

যদি কোনো সমস্যা হয়:
1. Check logs
2. Verify environment variables
3. Test API endpoints
4. Check CORS settings

---

**🎉 Deploy সফল হলে আপনি পাবেন:**
- Live dashboard with real data
- Proper routing
- Mobile responsive design
- Fast loading times
- Secure connections
