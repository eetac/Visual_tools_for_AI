# pyright: reportUndefinedVariable=false
# EXAMPLE 04 · LangGraph router for drone mission
# Original file: ../src/04_langgraph_drone_mission_agent.py
# What it shows: the router, the creation of the graph and its execution.
# LLM: The request may have been interpreted on a previous node.
# Python: This router applies fixed conditions; DO NOT refer to the LLM.
# Read Snippet: Nodes and DroneMissionState are defined in full code.

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver


# 1. ROUTER: Select next node with Python rules.

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

    # A correctly calculated flight is required to check the battery.
    if (
        state.get("run_battery", False)
        and state.get("flight_result") is not None
        and state["flight_result"].get("status") == "success"
    ):
        return "battery"

    return "report"


# 2. BUILD: LangGraph connects Python functions to transitions.
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


# 3. MEMORY AND EXECUTION: State is maintained by thread_id.
memory = InMemorySaver()
drone_mission_graph = builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "drone-mission-session"}}

# Fragment of main(): running the graph is not equivalent to always invoking the LLM.
result = drone_mission_graph.invoke({"user_input": user_input}, config=config)
