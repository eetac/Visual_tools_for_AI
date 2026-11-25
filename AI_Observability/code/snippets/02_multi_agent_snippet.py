# pyright: reportUndefinedVariable=false
# EXAMPLE 02 · Delegation to a flight sub-agent
# Original file: ../src/02_multi_agent.py
# What it shows: Two subagents, a delegation tool, and the supervisor.
# LLM supervisor: You can choose this tool according to the user's request.
# Python: Invoke the subagent and extract the contents of its response.
# Reading fragment: get_weather, calculate_flight_time and ask_weather_agent
# are defined in the full file. Here is the connection.

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# 1. All agents use the SAME model, with different instructions.
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


# 2. Supervisor does not execute calculate_flight_time directly:
# calls a tool that delegates the work to flight_agent.

@tool
def ask_flight_agent(query: str) -> str:
    """Delegate drone flight-time calculations to the flight specialist agent."""

    print("\n[SUBAGENT CALLED] flight_agent")
    print(f"[INPUT SUBAGENT] {query}")

    # The query is converted to a message for the subagent.
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


# 3. Supervisor can call ask_weather_agent or ask_flight_agent.
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


# 4. The query is initiated by the supervisor, who can delegate both tasks.
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
