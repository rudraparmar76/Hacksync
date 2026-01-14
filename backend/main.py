from fastapi import FastAPI, UploadFile, File
from orchestrator.coordinator import run_aether_pipeline

app = FastAPI()

@app.post("/analyze")
async def analyze_report(file: UploadFile = File(...)):
    content = await file.read()
    result = run_aether_pipeline(content,file.filename)
    return result
