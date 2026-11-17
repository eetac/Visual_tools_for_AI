# pyright: reportUndefinedVariable=false
# EXEMPLE 07 · Router i node add de LangGraph
# Fitxer original: ../src/07_shopping_list_langgraph.py
# Què mostra: la crida al LLM, router, nodes, construcció i execució del graf.
# LLM: en un pas anterior pot haver classificat la petició com a add/remove/etc.
# Python: route_after_input retorna el nom del node; add_node crida l'eina real.
# Fragment de lectura: els nodes i el prompt complet són a code/src/.

from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver


# 1. MODEL: Qwen interpreta l'usuari i retorna una acció en JSON.
llm = ChatOllama(model="qwen3.5:9b", temperature=0, format="json", reasoning=False)

# Fragment de process_input_node(): system_prompt és definit dins del node.
response = llm.invoke([
    ("system", system_prompt),
    ("human", state["user_input"]),
])
# Python transforma aquest JSON en els camps de ShoppingState.


# 2. ROUTER: ja NO pregunta al LLM; només llegeix state["action"].

def route_after_input(state: ShoppingState) -> Literal["add", "remove", "replace", "show", "other"]:
    action = state.get("action", "other")
    print(f"[ROUTER] {action}")
    return action


def add_node(state: ShoppingState) -> dict:
    # El node executa la funció; el router anterior només ha triat el camí.
    print("[NODE] add")
    return add_products.invoke({
        "shopping_list": state.get("shopping_list", []),
        "products": state.get("products", []),
        "last_product": state.get("last_product", ""),
    })


# 4. CREACIÓ DEL GRAF: connectar cada node amb el router.
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


# 5. COMPILACIÓ I EXECUCIÓ amb memòria per conversa.
memory = InMemorySaver()
shopping_graph = builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "shopping-session"}}
result = shopping_graph.invoke({"user_input": user_input}, config=config)
