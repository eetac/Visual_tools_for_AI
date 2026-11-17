# pyright: reportUndefinedVariable=false
# EXEMPLE 03 · Comprovació de la seguretat del vent
# Fitxer original: ../src/03_my_drone_mission_agent.py
# Què mostra: eina determinista, crida directa des de Python i ús del LLM.
# LLM: només intervé per explicar resultats; no selecciona aquesta eina.
# Python: valida les dades i compara la velocitat amb el límit de seguretat.
# La decisió safe/unsafe és una regla Python, NO una opinió del LLM.
# Fragment de lectura: els blocs finals pertanyen a analyse_mission()
# i answer_question(); no constitueixen un programa executable aïlladament.

from langchain_ollama import ChatOllama
from langchain.tools import tool


# 1. El model només serveix per explicar resultats o respondre preguntes.
llm = ChatOllama(model="qwen3.5:9b", temperature=0, reasoning=False)


# 2. La comprovació s'implementa amb regles Python.

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

    # Regla determinista: el límit també es considera segur.
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


# 3. Fragment d'analyse_mission(): PYTHON invoca directament l'eina.
# No és el LLM qui decideix cridar-la en aquest exemple.
if state.wind_speed_kmh is not None and state.max_safe_wind_speed_kmh is not None:
    wind_result = check_wind_safety.invoke({
        "wind_speed_kmh": state.wind_speed_kmh,
        "max_safe_wind_speed_kmh": state.max_safe_wind_speed_kmh,
    })


# 4. Fragment d'answer_question(): el LLM interpreta els resultats ja calculats.
# system_prompt i user_input es preparen en aquesta funció del codi complet.
response = llm.invoke(
    [("system", system_prompt), ("human", user_input)],
    reasoning=False,
)
