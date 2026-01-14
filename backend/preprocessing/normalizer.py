from typing import Dict, List, Optional
import pandas as pd


def normalize_input(
    text: str,
    structured_data: Optional[Dict] = None,
    csv_df: Optional[pd.DataFrame] = None,
    chart_notes: Optional[str] = None
) -> Dict:
    """
    Normalizes multimodal inputs into a unified representation
    for downstream reasoning agents.
    """

    normalized = {
        "text": text.strip(),
        "structured_insights": []
    }

    # ---------- Structured JSON ----------
    if structured_data:
        for key, value in structured_data.items():
            normalized["structured_insights"].append(
                f"{key}: {value}"
            )

    # ---------- CSV / Tabular Data ----------
    if csv_df is not None:
        normalized["structured_insights"].extend(
            _summarize_dataframe(csv_df)
        )

    # ---------- Chart / Human Notes ----------
    if chart_notes:
        normalized["structured_insights"].append(
            f"Chart observation: {chart_notes}"
        )

    return normalized


# ------------------ helpers ------------------

def _summarize_dataframe(df: pd.DataFrame) -> List[str]:
    """
    Extracts lightweight semantic insights from a dataframe.
    NO ML. NO assumptions.
    """
    insights = []

    insights.append(f"Dataset contains {len(df)} rows and {len(df.columns)} columns")

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            insights.append(
                f"Column '{col}' stats — mean: {df[col].mean():.2f}, "
                f"min: {df[col].min():.2f}, max: {df[col].max():.2f}"
            )

    return insights
