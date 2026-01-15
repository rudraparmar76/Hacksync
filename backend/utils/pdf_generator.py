from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

def generate_debate_report(filename, overall_summary, synthesis, debate_results):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles["Title"]
    story.append(Paragraph("Strategic Decision Report", title_style))
    story.append(Spacer(1, 0.25*inch))

    # Executive Summary
    h1_style = styles["Heading1"]
    body_style = styles["BodyText"]
    
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(synthesis.get("executive_summary", "N/A"), body_style))
    story.append(Spacer(1, 0.2*inch))

    # Key Insights
    story.append(Paragraph("Key Insights", h1_style))
    for insight in synthesis.get("key_insights", []):
        story.append(Paragraph(f"• {insight}", body_style))
    story.append(Spacer(1, 0.2*inch))

    # Strategic Recommendations
    story.append(Paragraph("Strategic Recommendations", h1_style))
    for rec in synthesis.get("strategic_recommendations", []):
        story.append(Paragraph(f"<b>Strategy:</b> {rec.get('strategy', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Action:</b> {rec.get('action', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Rationale:</b> {rec.get('rationale', 'N/A')}", body_style))
        story.append(Spacer(1, 0.1*inch))
    story.append(Spacer(1, 0.2*inch))

    # Debate Details
    story.append(Paragraph("Detailed Debate Analysis", h1_style))
    
    for factor in debate_results:
        # Factor Title
        h2_style = styles["Heading2"]
        # Assuming factor is a dict with 'decision' and other fields, OR the structure from debate engine
        # Based on debate_engine.py: returns {claim, attack, defense, counter, decision}
        # But we need factor name. The structure depends on how we collect results. 
        # Assuming debate_results is a list of dicts that have factor_name mixed in or passed separately. 
        # Let's assume the caller passes a list where each item has "factor_name" and the debate dict.
        
        factor_name = factor.get("factor_name", "Factor")
        story.append(Paragraph(f"Factor: {factor_name}", h2_style))
        
        # Verdict
        decision = factor.get("decision", {})
        verdict_color = colors.green if decision.get("status") == "ACCEPTED" else colors.red
        verdict_style = ParagraphStyle('Verdict', parent=body_style, textColor=verdict_color, spaceAfter=6)
        story.append(Paragraph(f"Verdict: {decision.get('status', 'UNKNOWN')} (Score: {decision.get('score', 0)})", verdict_style))
        story.append(Paragraph(f"<i>{decision.get('verdict', '')}</i>", body_style))
        story.append(Spacer(1, 0.1*inch))

        # Debate Flow Table
        data = [
            ["Phase", "Argument"],
            ["Claim", Paragraph(factor.get("claim", ""), body_style)],
            ["Attack", Paragraph(factor.get("attack", ""), body_style)],
            ["Defense", Paragraph(factor.get("defense", ""), body_style)],
            ["Counter", Paragraph(factor.get("counter", ""), body_style)],
        ]

        table = Table(data, colWidths=[1*inch, 5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))

    doc.build(story)
