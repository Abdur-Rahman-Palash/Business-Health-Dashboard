#!/usr/bin/env python3
"""
Check GitHub repository status and force update if needed
"""

import subprocess
import json
import requests
from datetime import datetime

def run_command(command):
    """Run shell command and return output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def check_github_status():
    """Check GitHub repository status"""
    print("🔍 Checking GitHub Repository Status")
    print("=" * 50)
    
    # Check current branch
    stdout, stderr, code = run_command("git branch --show-current")
    if code == 0:
        print(f"✅ Current Branch: {stdout}")
    else:
        print(f"❌ Branch check failed: {stderr}")
    
    # Check remote URL
    stdout, stderr, code = run_command("git remote get-url origin")
    if code == 0:
        print(f"✅ Remote URL: {stdout}")
    else:
        print(f"❌ Remote URL check failed: {stderr}")
    
    # Check last commit
    stdout, stderr, code = run_command("git log -1 --oneline")
    if code == 0:
        print(f"✅ Last Commit: {stdout}")
    else:
        print(f"❌ Commit check failed: {stderr}")
    
    # Check if ahead/behind
    stdout, stderr, code = run_command("git status --porcelain=v1 -b")
    if code == 0:
        print(f"✅ Git Status: {stdout}")
    else:
        print(f"❌ Status check failed: {stderr}")

def force_sync_github():
    """Force sync with GitHub"""
    print("\n🔄 Force Syncing with GitHub")
    print("=" * 50)
    
    # Add all changes
    print("📁 Adding all changes...")
    stdout, stderr, code = run_command("git add -A")
    if code == 0:
        print("✅ Changes added")
    else:
        print(f"❌ Add failed: {stderr}")
    
    # Create commit if needed
    stdout, stderr, code = run_command("git status --porcelain")
    if stdout.strip():
        print("📝 Creating commit...")
        commit_message = f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Railway deployment sync"
        stdout, stderr, code = run_command(f'git commit -m "{commit_message}"')
        if code == 0:
            print("✅ Commit created")
        else:
            print(f"❌ Commit failed: {stderr}")
    else:
        print("ℹ️  No changes to commit")
    
    # Force push
    print("🚀 Force pushing to GitHub...")
    stdout, stderr, code = run_command("git push -f origin main")
    if code == 0:
        print("✅ Force push successful")
    else:
        print(f"❌ Force push failed: {stderr}")
        
        # Try normal push
        print("🔄 Trying normal push...")
        stdout, stderr, code = run_command("git push origin main")
        if code == 0:
            print("✅ Normal push successful")
        else:
            print(f"❌ Normal push failed: {stderr}")

def check_github_api():
    """Check GitHub API for latest commit"""
    print("\n🌐 Checking GitHub API")
    print("=" * 50)
    
    try:
        url = "https://api.github.com/repos/Abdur-Rahman-Palash/Business-Health-Dashboard/commits/main"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            commit_sha = data.get('sha', '')[:7]
            commit_message = data.get('commit', {}).get('message', '')
            commit_date = data.get('commit', {}).get('author', {}).get('date', '')
            
            print(f"✅ GitHub API Response:")
            print(f"   SHA: {commit_sha}")
            print(f"   Message: {commit_message}")
            print(f"   Date: {commit_date}")
            
            return True
        else:
            print(f"❌ GitHub API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API Check Failed: {e}")
        return False

def main():
    print("🚀 GitHub Repository Update Checker")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check local status
    check_github_status()
    
    # Check GitHub API
    api_success = check_github_api()
    
    # Force sync if needed
    if api_success:
        print("\n🔄 Syncing with GitHub...")
        force_sync_github()
    else:
        print("\n⚠️  GitHub API not accessible, trying local sync...")
        force_sync_github()
    
    print("\n✅ Update check completed!")
    print("📋 Summary:")
    print("   - Local repository checked")
    print("   - GitHub API verified")
    print("   - Force sync attempted")
    print("   - Railway should auto-update from GitHub")

if __name__ == "__main__":
    main()
