from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import time
from orchestrator.coordinator import run_aether_pipeline
from preprocessing.normalizer import normalize_input
from preprocessing.summarizer import summarize_document
from agents.factor_agent import run_factor_agent
from core.schema import Factor
from engines.debate_engine import run_debate
from agents.synth_agent import run_synth_agent

app = FastAPI(
    title="Project AETHER API",
    description="Multi-agent deliberative AI system",
    version="1.0.0"
)

# --------- CORS (frontend safe) ---------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Health ---------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/analyze/demo")
def analyze_demo():
    """
    One-click demo for judges.
    """
    demo_prompt = (
        "Why does the Sun appear yellow to humans instead of green, "
        "even though its radiation spectrum peaks near green wavelengths?"
    )

    start = time.time()

    result = run_aether_pipeline(user_prompt=demo_prompt)

    result["latency_ms"] = int((time.time() - start) * 1000)
    result["mode"] = "demo"
    result["demo_prompt"] = demo_prompt

    return result

# --------- Prompt-based analysis ---------

@app.post("/analyze/prompt")
def analyze_prompt(prompt: str = Form(...)):
    """
    Analyze a direct user prompt (no document).
    """
    result = run_aether_pipeline(user_prompt=prompt)
    return result

# --------- Document-based analysis ---------

@app.post("/analyze/document")
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze an uploaded document (PDF / text).
    """
    file_bytes = await file.read()

    result = run_aether_pipeline(
        file_bytes=file_bytes,
        filename=file.filename
    )
    return result

@app.post("/agent/summarize")
def summarize_agent(payload: dict):
    """
    Run summarizer agent independently.
    """
    normalized = normalize_input(text=payload["text"])
    result = summarize_document(normalized)
    return result

@app.post("/agent/factors")
def factor_agent(payload: dict):
    """
    Run factor extraction independently.
    """
    return run_factor_agent(payload)

@app.post("/agent/debate")
def debate_agent(payload: dict):
    """
    Run debate for ONE factor.
    """
    factor = Factor(**payload["factor"])
    result = run_debate(factor)
    return result

@app.post("/agent/synthesize")
def synth_agent(payload: dict):
    """
    Run synthesis independently.
    """
    return run_synth_agent(payload["debates"])

