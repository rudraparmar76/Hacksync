# from preprocessing.summarizer import summarize_document
# from preprocessing.loader import _extract_pdf

# with open("test.pdf", "rb") as f:
#     pdf_bytes = f.read()

# text = _extract_pdf(pdf_bytes)
# result = summarize_document(text)

# print(result["summary"])
# print(result["sections"])

# from agents.factor_agent import run_factor_agent
# import json

# mock_summary = {
#     "summary": "This document compiles practice activity sheets for STD_X Science & Technology, designed to reinforce learning across a broad curriculum. It covers key biological concepts such as Heredity and Evolution, Life Processes (energy metabolism, cell division, reproduction), and Animal Classification. Environmental science topics include Green Energy generation, Environmental Management (pollution, global warming, conservation), and Disaster Management. The sheets also delve into modern scientific applications like Biotechnology (food, medical, agricultural, bioremediation, stem cells) and Microbiology (industrial uses, clean technology). Additionally, content addresses Social Health, including lifestyle impacts, addiction, and stress management. The exercises feature diverse question formats, requiring students to define, explain, distinguish, interpret diagrams, provide scientific reasons, and apply critical thinking to consolidate their understanding of these varied scientific and societal topics.",
#     "sections": [{'title': 'Heredity and Evolution', 'summary': 'Explores evolutionary concepts (mutation, wise man evolution), key theories (Darwin, Lamarck), cellular processes (transcription, translation, mutation, translocation), and evidence like fossils and comparative biology.'}, {'title': 'Life Processes in Organisms (Part 1)', 'summary': 'Focuses on energy metabolism (carbohydrate energy, ATP, oxygen), cellular respiration (glycolysis, co-enzymes), and detailed aspects of cell division (mitosis, meiosis, stages, importance).'}, {'title': 'Life Processes in Organisms (Part 2)', 'summary': 'Covers asexual reproduction (Euglena, Yeast), sexual reproduction in plants (flowers), the human reproductive system (hormones, menopause), and basic plant morphology.'}, {'title': 'Reproduction (Advanced Topics)', 'summary': 'Dives into specific reproductive processes like double fertilization, fungal colony formation, the human menstrual cycle, comprehensive distinctions between asexual and sexual reproduction, various asexual methods, and cloning.'}, {'title': 'Environmental Management', 'summary': 'Discusses global warming (causes, impacts), various forms of pollution, strategies for environmental conservation (social responsibility, individual efforts), and solutions to environmental issues.'}, {'title': 'Energy Generation and Green Energy', 'summary': 'Covers diverse energy sources (fossil fuels, nuclear, solar, wind), power plant types, energy production mechanisms, eco-friendliness comparisons, and solar energy technologies.'}, {'title': 'Animal Classification', 'summary': 'Details major animal phyla and classes, their distinguishing characteristics (body organization, specific features), larval metamorphosis, connecting links, and reproductive methods across various animal groups.'}, {'title': 'Introduction to Microbiology', 'summary': 'Highlights the roles of various microbes in bioremediation (oil spills, sewage, uranium conversion), industrial applications (yoghurt, antibiotics), and their potential for eco-friendly technologies.'}, {'title': 'Biotechnology and Its Applications', 'summary': 'Encompasses food biotechnology, extensive bioremediation using microorganisms, medical and agricultural biotechnology (transgenic crops, stem cells, vaccines, DNA fingerprinting), and related definitions.'}, {'title': 'Social Health', 'summary': 'Examines factors influencing social health, the impact of technology and lifestyle, issues like addiction (tobacco, alcoholism), stress management, cybercrime, and threats to adolescent social well-being.'}, {'title': 'Disaster Management', 'summary': 'Explores types of disasters (natural, man-made), the importance of first aid, pre- and post-disaster management strategies, effects and remedies for specific disasters, and overall disaster scope.'}, {'title': 'Previous Year Question Papers Compilation', 'summary': 'A section compiling various question types (MCQ, short answer, matching, true/false) from past exams, covering a wide array of topics across the science curriculum.'}]
# }

# result = run_factor_agent(mock_summary)
# print(json.dumps(result, indent=2))

# import json
# import pandas as pd

# from preprocessing.normalizer import normalize_input
# from preprocessing.summarizer import summarize_document


# import json
# import pandas as pd

# from preprocessing.loader import extract_text
# from preprocessing.normalizer import normalize_input
# from preprocessing.summarizer import summarize_document


# def test_pdf_multimodal_summarizer():
#     # --------- Load PDF ----------
#     with open("test.pdf", "rb") as f:
#         pdf_bytes = f.read()

#     # --------- Extract text from PDF ----------
#     extracted_text = extract_text(pdf_bytes, filename="sample_report.pdf")

#     assert extracted_text.strip(), "PDF text extraction failed"

#     # --------- Optional: mock structured data ----------
#     data = {
#         "month": ["Jan", "Feb", "Mar"],
#         "revenue": [100, 130, 160]
#     }
#     df = pd.DataFrame(data)

#     # --------- Optional chart insight ----------
#     chart_notes = "Revenue shows an increasing trend across Q1."

#     # --------- Normalize multimodal input ----------
#     normalized = normalize_input(
#         text=extracted_text   
#     )

#     # --------- Run summarizer ----------
#     result = summarize_document(normalized)

#     # --------- Assertions ----------
#     assert isinstance(result, dict)
#     assert "summary" in result
#     assert "sections" in result
#     assert isinstance(result["summary"], str)
#     assert isinstance(result["sections"], list)

#     for section in result["sections"]:
#         assert "title" in section
#         assert "summary" in section

#     # --------- Print output ----------
#     print("\n===== PDF SUMMARY =====\n")
#     print(result["summary"])

#     print("\n===== PDF SECTIONS =====\n")
#     print(json.dumps(result["sections"], indent=2))

#     print("\n✅ PDF summarizer test PASSED\n")


# if __name__ == "__main__":
#     test_pdf_multimodal_summarizer()


# import json

# from preprocessing.loader import extract_text
# from preprocessing.normalizer import normalize_input
# from preprocessing.summarizer import summarize_document
# from agents.factor_agent import run_factor_agent


# def test_pdf_to_factor_pipeline():
#     # --------- Load PDF ----------
#     with open("test.pdf", "rb") as f:
#         pdf_bytes = f.read()

#     text = extract_text(pdf_bytes, filename="test.pdf")
#     assert text.strip(), "Failed to extract text from PDF"

#     # --------- Normalize ----------
#     normalized = normalize_input(text=text)

#     # --------- Summarize ----------
#     summarized = summarize_document(normalized)
#     assert summarized["summary"], "Summarizer produced empty summary"

#     # --------- Factor Agent ----------
#     factors = run_factor_agent(summarized)
#     assert "factors" in factors and factors["factors"], "No factors extracted"

#     # --------- Print results ----------
#     print("\n===== PDF → FACTORS =====\n")
#     print(json.dumps(factors, indent=2))

#     print("\n✅ PDF → Factor pipeline test PASSED\n")


# if __name__ == "__main__":
#     test_pdf_to_factor_pipeline()
import json
from agents.support_agent import run_support_agent

factor = {
    "id": "F1",
    "name": "Pricing Strategy Effectiveness",
    "description": "Impact of pricing changes on revenue and customer behavior"
}

document = {
    "summary": "Revenue increased after a 10% price hike, but churn rose slightly.",
    "sections": [
        {"title": "Pricing", "summary": "Prices increased by 10% in Q2."},
        {"title": "Revenue", "summary": "Revenue grew by 12% quarter-over-quarter."}
    ]
}

result = run_support_agent(factor, document)
print(json.dumps(result, indent=2))

