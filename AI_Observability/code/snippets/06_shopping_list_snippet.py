# pyright: reportUndefinedVariable=false
# EXEMPLE 06 · Eina per afegir productes a la llista
# Fitxer original: ../src/06_shopping_list.py
# Què mostra: crear el model, definir l'eina i connectar-la amb l'agent.
# LLM: interpreta la petició i pot triar l'eina add_product.
# Python: comprova duplicats i actualitza la llista; el LLM no la modifica directament.
# Fragment de lectura: remove_product, replace_product, show_list i el prompt
# complet són al fitxer original; el snippet en resumeix la configuració.

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# 1. MODEL I ESTAT PYTHON
llm = ChatOllama(model="qwen3.5:9b", temperature=0)
shopping_list = []


# 2. EINA: el LLM la pot seleccionar, però Python modifica la llista.

def normalize_product(product: str) -> str:
    return product.strip().lower()


@tool
def add_product(product: str) -> str:
    """Add a product to the shopping list."""

    product = normalize_product(product)

    print(f"[TOOL] add_product({product})")

    if product in shopping_list:
        return f"{product} ya está en la lista."

    shopping_list.append(product)

    return f"He añadido {product}."


# 3. AGENT: quatre eines disponibles per a la gestió de la llista.
# El system_prompt complet inclou traducció al castellà i correccions.
agent = create_agent(
    model=llm,
    tools=[add_product, remove_product, replace_product, show_list],
    system_prompt=(
        "You are a shopping list assistant. "
        "Always use the provided tools to add, remove, replace or show products. "
        "Always answer in Spanish."
    ),
)


# 4. EXECUCIÓ I MEMÒRIA CONVERSACIONAL (fragment del bucle principal).
# messages inclou l'historial de la conversa, no només l'últim missatge.
messages.append({"role": "user", "content": user_input})
result = agent.invoke({"messages": messages})
messages = result["messages"]
print("AGENT:", messages[-1].content)
