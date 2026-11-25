
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3.5:9b",
    temperature=0,
)

response = llm.invoke("Explain to me what LangChain is in two sentences.")

print(response.content)
