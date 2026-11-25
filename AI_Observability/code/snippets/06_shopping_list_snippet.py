# pyright: reportUndefinedVariable=false
# EXAMPLE 06 · Tool to add products to the list
# Original file: ../src/06_shopping_list.py
# What it shows: Create the model, define the tool, and connect it to the agent.
# LLM: Interprets the request and can choose the tool add_product.
# Python: check for duplicates and update list; the LLM does not modify it directly.
# Reading Fragment: remove_product, replace_product, show_list and the prompt
# are in the original file; the snippet summarizes its configuration.

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# 1. PYTHON MODEL AND STATUS
llm = ChatOllama(model="qwen3.5:9b", temperature=0)
shopping_list = []


# 2. TOOL: LLM can select it, but Python modifies the list.

def normalize_product(product: str) -> str:
    return product.strip().lower()


@tool
def add_product(product: str) -> str:
    """Add a product to the shopping list."""

    product = normalize_product(product)

    print(f"[TOOL] add_product({product})")

    if product in shopping_list:
        return f"{product} is already on the list."

    shopping_list.append(product)

    return f"I added {product}."


# 3. AGENT: Four tools available for list management.
# The complete system_prompt includes Spanish translation and corrections.
agent = create_agent(
    model=llm,
    tools=[add_product, remove_product, replace_product, show_list],
    system_prompt=(
        "You are a shopping list assistant. "
        "Always use the provided tools to add, remove, replace or show products. "
        "Always answer in English."
    ),
)


# 4. EXECUTION AND CONVERSATIONAL MEMORY (main loop fragment).
# messages includes the conversation history, not just the last message.
messages.append({"role": "user", "content": user_input})
result = agent.invoke({"messages": messages})
messages = result["messages"]
print("AGENT:", messages[-1].content)
