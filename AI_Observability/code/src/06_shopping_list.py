
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.tools import tool

# 1. Ollama
llm = ChatOllama(
    model="qwen3.5:9b",
    temperature=0,
)

# 2. Shopping list
shopping_list = []


# 3. Normalization function
def normalize_product(product: str) -> str:
    return product.strip().lower()


# 4. Tools
@tool
def add_product(product: str) -> str:
    """Add a product to the shopping list."""

    product = normalize_product(product)

    print(f"[TOOL] add_product({product})")

    if product in shopping_list:
        return f"{product} ya está en la lista."

    shopping_list.append(product)

    return f"He añadido {product}."


@tool
def remove_product(product: str) -> str:
    """Remove a product from the shopping list."""

    product = normalize_product(product)

    print(f"[TOOL] remove_product({product})")

    if product not in shopping_list:
        return f"{product} no está en la lista."

    shopping_list.remove(product)

    return f"He eliminado {product}."


@tool
def replace_product(old_product: str, new_product: str) -> str:
    """Replace a product when the user corrects or changes their choice."""

    old_product = normalize_product(old_product)
    new_product = normalize_product(new_product)

    print(f"[TOOL] replace_product({old_product}, {new_product})")

    if old_product not in shopping_list:
        return f"{old_product} no está en la lista."

    if old_product == new_product:
        return "El producto ya es el solicitado."

    if new_product in shopping_list:
        shopping_list.remove(old_product)
    else:
        index = shopping_list.index(old_product)
        shopping_list[index] = new_product

    return f"He sustituido {old_product} por {new_product}."


@tool
def show_list() -> str:
    """Show all products in the shopping list."""

    print("[TOOL] show_list()")

    if not shopping_list:
        return "La lista de la compra está vacía."

    return ", ".join(shopping_list)


# 5. Create agent
agent = create_agent(
    model=llm,
    tools=[
        add_product,
        remove_product,
        replace_product,
        show_list,
    ],
    system_prompt=(
        "You are a shopping list assistant. "

        "Always use the provided tools to add, remove, "
        "replace or show products. "

        "IMPORTANT: Before calling any tool, translate all "
        "product names into Spanish if necessary. "
        "Always pass Spanish product names to the tools. "

        "Keep product names consistent across operations. "
        "For example, milk and leche must refer to the same product. "

        "Preserve product details such as soy milk, "
        "lactose-free milk or whole milk. "

        "If the user corrects a previously added product, "
        "use replace_product instead of add_product. "

        "Use the conversation history to understand corrections "
        "and references to previous products. "

        "When adding multiple products, use one tool call per product. "

        "Never claim a product was added, removed or replaced "
        "unless the tool confirms the operation. "

        "When showing the list, report only products returned "
        "by show_list. Never invent products. "

        "Always answer in Spanish. "
        "Be concise."
    ),
)


# 6. Conversation history
messages = []


# 7. Main
print("Shopping List Assistant")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit", "salir"]:
        print("Goodbye!")
        break

    if not user_input:
        continue

    # Add the user's message to the conversation
    messages.append({
        "role": "user",
        "content": user_input,
    })

    # Execute the agent
    result = agent.invoke({
        "messages": messages
    })

    # Save the conversation history
    messages = result["messages"]

    # Display the response
    print("\nAGENT:", messages[-1].content)

    # Show the real Python shopping list
    print("[DEBUG] Shopping list:", shopping_list)

    print()
