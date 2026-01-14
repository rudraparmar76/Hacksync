# from core.gemini_client import call_gemini
# from core.schema import Factor
# from prompts.structured_debate import single_call_structured_debate_prompt

# input_data = {
#     "factors": [
#         {
#             "id": "F1",
#             "name": "Breadth of Scientific and Societal Topics Covered",
#             "description": "The material encompasses a wide array of subjects from core biological processes and animal classification to environmental management, energy generation, modern biotechnology, microbiology, and social health."
#         },
#         {
#             "id": "F2",
#             "name": "Inclusion of Contemporary Scientific Applications",
#             "description": "The curriculum integrates modern scientific fields such as biotechnology (food, medical, agricultural, stem cells, bioremediation) and applied microbiology (industrial uses, clean technology), reflecting current advancements."
#         },
#         {
#             "id": "F3",
#             "name": "Emphasis on Environmental and Social-Health Awareness",
#             "description": "Significant attention is given to topics like global warming, pollution, conservation, disaster management, social health factors, addiction, and stress management, fostering awareness of real-world challenges."
#         },
#         {
#             "id": "F4",
#             "name": "Variety of Cognitive Skills Assessed Through Question Formats",
#             "description": "The exercises employ diverse question formats, including definitions, explanations, distinctions, diagram interpretation, scientific reasoning, and critical thinking, designed to engage multiple cognitive abilities."
#         },
#         {
#             "id": "F5",
#             "name": "Pedagogical Approach Focused on Reinforcement and Practice",
#             "description": "The document is primarily composed of 'practice activity sheets' and is 'designed to reinforce learning', indicating a pedagogical strategy centered on consolidating and applying previously learned knowledge."
#         }
#     ]
# }


# def run():
#     for f in input_data["factors"]:
#         factor = Factor(**f)

#         print("\n==============================")
#         print(f"DEBATE FOR {factor.id}: {factor.name}")
#         print("==============================")

#         # 1️⃣ Build single-call prompt
#         prompt = single_call_structured_debate_prompt(factor)

#         # 2️⃣ Call Gemini ONCE
#         response = call_gemini(prompt)

#         # 3️⃣ Print result
#         print(response)


# if __name__ == "__main__":
#     run()


from core.schema import Factor
from engines.debate_engine import run_debate

input_data = {
  "factors": [
    {
      "id": "F1",
      "name": "Breadth of Scientific and Societal Topics Covered",
      "description": "The material encompasses a wide array of subjects from core biological processes and animal classification to environmental management, energy generation, modern biotechnology, microbiology, and social health."
    },
    {
      "id": "F2",
      "name": "Inclusion of Contemporary Scientific Applications",
      "description": "The curriculum integrates modern scientific fields such as biotechnology (food, medical, agricultural, stem cells, bioremediation) and applied microbiology (industrial uses, clean technology), reflecting current advancements."
    },
    {
      "id": "F3",
      "name": "Emphasis on Environmental and Social-Health Awareness",
      "description": "Significant attention is given to topics like global warming, pollution, conservation, disaster management, social health factors, addiction, and stress management, fostering awareness of real-world challenges."
    },
    {
      "id": "F4",
      "name": "Variety of Cognitive Skills Assessed Through Question Formats",
      "description": "The exercises employ diverse question formats, including definitions, explanations, distinctions, diagram interpretation, scientific reasoning, and critical thinking, designed to engage multiple cognitive abilities."
    },
    {
      "id": "F5",
      "name": "Pedagogical Approach Focused on Reinforcement and Practice",
      "description": "The document is primarily composed of 'practice activity sheets' and is 'designed to reinforce learning', indicating a pedagogical strategy centered on consolidating and applying previously learned knowledge."
    }
  ]
}

def main():
    # for f in input_data["factors"]:
    #     factor = Factor(**f)
        
    #     print(f"\n\n{'='*40}")
    #     print(f"🚀 STARTING DEBATE: {factor.id} - {factor.name}")
    #     print(f"{'='*40}\n")

    #     # This will now stream the Support and Opposition text to your console
    #     # because of the print() calls inside call_ollama.
    #     result = run_debate(factor)

    #     # Separate the transcript from the decision clearly
    #     print(f"\n{'-'*40}")
    #     print(f"⚖️ FINAL JUDGMENT for {factor.id}:")
        
    #     decision = result["decision"]
    #     print(f"STATUS:    {decision.get('status')}")
    #     print(f"SCORE:     {decision.get('score')}/10")
    #     print(f"REASONING: {decision.get('reasoning')}")
    #     print(f"{'-'*40}\n")
    for f in input_data["factors"]:
        factor = Factor(**f)
        
        print(f"\n{'#'*60}")
        print(f"🏛️  DEBATE CHAMBER: {factor.name}")
        print(f"{'#'*60}\n")

        result = run_debate(factor)
        
        # Split the transcript for cleaner printing
        # This assumes your transcript is formatted as "SUPPORT: ... OPPOSITION: ..."
        parts = result["transcript"].split("OPPOSITION:")
        
        print("🎤 [PROponent]:")
        print(parts[0].replace("SUPPORT:", "").strip())
        print(f"\n🔥 [OPPonent]:")
        print(parts[1].strip() if len(parts) > 1 else "No rebuttal.")
        
        print(f"\n{'-'*60}")
        print(f"⚖️  VERDICT: {result['decision'].get('status')}")
        print(f"📝 {result['decision'].get('verdict')}")
        print(f"📊 STRENGTH SCORE: {result['decision'].get('score')}/10")
        print(f"{'-'*60}\n")

if __name__ == "__main__":
    main()