# pyright: reportUndefinedVariable=false
# EXAMPLE 01 · Agent with a weather tool
# Original file: ../src/01_simple_agent.py
# What it shows: Create the LLM, register the tool, create the agent and make a query.
# LLM: Decide if you need weather information.
# Python: Runs get_weather() and returns a SIMULATED data, not a real forecast.
# In this example the fragment shows the complete route.

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


# 1. MODEL: Qwen runs locally with Ollama.
load_dotenv()
llm = ChatOllama(model="qwen3.5:9b", temperature=2)


# 2. TOOL: The docstring helps the LLM know when to use it.

def get_weather(city: str) -> str:
    """Get weather for a given city."""

    # The docstring helps the agent understand what the function is for.
    print(f"[TOOL EXECUTED] get_weather(city={city})")

    # Mock response; it does not consult any real weather service.
    return f"It's always sunny in {city}!"


# 3. AGENT: LangChain makes the tool available to the LLM.
agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


# 4. EXECUTION: LLM can request the tool, LangChain executes it
# and then the model can write the final answer.
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What's the weather in San Francisco?",
    }]
})
print(result["messages"][-1].content)
