from fastapi import FastAPI

app = FastAPI(
    title="Job Automation System",
    description="AI-powered job discovery and application tracking system",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Job Automation API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }