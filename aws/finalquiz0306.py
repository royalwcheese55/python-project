import re

# ----------------------------
# Tools
# ----------------------------

def search_tool(query):
    knowledge = {
        "capital of france": "Paris",
        "capital of japan": "Tokyo",
        "openai founder": "Sam Altman"
    }
    return knowledge.get(query.lower(), "Unknown")


def calculator(expression):
    return str(eval(expression))


# ----------------------------
# Agent
# ----------------------------

def agent(question):
    thoughts = []
    actions = []
    observations = []

    results = []

    # split multi-step queries
    parts = re.split(r"\band\b", question.lower())

    for part in parts:
        part = part.strip()

        # detect math
        math_match = re.search(r"\d+\s*[\+\-\*\/]\s*\d+", part)

        if math_match:
            expr = math_match.group()

            thoughts.append(f"I need to calculate {expr}")
            actions.append(f"calculator({expr})")

            result = calculator(expr)
            observations.append(result)

            results.append(result)

        # detect knowledge queries
        elif "capital of france" in part:
            thoughts.append("I should search the capital of France")
            actions.append("search_tool(capital of france)")

            result = search_tool("capital of france")
            observations.append(result)

            results.append(result)

        elif "capital of japan" in part:
            thoughts.append("I should search the capital of Japan")
            actions.append("search_tool(capital of japan)")

            result = search_tool("capital of japan")
            observations.append(result)

            results.append(result)

        elif "openai founder" in part:
            thoughts.append("I should search the OpenAI founder")
            actions.append("search_tool(openai founder)")

            result = search_tool("openai founder")
            observations.append(result)

            results.append(result)

    answer = " and ".join(results)

    return answer


print(agent("What is the capital of France?"))
# Paris

print(agent("What is 8 * 7?"))
# 56

print(agent("What is the capital of Japan and what is 5*6?"))
# Tokyo and 30