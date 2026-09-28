"""
API Gateway
"""

from fastapi import FastAPI
from app.routes.resume import router as resume_router

app = FastAPI()

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
  

