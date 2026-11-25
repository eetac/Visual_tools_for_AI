# pyright: reportUndefinedVariable=false
# EXAMPLE 11 · Observability of the RAG with OpenTelemetry and Grafana
# Original file: ../src/11_shopping_list_weaviate_opentelemetry.py
# What it shows: LangGraph instrumentation, logging tokens and sending traces to Grafana.
# LLM: Ollama classifies requests and generates RAG responses, recording token consumption.
# Python: configure OpenTelemetry, create spans for nodes and log router decisions.
# OpenTelemetry: collects traces, durations, attributes and tokens of the different operations.
# Grafana: allows you to view executions, nodes traversed and consumption metrics.
# Observability data flow is performed via OTLP/HTTP to Tempo.
# Read Snippet: Amounts, full configuration, and auxiliary functions are in the original file.
# The final block corresponds to main() and shows how a LangGraph execution is registered.
# Docker and dashboard configuration is explained in 06_observalility.md.
# The snippet is self explanatory and not standalone executable.


# 1. Instrumentation initialization (amounts to full program).
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


# 2. An inference with the tokens associated with its span.
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


# 3. The graph node is a span; the decision is recorded as an attribute.
# The full implementation includes traceparent propagation between nodes.
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


# 4. The parent span wraps around a complete user query.
# Inside the actual main(), 'shopping_graph', 'user_input' and 'config' already exist.
#
# with tracer.start_as_current_span("langgraph.invoke"):
#     carrier = {}
#     propagator.inject(carrier)
#     result = shopping_graph.invoke(
#         {"user_input": user_input, "otel_traceparent": carrier["traceparent"]},
#         config=config,
#     )
# otel_provider.force_flush(timeout_millis=10000)
