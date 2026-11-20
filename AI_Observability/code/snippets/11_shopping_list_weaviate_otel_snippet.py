# pyright: reportUndefinedVariable=false
# EXEMPLE 11 · Observabilitat del RAG amb OpenTelemetry i Grafana
# Fitxer original: ../src/11_shopping_list_weaviate_otel.py
# Què mostra: instrumentació de LangGraph, registre de tokens i enviament de traces a Grafana.
# LLM: Ollama classifica les peticions i genera respostes RAG, registrant el consum de tokens.
# Python: configura OpenTelemetry, crea spans per als nodes i registra les decisions del router.
# OpenTelemetry: recull traces, durades, atributs i tokens de les diferents operacions.
# Grafana: permet visualitzar les execucions, els nodes recorreguts i les mètriques de consum.
# El flux de dades d'observabilitat es realitza mitjançant OTLP/HTTP cap a Tempo.
# Fragment de lectura: els imports, la configuració completa i les funcions auxiliars es troben al fitxer original.
# El bloc final correspon a main() i mostra com es registra una execució de LangGraph.
# La configuració de Docker i del dashboard s'explica a 06_observability.md.
# El snippet és explicatiu i no és executable de manera independent.


# 1. Inicialització de la instrumentació (imports al programa complet).
otel_provider = TracerProvider(
    resource=Resource.create({"service.name": "shopping-rag-weaviate-otel"}),
    sampler=ParentBased(ALWAYS_ON),
)
otel_provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
    )
)
trace.set_tracer_provider(otel_provider)
tracer = trace.get_tracer("shopping-rag-weaviate-otel")


# 2. Una inferència amb els tokens associats al seu span.
def invoke_with_otel_usage(model, messages, etapa: str):
    with tracer.start_as_current_span(f"ollama.{etapa}") as span:
        span.set_attribute("gen_ai.provider.name", "ollama")
        answer = model.invoke(messages)
        usage = getattr(answer, "usage_metadata", None) or {}
        if usage.get("input_tokens") is not None:
            span.set_attribute("gen_ai.usage.input_tokens", usage["input_tokens"])
        if usage.get("output_tokens") is not None:
            span.set_attribute("gen_ai.usage.output_tokens", usage["output_tokens"])
        if usage.get("total_tokens") is not None:
            span.set_attribute("rag.tokens.total", usage["total_tokens"])
        print(f"[OTEL] Tokens {etapa}: {usage}")
        return answer


# 3. El node del graf és un span; la decisió es registra com a atribut.
# La implementació completa inclou propagació de traceparent entre nodes.
def observed_node(name, fn):
    @wraps(fn)
    def wrapped(state):
        parent = state.get("otel_traceparent", "")
        ctx = propagator.extract({"traceparent": parent}) if parent else None
        with tracer.start_as_current_span(f"langgraph.node.{name}", context=ctx) as span:
            result = fn(state)
            if name == "process_input":
                span.set_attribute("langgraph.route", result.get("action", "other"))
            return result
    return wrapped


# 4. El span principal envolta una consulta completa de l'usuari.
# Dins del main() real, 'shopping_graph', 'user_input' i 'config' ja existeixen.
#
# with tracer.start_as_current_span("langgraph.invoke"):
#     carrier = {}
#     propagator.inject(carrier)
#     result = shopping_graph.invoke(
#         {"user_input": user_input, "otel_traceparent": carrier["traceparent"]},
#         config=config,
#     )
# otel_provider.force_flush(timeout_millis=10000)
