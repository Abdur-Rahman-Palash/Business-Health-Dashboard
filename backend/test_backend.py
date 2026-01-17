#!/usr/bin/env python3
"""
Simple backend test to isolate issues
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Set Hugging Face token from environment
hf_token = os.getenv('HF_TOKEN')
if hf_token:
    os.environ['HF_TOKEN'] = hf_token

app = FastAPI(title="Test Backend", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Test Backend is running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "test-backend"}

if __name__ == "__main__":
    print("🚀 Starting Test Backend...")
    print("📍 Test Endpoint: http://localhost:8000")
    print("🔍 Health Check: http://localhost:8000/health")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
