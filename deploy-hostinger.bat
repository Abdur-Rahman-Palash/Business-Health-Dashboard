@echo off
REM Executive Dashboard - Hostinger Deployment Script (Windows)
REM This script prepares and packages the dashboard for Hostinger deployment

echo 🚀 Executive Dashboard - Hostinger Deployment Script
echo ==================================================

REM Step 1: Clean previous build
echo 🧹 Cleaning previous build...
if exist out rmdir /s /q out
if exist .next rmdir /s /q .next

REM Step 2: Install dependencies
echo 📦 Installing dependencies...
call npm install

REM Step 3: Build for production
echo 🏗️ Building for production...
call npm run export

REM Step 4: Check if build was successful
if not exist out (
    echo ❌ Build failed! 'out' directory not found.
    pause
    exit /b 1
)

if not exist out\index.html (
    echo ❌ Build failed! 'index.html' not found in 'out' directory.
    pause
    exit /b 1
)

echo ✅ Build successful!

REM Step 5: Create deployment package
echo 📦 Creating deployment package...
cd out
powershell -command "Compress-Archive -Path * -DestinationPath ..\executive-dashboard-hostinger.zip -Force"
cd ..

echo ✅ Package created: executive-dashboard-hostinger.zip

REM Step 6: Show deployment instructions
echo 📋 Deployment Instructions:
echo 1. Upload 'executive-dashboard-hostinger.zip' to Hostinger
echo 2. Extract the zip file in 'public_html' directory
echo 3. Make sure '.htaccess' file is in the root
echo 4. Visit your domain to test
echo.

echo 📁 Files in 'out' directory:
dir out

echo 🎉 Ready for Hostinger deployment!
echo.
echo 📝 Important Notes:
echo - All routing is handled by .htaccess
echo - Page reload will work perfectly
echo - Static files are served directly
echo - Security headers are enabled
echo - Gzip compression is active
echo - Cache is optimized for performance
echo.
pause
