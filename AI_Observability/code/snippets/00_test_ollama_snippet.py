
# EXAMPLE 00 · First consultation in Ollama
# Original file: ../src/00_test_ollama.py
# LLM: Generate the text when running llm.invoke(...).
# Python: Set up the model, submit the question, and display the answer.
# This case is so short that the snippet matches the full program.

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3.5:9b",
    temperature=0,
)

response = llm.invoke("Explain to me what LangChain is in two sentences.")

print(response.content)
