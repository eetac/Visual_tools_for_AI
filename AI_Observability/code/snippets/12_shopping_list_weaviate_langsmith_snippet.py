# pyright: reportUndefinedVariable=false
# EXAMPLE 12: Observability of the RAG with LangSmith
# Original file: ../src/12_shopping_list_weaviate_langsmith.py
# What it shows: LangGraph and Ollama native tracing, tokens and Weaviate manual run.
# LLM: Ollama classifies the request and generates the RAG response with retrieved recipes.
# Python: Set up the project, run the graph, query Weaviate and read the tokens.
# LangSmith: Automatically registers nodes, router, tools and inferences.
# Read Snippet: Amounts, constants and helper functions are in the original file.
# Commented blocks belong to search_recipes() and main(); the snippet is not executable by itself.

# 1. LangSmith project setup
load_dotenv()
PROJECT = os.getenv("LANGSMITH_PROJECT", "shopping-rag-weaviate-langsmith").strip() or "shopping-rag-weaviate-langsmith"

# 2. Inference automatically instrumented by LangChain
# The run_name identifies the stage. Tokens are also displayed in the terminal.
def invoke_with_langsmith_usage(model, messages, etapa: str):
    answer = model.invoke(messages, config={
        "run_name": f"ollama.{etapa}",
        "metadata": {"llm.etapa": etapa},
    })
    usage = getattr(answer, "usage_metadata", None) or {}
    metadata = getattr(answer, "response_metadata", None) or {}
    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    if input_tokens is None:
        input_tokens = metadata.get("prompt_eval_count")
    if output_tokens is None:
        output_tokens = metadata.get("eval_count")
    total_tokens = usage.get("total_tokens")
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = int(input_tokens) + int(output_tokens)
    shown_usage = {"input_tokens": input_tokens, "output_tokens": output_tokens,
                   "total_tokens": total_tokens}
    print(f"[LANGSMITH] Tokens {etapa}: {shown_usage if any(v is not None for v in shown_usage.values()) else 'not available'}")
    return answer


# 3. Manually instrumenting direct search in Weaviate
def weaviate_near_text(collection, query: str, max_minutes: int):
    """Vector query; records the number of candidates obtained."""
    with ls.trace("weaviate_near_text", run_type="chain", inputs={
        "collection": COLLECTION, "query": query, "max_minutes": max_minutes,
    }) as run:
        filters = Filter.by_property("tiempoMin").less_or_equal(max_minutes) if max_minutes > 0 else None
        kwargs = {"query": query, "limit": 100, "filters": filters}
        target_vector = query_target_vector(collection)
        if target_vector:
            kwargs["target_vector"] = target_vector
        result = collection.query.near_text(**kwargs)
        if run is not None:
            run.end(outputs={"candidates_retrieved": len(result.objects)})
        return result


# 4. Metadata of search_recipes()
# Counters are logged after filtering ingredients.
# run = get_current_run_tree()
# if run is not None:
#     run.add_metadata({
#         "rag.recipes.candidates_retrieved": len(result.objects),
#         "rag.recipes.matches_returned": len(matches),
#         "rag.recipes.required_ingredients_count": len(required_ingredients),
#     })
# return matches

# 5. CONNECTION WITH LANGGRAPH
# The context records the root run, nodes, router, and child calls.
# The full program validates the key and avoids mixing project and agent.
# tracing_enabled = os.getenv("LANGSMITH_TRACING", "true").strip().lower() in ("true", "1")
# client = ls.Client() if tracing_enabled else None
# try:
#     with ls.tracing_context(enabled=tracing_enabled, client=client, project_name=PROJECT):
#         result = shopping_graph.invoke(
#             {"user_input": user_input},
#             config={**config, "run_name": "langgraph.invoke",
#                     "metadata": {"thread_id": THREAD_ID, "collection": COLLECTION}},
#         )
# finally:
#     if client is not None:
#         wait_for_all_tracers()
#         client.flush()
