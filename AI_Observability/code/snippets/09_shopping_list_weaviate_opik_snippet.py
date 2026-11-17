# pyright: reportUndefinedVariable=false
# EXEMPLE 09 · Observabilitat d'Ollama i Weaviate amb Opik
# Fitxer original: ../src/09_shopping_list_weaviate_opik.py
# Què mostra: instrumentar les crides al LLM i connectar Opik amb LangGraph.
# LLM: s'executa dins de model.invoke(messages).
# Python: registra consum de tokens i nombre de receptes recuperades.
# Fragment de lectura: shopping_graph i query_target_vector són al fitxer original.

import os
from langchain_ollama import ChatOllama
from opik import opik_context, track
from opik.integrations.langchain import OpikTracer, track_langgraph
from weaviate.classes.query import Filter


# 1. MODEL: dos usos de Qwen, que s'observaran per separat.
MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
llm = ChatOllama(model=MODEL, temperature=0, format="json", reasoning=False)
rag_llm = ChatOllama(model=MODEL, temperature=0, reasoning=False)


# 2. SPAN DE LLM: embolcalla model.invoke i desa tokens.

@track(name="ollama_tokens", type="llm", capture_input=False, capture_output=False)
def invoke_with_opik_usage(model, messages, etapa: str):
    # Punt on s'executa el LLM; després se'n llegeix el consum.
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

    print(f"[OPIK] Tokens {etapa}: {usage or 'no disponibles'}")
    return answer


# 3. SPAN D'EINA: registra també el nombre de receptes recuperades.
@track(name="weaviate_near_text", type="tool", ignore_arguments=["collection"], capture_output=False)
def weaviate_near_text(collection, query: str, max_minutes: int):
    """Consulta vectorial; registra cantidad de candidatos obtenidos."""
    filters = Filter.by_property("tiempoMin").less_or_equal(max_minutes) if max_minutes > 0 else None
    kwargs = {"query": query, "limit": 100, "filters": filters}
    target_vector = query_target_vector(collection)
    if target_vector:
        kwargs["target_vector"] = target_vector

    result = collection.query.near_text(**kwargs)
    opik_context.update_current_span(output={"candidates_retrieved": len(result.objects)})
    return result


# 4. INSTRUMENTACIÓ DEL GRAF: aquesta és la nova connexió amb Opik.
# shopping_graph ja s'ha construït amb StateGraph al programa complet.
opik_tracer = OpikTracer(
    project_name="shopping-rag-weaviate",
    tags=["ollama", "langgraph", "weaviate", "rag"],
    metadata={"model": MODEL, "collection": COLLECTION},
)
shopping_graph = track_langgraph(shopping_graph, opik_tracer)

# A process_input_node() i search_recipe_node() es crida
# invoke_with_opik_usage(llm, ...) o invoke_with_opik_usage(rag_llm, ...).
