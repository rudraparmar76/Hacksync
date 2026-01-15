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
            "description": (
                "The material encompasses subjects from core biological processes and "
                "animal classification to environmental management, energy generation, "
                "modern biotechnology, microbiology, and social health."
            )
        }
    ]
}

def main():
    for f in input_data["factors"]:
        factor = Factor(**f)

        print("\n" + "#" * 60)
        print(f"🏛️  DEBATE CHAMBER: {factor.name}")
        print("#" * 60 + "\n")

        result = run_debate(factor)

        print("🎤 SUPPORT — CLAIM")
        print(result["claim"])

        print("\n" + "-" * 60)
        print("🔥 OPPOSITION — ATTACK")
        print(result["attack"])

        print("\n" + "-" * 60)
        print("🎤 SUPPORT — DEFENSE")
        print(result["defense"])

        print("\n" + "-" * 60)
        print("🔥 OPPOSITION — COUNTER")
        print(result["counter"])

        print("\n" + "=" * 60)
        print(f"⚖️  VERDICT: {result['decision']['status']}")
        print(f"📝 {result['decision']['verdict']}")
        print(f"📊 STRENGTH SCORE: {result['decision']['score']}/10")
        print(f"🏆 WINNING POINT: {result['decision']['winning_argument']}")
        print("=" * 60)

if __name__ == "__main__":
    main()
