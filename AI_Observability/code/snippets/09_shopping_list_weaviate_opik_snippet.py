# pyright: reportUndefinedVariable=false
# EXAMPLE 09 · Observability of Ollama and Weaviate with Opik
# Original file: ../src/09_shopping_list_weaviate_opik.py
# What it shows: Instrument calls to LLM and connect Opik to LangGraph.
# LLM: Runs inside model.invoke(messages).
# Python: Log token consumption and number of recipes retrieved.
# Read fragment: shopping_graph and query_target_vector are in the original file.

import os
from langchain_ollama import ChatOllama
from opik import opik_context, track
from opik.integrations.langchain import OpikTracer, track_langgraph
from weaviate.classes.query import Filter


# 1. MODEL: Two uses of Qwen, which will be noted separately.
MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
llm = ChatOllama(model=MODEL, temperature=0, format="json", reasoning=False)
rag_llm = ChatOllama(model=MODEL, temperature=0, reasoning=False)


# 2. LLM SPAN: Wrap model.invoke and save tokens.

@track(name="ollama_tokens", type="llm", capture_input=False, capture_output=False)
def invoke_with_opik_usage(model, messages, etapa: str):
    # Point where the LLM is executed; then the consumption is read.
    answer = model.invoke(messages)
    usage = answer.usage_metadata or {}

    if usage:
        opik_context.update_current_span(
            model=MODEL,
            provider="ollama",
            metadata={"etapa": etapa},
            usage={
                "prompt_tokens": usage.get("input_tokens", 0),
                "completion_tokens": usage.get("output_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
        )
    else:
        opik_context.update_current_span(
            model=MODEL, provider="ollama", metadata={"etapa": etapa}
        )

    print(f"[OPIK] Tokens {etapa}: {usage or 'not available'}")
    return answer


# 3. TOOL SPAN: Also records the number of recipes retrieved.
@track(name="weaviate_near_text", type="tool", ignore_arguments=["collection"], capture_output=False)
def weaviate_near_text(collection, query: str, max_minutes: int):
    """Vector query; records the number of candidates obtained."""
    filters = Filter.by_property("tiempoMin").less_or_equal(max_minutes) if max_minutes > 0 else None
    kwargs = {"query": query, "limit": 100, "filters": filters}
    target_vector = query_target_vector(collection)
    if target_vector:
        kwargs["target_vector"] = target_vector

    result = collection.query.near_text(**kwargs)
    opik_context.update_current_span(output={"candidates_retrieved": len(result.objects)})
    return result


# 4. GRAPH INSTRUMENTATION: This is the new connection to Opik.
# shopping_graph has already been built with StateGraph in the full program.
opik_tracer = OpikTracer(
    project_name="shopping-rag-weaviate",
    tags=["ollama", "langgraph", "weaviate", "rag"],
    metadata={"model": MODEL, "collection": COLLECTION},
)
shopping_graph = track_langgraph(shopping_graph, opik_tracer)

# process_input_node() and search_recipe_node() are called
# invoke_with_opik_usage(llm, ...) or invoke_with_opik_usage(rag_llm, ...).
