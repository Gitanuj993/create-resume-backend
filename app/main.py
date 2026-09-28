"""
API Gateway
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.resume import router as resume_router

app = FastAPI()

cors_origins = [
  origin.strip()
  for origin in os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173,"
    "http://127.0.0.1:3000,http://127.0.0.1:5173",
  ).split(",")
  if origin.strip()
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=cors_origins,
  allow_methods=["GET", "POST", "OPTIONS"],
  allow_headers=["Content-Type"],
)

# -------------------------
# Route
# -------------------------

# include router
app.include_router(resume_router)


# Health
@app.get("/health")
async def health() :
  return { "message" : "Healthy" }

@app.get("/")
async def home() :
  return { "message" : "App is running" }
  

