# pyright: reportUndefinedVariable=false
# EXAMPLE 03 · Wind safety check
# Original file: ../src/03_my_drone_mission_agent.py
# What it shows: Deterministic tool, direct call from Python and use of LLM.
# LLM: intervenes only to explain results; do not select this tool.
# Python: Validate data and compare speed with safety limit.
# The safe/unsafe decision is a Python rule, NOT an LLM opinion.
# Read fragment: end blocks belong to analyse_mission()
# and answer_question(); they do not constitute a stand-alone executable program.

from langchain_ollama import ChatOllama
from langchain.tools import tool


# 1. The model is only used to explain results or answer questions.
llm = ChatOllama(model="qwen3.5:9b", temperature=0, reasoning=False)


# 2. Checking is implemented with Python rules.

@tool
def check_wind_safety(
    wind_speed_kmh: float,
    max_safe_wind_speed_kmh: float,
) -> dict:
    """
    Check whether the wind speed is safe for the drone.
    """

    print(
        "\n[TOOL EXECUTED] check_wind_safety("
        f"wind_speed_kmh={wind_speed_kmh}, "
        f"max_safe_wind_speed_kmh={max_safe_wind_speed_kmh})"
    )

    if wind_speed_kmh < 0:
        return {
            "status": "error",
            "message": "Wind speed cannot be negative.",
        }

    if max_safe_wind_speed_kmh <= 0:
        return {
            "status": "error",
            "message": (
                "Maximum safe wind speed must be greater than 0."
            ),
        }

    # Deterministic Rule: Boundary is also considered safe.
    wind_safe = (
        wind_speed_kmh <= max_safe_wind_speed_kmh
    )

    return {
        "status": "safe" if wind_safe else "unsafe",
        "wind_safe": wind_safe,
        "wind_speed_kmh": round(
            wind_speed_kmh,
            2,
        ),
        "max_safe_wind_speed_kmh": round(
            max_safe_wind_speed_kmh,
            2,
        ),
    }


# 3. Fragment of analyse_mission(): PYTHON invokes the tool directly.
# It is not the LLM that decides to call it in this example.
if state.wind_speed_kmh is not None and state.max_safe_wind_speed_kmh is not None:
    wind_result = check_wind_safety.invoke({
        "wind_speed_kmh": state.wind_speed_kmh,
        "max_safe_wind_speed_kmh": state.max_safe_wind_speed_kmh,
    })


# 4. Fragment of answer_question(): The LLM interprets the already calculated results.
# system_prompt and user_input are prepared in this full code function.
response = llm.invoke(
    [("system", system_prompt), ("human", user_input)],
    reasoning=False,
)
