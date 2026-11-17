# pyright: reportUndefinedVariable=false
# EXEMPLE 05 · Decisió de replanificació de la missió
# Fitxer original: ../src/05_langgraph_autonomous_mission_planner.py
# Què mostra: com la validació condueix a replanificar o informar.
# LLM: pot intervenir en altres nodes per interpretar o explicar la missió.
# Python: el router envia una missió NOT FEASIBLE a replan; la resta, a report.
# Fragment de lectura: el graf real té més nodes i transicions;
# aquest fragment selecciona la part que diferencia l'exemple 05 del 04.

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver


# 1. ROUTER: la viabilitat no la decideix el LLM, sinó Python.

def route_after_evaluation(
    state: AutonomousMissionState,
) -> Literal["replan", "report"]:
    if state.get("mission_status") == "NOT FEASIBLE":
        return "replan"

    return "report"


# 2. CREACIÓ DEL GRAF: cada node és una funció Python real.
builder = StateGraph(AutonomousMissionState)
builder.add_node("process_input", process_input_node)
builder.add_node("mission_planner", mission_planner_node)
builder.add_node("flight_check", flight_check_node)
builder.add_node("wind_check", wind_check_node)
builder.add_node("battery_check", battery_check_node)
builder.add_node("evaluate_plan", evaluate_plan_node)
builder.add_node("replanner", replanner_node)
builder.add_node("final_report", final_report_node)
builder.add_node("show_trace", show_trace_node)
builder.add_node("answer_question", answer_question_node)

builder.add_edge(START, "process_input")

# 3. TRANSICIÓ CLAU: després d'avaluar, replanificar o informar.
builder.add_conditional_edges("evaluate_plan", route_after_evaluation, {
    "replan": "replanner",
    "report": "final_report",
})
builder.add_edge("replanner", "final_report")
builder.add_edge("final_report", END)

# IMPORTANT: s'han omès les transicions entre process_input, el planificador,
# les comprovacions i evaluate_plan. Consulteu el codi complet per veure-les.

# 4. MEMÒRIA: LangGraph conserva l'estat per sessió.
memory = InMemorySaver()
autonomous_mission_graph = builder.compile(checkpointer=memory)
