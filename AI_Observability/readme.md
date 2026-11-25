# AI, visualization and observability

This manual introduces the concepts and tools used to build applications with language models. The papers follow a journey from the basics of LLMs to their local execution, creating agents, searching with RAG, connecting to tools using MCP, and observability of applications.

## Table of contents

1. [LLM (Large Language Model)](./docs/01_llm.md)
2. [Ollama: Install and run locally](./docs/02_ollama.md)
3. [LangChain and LangGraph](./docs/03_langchain_langgraph.md)
4. [RAG (Retrieval-Augmented Generation)](./docs/04_rag.md)
5. [Vector databases](./docs/04.1_vector_databases.md)
6. [MCP (Model Context Protocol)](./docs/05_MCP.md)
7. [Observability with Opik and Opentelemetry and application examples](./docs/06_observalility.md)
8. [Hermes](./docs/07_hermes.md) — document pending content
9. [Examples](./docs/08_examples.md)

## Summary of documents

### 1. LLM (Large Language Model)

Explains what a language model is, what tasks it can do, and how it generates token-by-token responses. It also presents the stages of processing and differentiates training from inference.

**Document:** [01_llm.md](./docs/01_llm.md)

### 2. Ollama

Describes Ollama as a tool for downloading and running language models locally. It includes instructions for installing it on macOS, choosing and downloading models, running them, and checking their memory and GPU usage.

**Document:** [02_ollama.md](./docs/02_ollama.md)

### 3. LangChain and LangGraph

Introduces LangChain to connect LLM with tools and resources, and LangGraph to define explicit flows with state, nodes, routing, and conditional transitions. Includes examples of how a natural language request can trigger Python functions.

**Document:** [03_langchain_langgraph.md](./docs/03_langchain_langgraph.md)

### 4. RAG (RAG Retrieval-Augmented Generation)

Explains how RAG retrieves information from an external source, adds it to the model context, and generates a response based on that information. It also introduces semantic searches and the use of Weaviate as a vector database to retrieve recipes.

**Document:** [04_rag.md](./docs/04_rag.md)

### 5. Vector databases

Explains what vector databases are, how they store information through embeddings and how they allow searches by semantic similarity. It introduces Weaviate as an example vector database, its main functionalities and the differences between local execution and Weaviate Cloud.

**Document:** [04.1_vector_databases.md](./docs/04.1_vector_databases.md)

### 6. MCP (Model Context Protocol)

Describes the MCP protocol and its client-server architecture: host, client, and server. It summarizes the functionality that a server can expose—tools, resources, and prompts—and the communication flow between the application and the server.

**Document:** [05_MCP.md](./docs/05_MCP.md)

### 7. Observability with Opik, Opentelemetry and LangSmith

Enter traces, spans, conversations, and metrics like latency, token consumption, and errors. It explains the configuration of Opik and the configuration of Opentelemetry (+ grafana) and the query of logs, dashboards and detailed traces. And the same for LangSmith.

**Document:** [06_observalility.md](./docs/06_observalility.md)

### 8. Hermes

The file intended for this topic has no content yet. The integration with Hermes to generate weekly menu proposals, validate them with Python, and use recipes retrieved from Weaviate is currently described in [example 10 of the observability document](./docs/06_observalility.md).

**Document:** [07_hermes.md](./docs/07_hermes.md)

### 9. Examples

Collect Python examples from agents, LangGraph, Weaviate and a weekly schedule with Hermes.

**Document:** [08_examples.md](./docs/08_examples.md)
