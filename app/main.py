"""
API Gateway
"""
app = FastAPI(title="Resume Generation Service",descrption="API for generating resume",version="1.0.0")

# -------------------------
# Route
# -------------------------


# Health
@app.get("/health")
async def health() :
  return { "message" : "Healthy" }

@app.get("/")
async def home() :
  return { "message" : "App is running" }
  
# include router
app.include_router(resume_router)

