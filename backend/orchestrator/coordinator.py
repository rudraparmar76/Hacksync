# backend/orchestrator/coordinator.py
from logs.traces import TraceLogger
from preprocessing.loader import extract_text
from preprocessing.summarizer import summarize_document
from backend.preprocessing.normalizer import normalize_input


from agents.factor_agent import run_factor_agent
from agents.support_agent import run_support_agent
from agents.oppose_agent import run_oppose_agent
from agents.synth_agent import run_synth_agent


def run_aether_pipeline(file_bytes: bytes,filename:str):
    trace = TraceLogger()

    raw_text = raw_text = extract_text(file_bytes, filename)


    normalized = normalize_input(
        text=raw_text,
        csv_df=optional_csv_df,
        chart_notes=optional_chart_notes
    )

    processed_doc = summarize_document(normalized)

    factors = run_factor_agent(processed_doc)
    trace.log_step(
        agent_name="FactorAgent",
        input_data=processed_doc,
        output_data=factors
    )

    debates = []

    for factor in factors["factors"]:
        support = run_support_agent(factor)
        trace.log_step(
            agent_name="SupportAgent",
            input_data=factor,
            output_data=support
        )

        oppose = run_oppose_agent(factor, support)
        trace.log_step(
            agent_name="OpposeAgent",
            input_data={"factor": factor, "support": support},
            output_data=oppose
        )

        debates.append({
            "factor": factor,
            "support": support,
            "oppose": oppose
        })

    final_report = run_synth_agent(debates)
    trace.log_step(
        agent_name="SynthesizerAgent",
        input_data=debates,
        output_data=final_report
    )

    return {
        "trace": trace.get_trace(),
        "final_report": final_report
    }
