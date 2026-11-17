# pyright: reportUndefinedVariable=false
# EXEMPLE 04 · Router de LangGraph per a la missió del dron
# Fitxer original: ../src/04_langgraph_drone_mission_agent.py
# Què mostra: el router, la creació del graf i la seva execució.
# LLM: pot haver interpretat la petició en un node anterior.
# Python: aquest router aplica condicions fixes; NO consulta el LLM.
# Fragment de lectura: els nodes i DroneMissionState es defineixen al codi complet.

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver


# 1. ROUTER: selecciona el següent node amb regles Python.

def route_after_input(
    state: DroneMissionState,
) -> Literal["flight", "wind", "battery", "report", "trace", "question"]:
    intent = state["intent"]

    if intent == "trace":
        return "trace"

    if intent == "question":
        return "question"

    if state.get("run_flight", False):
        return "flight"

    if state.get("run_wind", False):
        return "wind"

    # Per comprovar la bateria es necessita un vol calculat correctament.
    if (
        state.get("run_battery", False)
        and state.get("flight_result") is not None
        and state["flight_result"].get("status") == "success"
    ):
        return "battery"

    return "report"


# 2. CONSTRUCCIÓ: LangGraph connecta funcions Python amb transicions.
builder = StateGraph(DroneMissionState)

builder.add_node("process_input", process_input_node)
builder.add_node("flight_check", flight_check_node)
builder.add_node("wind_check", wind_check_node)
builder.add_node("battery_check", battery_check_node)
builder.add_node("final_report", final_report_node)
builder.add_node("show_trace", show_trace_node)
builder.add_node("answer_question", answer_question_node)

builder.add_edge(START, "process_input")
builder.add_conditional_edges("process_input", route_after_input, {
    "flight": "flight_check",
    "wind": "wind_check",
    "battery": "battery_check",
    "report": "final_report",
    "trace": "show_trace",
    "question": "answer_question",
})
builder.add_conditional_edges("flight_check", route_after_flight, {
    "wind": "wind_check", "battery": "battery_check", "report": "final_report",
})
builder.add_conditional_edges("wind_check", route_after_wind, {
    "battery": "battery_check", "report": "final_report",
})
builder.add_edge("battery_check", "final_report")
for node in ("final_report", "show_trace", "answer_question"):
    builder.add_edge(node, END)


# 3. MEMÒRIA I EXECUCIÓ: l'estat es manté per thread_id.
memory = InMemorySaver()
drone_mission_graph = builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "drone-mission-session"}}

# Fragment de main(): executar el graf no equival a invocar sempre el LLM.
result = drone_mission_graph.invoke({"user_input": user_input}, config=config)
