# pyright: reportUndefinedVariable=false
# EXEMPLE 02 · Delegació a un subagent de vols
# Fitxer original: ../src/02_multi_agent.py
# Què mostra: dos subagents, una eina de delegació i el supervisor.
# LLM supervisor: pot triar aquesta eina segons la petició de l'usuari.
# Python: invoca el subagent i extreu el contingut de la seva resposta.
# Fragment de lectura: get_weather, calculate_flight_time i ask_weather_agent
# es defineixen al fitxer complet. Aquí se'n mostra la connexió.

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# 1. Tots els agents fan servir el MATEIX model, amb diferents instruccions.
llm = ChatOllama(model="qwen3.5:9b", temperature=0)

weather_agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt=(
        "You are a weather specialist. "
        "Answer weather-related questions using the available weather tool."
    ),
)

flight_agent = create_agent(
    model=llm,
    tools=[calculate_flight_time],
    system_prompt=(
        "You are a drone flight specialist. "
        "Use the available tool to calculate drone flight times."
    ),
)


# 2. El supervisor no executa calculate_flight_time directament:
# crida una eina que delega la feina a flight_agent.

@tool
def ask_flight_agent(query: str) -> str:
    """Delegate drone flight-time calculations to the flight specialist agent."""

    print("\n[SUBAGENT CALLED] flight_agent")
    print(f"[SUBAGENT INPUT] {query}")

    # La consulta es converteix en un missatge per al subagent.
    result = flight_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )

    return result["messages"][-1].content


# 3. El supervisor pot cridar ask_weather_agent o ask_flight_agent.
supervisor_agent = create_agent(
    model=llm,
    tools=[ask_weather_agent, ask_flight_agent],
    system_prompt=(
        "You are a supervisor agent that coordinates specialized agents. "
        "Use ask_weather_agent for weather-related questions. "
        "Use ask_flight_agent for drone flight-time calculations. "
        "If the user asks for information requiring both specialists, "
        "delegate to both and combine their results into one final answer."
    ),
)


# 4. La consulta inicia el supervisor, que pot delegar les dues tasques.
result = supervisor_agent.invoke({
    "messages": [{
        "role": "user",
        "content": (
            "I want to fly a drone in Barcelona. "
            "Tell me the weather and calculate how long it would take "
            "to fly 12 km at 40 km/h."
        ),
    }]
})
print(result["messages"][-1].content)
