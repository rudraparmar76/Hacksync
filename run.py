from core.schema import Factor
from engines.debate_engine import run_debate

input_data = {
    "factors": [
        {
            "id": "F1",
            "name": "Breadth of Scientific and Societal Topics Covered",
            "description": "The material encompasses a wide array of subjects from core biological processes and animal classification to environmental management, energy generation, modern biotechnology, microbiology, and social health."
        }
    ]
}

def main():
    for f in input_data["factors"]:
        factor = Factor(**f)
        result = run_debate(factor)

        print("\n==============================")
        print(f"FACTOR {factor.id}")
        print("==============================")
        print(result["transcript"])
        print("\nDECISION:", result["decision"])

if __name__ == "__main__":
    main()
