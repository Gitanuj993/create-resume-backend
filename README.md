# Create Resume API

FastAPI service that validates resume JSON and returns a generated PDF.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open `http://127.0.0.1:8000/docs` for the Swagger UI. The health endpoint is `GET /health`.






## Generate a resume

Send a JSON `POST` request to `/resume/generate` matching the `ResumeRequest` schema shown in `/docs`. The endpoint responds with an `application/pdf` file.