# pyright: reportUndefinedVariable=false
# EXEMPLE 01 · Agent amb una eina meteorològica
# Fitxer original: ../src/01_simple_agent.py
# Què mostra: crear el LLM, registrar l'eina, crear l'agent i fer una consulta.
# LLM: decideix si necessita informació meteorològica.
# Python: executa get_weather() i retorna una dada SIMULADA, no una previsió real.
# En aquest exemple el fragment mostra el recorregut complet.

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


# 1. MODEL: Qwen s'executa localment amb Ollama.
load_dotenv()
llm = ChatOllama(model="qwen3.5:9b", temperature=2)


# 2. EINA: la docstring ajuda el LLM a saber quan pot usar-la.

def get_weather(city: str) -> str:
    """Get weather for a given city."""

    # La docstring ajuda l'agent a entendre per a què serveix la funció.
    print(f"[TOOL EXECUTED] get_weather(city={city})")

    # Resposta simulada; no consulta cap servei meteorològic real.
    return f"It's always sunny in {city}!"


# 3. AGENT: LangChain posa l'eina a disposició del LLM.
agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


# 4. EXECUCIÓ: el LLM pot demanar l'eina, LangChain l'executa
# i després el model pot redactar la resposta final.
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What's the weather in San Francisco?",
    }]
})
print(result["messages"][-1].content)
