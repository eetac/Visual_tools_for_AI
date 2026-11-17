
# EXEMPLE 00 · Primera consulta a Ollama
# Fitxer original: ../src/00_test_ollama.py
# LLM: genera el text en executar llm.invoke(...).
# Python: configura el model, envia la pregunta i mostra la resposta.
# Aquest cas és tan breu que el snippet coincideix amb el programa complet.

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3.5:9b",
    temperature=0,
)

response = llm.invoke("Explícame qué es LangChain en dos frases.")

print(response.content)
