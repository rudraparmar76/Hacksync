from backend.logs.traces import TraceLogger
from backend.logs.timeline import build_timeline
from backend.logs.highlights import extract_decision_path
from backend.logs.explanation import build_trace_explanation

from backend.preprocessing.loader import extract_text
from backend.preprocessing.normalizer import normalize_input
from backend.preprocessing.summarizer import summarize_document

from backend.agents.factor_agent import run_factor_agent
from backend.engines.debate_engine import run_debate
from backend.agents.synth_agent import run_synth_agent

from backend.core.schema import Factor

def run_aether_pipeline(
    file_bytes: bytes | None = None,
    filename: str | None = None,
    user_prompt: str | None = None
):
    trace = TraceLogger()

    # ---------- 1. INPUT ----------
    if user_prompt:
        raw_text = user_prompt
        source = "prompt"
    elif file_bytes and filename:
        raw_text = extract_text(file_bytes, filename)
        source = "document"
    else:
        raise ValueError("Either file or user_prompt must be provided")

    # ---------- 2. NORMALIZE ----------
    normalized = normalize_input(text=raw_text)

    # ---------- 3. SUMMARIZE ----------
    if source == "prompt" and len(raw_text) < 500:
        processed_doc = {"summary": raw_text, "sections": []}
    else:
        processed_doc = summarize_document(normalized)

    trace.log_step(
        agent_name="Summarizer",
        stage="summarization",
        input_data={"source": source, "text_length": len(raw_text)},
        output_data={"summary_length": len(processed_doc.get("summary", ""))}
    )

    # ---------- 4. FACTOR EXTRACTION ----------
    factor_output = run_factor_agent(processed_doc)
    factors = factor_output.get("factors", [])

    if not factors:
        trace.log_step(
            agent_name="FactorAgent",
            stage="factor_extraction",
            input_data=processed_doc,
            output_data={"error": "No evaluable factors extracted"}
        )
        # graceful exit (as shown above)
        # [return block omitted here for brevity]

    trace.log_step(
        agent_name="FactorAgent",
        stage="factor_extraction",
        input_data={"summary": processed_doc.get("summary", "")},
        output_data={"factor_count": len(factors)}
    )

    # ---------- 5. DEBATES ----------
    debates = []

    for f in factors:
        factor = Factor(**f)
        debate_result = run_debate(factor)

        trace.log_step(
            agent_name="DebateEngine",
            stage="debate",
            factor_id=factor.id,
            factor_name=factor.name,
            input_data=f,
            output_data={
                "status": debate_result["decision"]["status"],
                "score": debate_result["decision"]["score"],
                "winning_argument": debate_result["decision"]["winning_argument"]
            }
        )

        debates.append(debate_result)

    # ---------- 6. SYNTHESIS ----------
    for d in debates:
        assert "decision" in d and "score" in d["decision"]

    final_report = run_synth_agent(debates)

    trace.log_step(
        agent_name="SynthesizerAgent",
        stage="synthesis",
        input_data={"debates_count": len(debates)},
        output_data={"report_generated": True}
    )

    # ---------- 7. EXPLAINABILITY ----------
    trace_data = trace.get_trace()

    return {
        "final_report": final_report,
        "debates":debates,
        "trace": trace_data,
        "timeline": build_timeline(trace_data),
        "decision_path": extract_decision_path(trace_data),
        "explanation": build_trace_explanation(trace_data)
    }
