import json
from typing import Literal, TypedDict

from langchain.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


# 1. Shopping State
class ShoppingState(TypedDict, total=False):
    user_input: str
    shopping_list: list[str]
    last_product: str
    action: str
    products: list[str]
    old_product: str
    new_product: str
    response: str


# 2. Ollama
llm = ChatOllama(
    model="qwen3.5:9b",
    temperature=0,
    format="json",
    reasoning=False,
)


# 3. Tools
@tool
def add_products(shopping_list: list[str], products: list[str], last_product: str) -> dict:
    """Add products to a shopping list, avoiding duplicates."""
    print("[TOOL EXECUTED] add_products")

    new_list = shopping_list.copy()
    messages = []

    for product in products:
        if product in new_list:
            messages.append(f"{product} is already on the list.")
        else:
            new_list.append(product)
            last_product = product
            messages.append(f"Added: {product}.")

    return {
        "shopping_list": new_list,
        "last_product": last_product,
        "response": " ".join(messages) or "You have not specified any products.",
    }


@tool
def remove_products(shopping_list: list[str], products: list[str], last_product: str) -> dict:
    """Remove products from a shopping list."""
    print("[TOOL EXECUTED] remove_products")

    new_list = shopping_list.copy()
    messages = []

    for product in products:
        if product in new_list:
            new_list.remove(product)
            if last_product == product:
                last_product = ""
            messages.append(f"Removed: {product}.")
        else:
            messages.append(f"{product} is not on the list.")

    return {
        "shopping_list": new_list,
        "last_product": last_product,
        "response": " ".join(messages) or "You have not specified any products.",
    }


@tool
def replace_product(shopping_list: list[str], old_product: str, new_product: str, last_product: str) -> dict:
    """Replace one product in a shopping list with another."""
    print("[TOOL EXECUTED] replace_product")

    new_list = shopping_list.copy()

    if not old_product or not new_product:
        response = "Indicate which product you want to replace and with which one."
    elif old_product not in new_list:
        response = f"{old_product} is not on the list."
    elif old_product == new_product:
        response = f"You already have {new_product} in the list."
    else:
        index = new_list.index(old_product)
        new_list.remove(old_product)
        if new_product not in new_list:
            new_list.insert(index, new_product)
        last_product = new_product
        response = f"I have replaced {old_product} with {new_product}."

    return {"shopping_list": new_list, "last_product": last_product, "response": response}


@tool
def show_products(shopping_list: list[str]) -> str:
    """Show the current shopping list."""
    print("[TOOL EXECUTED] show_products")
    return "Shopping list: " + (", ".join(shopping_list) if shopping_list else "empty")


# 4. Nodes
def process_input_node(state: ShoppingState) -> dict:
    print("[NODE] process_input")

    system_prompt = f"""
            You are a shopping list assistant.
            Parses the message and returns ONLY a JSON object with these keys:
            "action", "products", "old_product", "new_product".

            - action: "add", "remove", "replace", "show" or "other".
            - products: list of products (to add or remove); if not used, [].
            - old_product and new_product: texts (to replace); if not used, "".
            - ALL product names in the JSON MUST be in SPANISH.
            - Translate yourself any product written in another language.
            - Do not use English names in JSON values, even if the user uses them.
            - Keep important details: "soy milk", "lactose free", etc.
            - To delete or replace, use the EXACT name in the current list.
            - If the user corrects himself ("but he wanted soy milk"), use replace
            and takes the last added product as the previous product, if applicable.
            - If you request multiple products to add, include them all in products.
            - Do not invent operations or products.

            Examples:
            "add milk" -> {{"action":"add","products":["leche"],"old_product":"","new_product":""}}
            "add butter and eggs" -> {{"action":"add","products":["mantequilla","huevos"],"old_product":"","new_product":""}}
            "remove milk" -> {{"action":"remove","products":["leche"],"old_product":"","new_product":""}}
            "but soy milk" -> {{"action":"replace","products":[],"old_product":"leche","new_product":"leche de soja"}}
            "what should I buy" -> {{"action":"show","products":[],"old_product":"","new_product":""}}

            Current list: {state.get('shopping_list', [])}
            Last product added: {state.get('last_product', '')}
            """

    response = llm.invoke([
        ("system", system_prompt),
        ("human", state["user_input"]),
    ])

    try:
        decision = json.loads(response.content)
        if not isinstance(decision, dict):
            raise ValueError("Bad JSON")
    except (ValueError, TypeError):
        return {"action": "other", "response": "I did not understand the request."}

    action = decision.get("action", "other")
    if action not in ("add", "remove", "replace", "show", "other"):
        action = "other"

    products = decision.get("products", [])
    if not isinstance(products, list):
        products = []
    products = [p.strip().lower() for p in products if isinstance(p, str) and p.strip()]

    old_product = decision.get("old_product", "")
    new_product = decision.get("new_product", "")
    old_product = old_product.strip().lower() if isinstance(old_product, str) else ""
    new_product = new_product.strip().lower() if isinstance(new_product, str) else ""

    return {
        "action": action,
        "products": products,
        "old_product": old_product,
        "new_product": new_product,
        "response": "",
    }



def route_after_input(state: ShoppingState) -> Literal["add", "remove", "replace", "show", "other"]:
    action = state.get("action", "other")
    print(f"[ROUTER] {action}")
    return action



def add_node(state: ShoppingState) -> dict:
    print("[NODE] add")
    return add_products.invoke({
        "shopping_list": state.get("shopping_list", []),
        "products": state.get("products", []),
        "last_product": state.get("last_product", ""),
    })


def remove_node(state: ShoppingState) -> dict:
    print("[NODE] remove")
    return remove_products.invoke({
        "shopping_list": state.get("shopping_list", []),
        "products": state.get("products", []),
        "last_product": state.get("last_product", ""),
    })


def replace_node(state: ShoppingState) -> dict:
    print("[NODE] replace")
    old_product = state.get("old_product") or state.get("last_product", "")
    new_product = state.get("new_product", "")
    result = replace_product.invoke({
        "shopping_list": state.get("shopping_list", []),
        "old_product": old_product,
        "new_product": new_product,
        "last_product": state.get("last_product", ""),
    })
    return result


def show_node(state: ShoppingState) -> dict:
    print("[NODE] show")
    response = show_products.invoke({"shopping_list": state.get("shopping_list", [])})
    return {"response": response}


def other_node(state: ShoppingState) -> dict:
    print("[NODE] other")
    return {"response": state.get("response") or "I can add, remove, replace and display products."}


# 5. Graph
builder = StateGraph(ShoppingState)

builder.add_node("process_input", process_input_node)
builder.add_node("add", add_node)
builder.add_node("remove", remove_node)
builder.add_node("replace", replace_node)
builder.add_node("show", show_node)
builder.add_node("other", other_node)

builder.add_edge(START, "process_input")

builder.add_conditional_edges(
    "process_input",
    route_after_input,
    {
        "add": "add",
        "remove": "remove",
        "replace": "replace",
        "show": "show",
        "other": "other",
    },
)

builder.add_edge("add", END)
builder.add_edge("remove", END)
builder.add_edge("replace", END)
builder.add_edge("show", END)
builder.add_edge("other", END)

memory = InMemorySaver()
shopping_graph = builder.compile(checkpointer=memory)

THREAD_ID = "shopping-session"
config = {"configurable": {"thread_id": THREAD_ID}}


# 6. Main
def main() -> None:
    print("LangGraph Shopping List Assistant")
    print("Type 'reset' to clear the list or 'exit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "salir"):
            break

        if user_input.lower() == "reset":
            memory.delete_thread(THREAD_ID)
            print("AGENT: List deleted.\n")
            continue

        print("\n[LANGGRAPH] Running graph...")

        try:
            result = shopping_graph.invoke({"user_input": user_input}, config=config)
        except Exception as error:
            print(f"[ERROR] {error}\n")
            continue

        print("AGENT:", result["response"])
        print("[DEBUG] Actual list:", result.get("shopping_list", []), "\n")


if __name__ == "__main__":
    main()
