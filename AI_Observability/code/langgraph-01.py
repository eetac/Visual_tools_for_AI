builder = StateGraph(ShoppingState)

builder.add_node(
    "process_input",
    process_input_node
)

builder.add_node(
    "add",
    add_node
)

builder.add_edge(
    START,
    "process_input"
)