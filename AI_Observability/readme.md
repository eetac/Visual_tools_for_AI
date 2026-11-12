# IA, visualització i observabilitat

Aquest manual presenta els conceptes i les eines utilitzats per construir aplicacions amb models de llenguatge. Els documents segueixen un recorregut des dels fonaments dels LLM fins a la seva execució local, la creació d’agents, la cerca amb RAG, la connexió amb eines mitjançant MCP i l’observabilitat de les aplicacions.

## Taula de continguts

1. [LLM (Large Language Model)](./docs/01_llm.md)
2. [Ollama: instal·lació i execució local](./docs/02_ollama.md)
3. [LangChain i LangGraph](./docs/03_langchain_langgraph.md)
4. [RAG (Retrieval-Augmented Generation) i bases de dades vectorials](./docs/04_rag.md)
5. [MCP (Model Context Protocol)](./docs/05_MCP.md)
6. [Observabilitat amb Opik i exemples d’aplicació](./docs/06_observalility.md)
7. [Hermes](./docs/07_hermes.md) — document pendent de contingut
8. [Exemples](./docs/08_examples.md)

## Resum dels documents

### 1. LLM (Large Language Model)

Explica què és un model de llenguatge, quines tasques pot fer i com genera respostes token a token. També presenta les etapes de processament i diferencia l’entrenament de la inferència.

**Document:** [01_llm.md](./01_llm.md)

### 2. Ollama

Descriu Ollama com a eina per descarregar i executar models de llenguatge localment. Inclou instruccions per instal·lar-lo a macOS, escollir i descarregar models, executar-los i comprovar-ne l’ús de memòria i GPU.

**Document:** [02_ollama.md](./02_ollama.md)

### 3. LangChain i LangGraph

Presenta LangChain per connectar LLM amb eines i recursos, i LangGraph per definir fluxos explícits amb estat, nodes, encaminament i transicions condicionals. Inclou exemples de com una petició en llenguatge natural pot activar funcions Python.

**Document:** [03_langchain_langgraph.md](./03_langchain_langgraph.md)

### 4. RAG (RAG Retrieval-Augmented Generation)

Explica com RAG recupera informació d’una font externa, l’afegeix al context del model i genera una resposta fonamentada en aquesta informació. També introdueix les cerques semàntiques i l’ús de Weaviate com a base de dades vectorial per recuperar receptes.

**Document:** [04_rag.md](./04_rag.md)

### 5. MCP (Model Context Protocol)

Descriu el protocol MCP i la seva arquitectura client-servidor: host, client i servidor. Resumeix les funcionalitats que pot exposar un servidor —eines, recursos i prompts— i el flux de comunicació entre l’aplicació i el servidor.

**Document:** [05_MCP.md](./05_MCP.md)

### 6. Observabilitat amb Opik

Introdueix traces, spans, converses i mètriques com la latència, el consum de tokens i els errors. Explica la configuració d’Opik i la consulta de logs, dashboards i traces detallades.

**Document:** [06_observalility.md](./06_observalility.md)

### 7. Hermes

El fitxer previst per a aquest tema encara no té contingut. La integració amb Hermes per generar propostes de menús setmanals, validar-les amb Python i utilitzar receptes recuperades de Weaviate es descriu actualment a l’[exemple 10 del document d’observabilitat](./06_observalility.md).

**Document:** [07_hermes.md](./07_hermes.md)

### 8. Exemples

Recull exemples Python d’agents, LangGraph, Weaviate i una planificació setmanal amb Hermes.

**Document:** [08_examples.md](./08_examples.md)
