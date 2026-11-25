# pyright: reportUndefinedVariable=false
# EXAMPLE 07 · Router and add node of LangGraph
# Original file: ../src/07_shopping_list_langgraph.py
# What it shows: The call to the LLM, router, nodes, graph construction and execution.
# LLM: In a previous step you may have classified the request as add/remove/etc.
# Python: route_after_input return node name; add_node calls the actual tool.
# Read Snippet: Nodes and full prompt are in code/src/.

from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver


# 1. MODEL: Qwen interprets the user and returns an action in JSON.
llm = ChatOllama(model="qwen3.5:9b", temperature=0, format="json", reasoning=False)

# Fragment of process_input_node(): system_prompt is defined inside the node.
response = llm.invoke([
    ("system", system_prompt),
    ("human", state["user_input"]),
])
# Python transforms this JSON into ShoppingState fields.


# 2. ROUTER: NO longer asks the LLM; just read state["action"].

def route_after_input(state: ShoppingState) -> Literal["add", "remove", "replace", "show", "other"]:
    action = state.get("action", "other")
    print(f"[ROUTER] {action}")
    return action


def add_node(state: ShoppingState) -> dict:
    # The node executes the function; the previous router only chose the path.
    print("[NODE] add")
    return add_products.invoke({
        "shopping_list": state.get("shopping_list", []),
        "products": state.get("products", []),
        "last_product": state.get("last_product", ""),
    })


# 4. CREATION OF THE GRAPH: connect each node to the router.
builder = StateGraph(ShoppingState)
builder.add_node("process_input", process_input_node)
builder.add_node("add", add_node)
builder.add_node("remove", remove_node)
builder.add_node("replace", replace_node)
builder.add_node("show", show_node)
builder.add_node("other", other_node)

builder.add_edge(START, "process_input")
builder.add_conditional_edges("process_input", route_after_input, {
    "add": "add", "remove": "remove", "replace": "replace",
    "show": "show", "other": "other",
})
for name in ("add", "remove", "replace", "show", "other"):
    builder.add_edge(name, END)


# 5. COMPILATION AND EXECUTION with memory per conversation.
memory = InMemorySaver()
shopping_graph = builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "shopping-session"}}
result = shopping_graph.invoke({"user_input": user_input}, config=config)
