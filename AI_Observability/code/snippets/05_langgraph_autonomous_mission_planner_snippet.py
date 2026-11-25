# pyright: reportUndefinedVariable=false
# EXAMPLE 05 · Mission replanning decision
# Original file: ../src/05_langgraph_autonomous_mission_planner.py
# What it shows: How validation leads to replanning or reporting.
# LLM: May intervene in other nodes to interpret or explain the mission.
# Python: Router sends NOT FEASIBLE mission to replan; the rest, to report.
# Reading Snippet: The real graph has more nodes and transitions;
# this snippet selects the part that differentiates example 05 from 04.

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver


# 1. ROUTER: Viability is not decided by the LLM, but by Python.

def route_after_evaluation(
    state: AutonomousMissionState,
) -> Literal["replan", "report"]:
    if state.get("mission_status") == "NOT FEASIBLE":
        return "replan"

    return "report"


# 2. BUILDING THE GRAPH: Each node is an actual Python function.
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

# 3. KEY TRANSITION: After assessing, replanning or reporting.
builder.add_conditional_edges("evaluate_plan", route_after_evaluation, {
    "replan": "replanner",
    "report": "final_report",
})
builder.add_edge("replanner", "final_report")
builder.add_edge("final_report", END)

# IMPORTANT: Skipped transitions between process_input, the scheduler,
# the checks and evaluate_plan. Check the full code to see them.

# 4. MEMORY: LangGraph retains state per session.
memory = InMemorySaver()
autonomous_mission_graph = builder.compile(checkpointer=memory)
