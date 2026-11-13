## 4. RAG (RETRIEVAL-AUGMENTED GENERATION)

RAG (Retrieval-Augmented Generation) és una tècnica que permet millorar les respostes d'un model de llenguatge incorporant informació recuperada d'una font externa, com ara una base de dades, documents o altres sistemes d'emmagatzematge.

Un LLM genera respostes a partir dels coneixements adquirits durant l'entrenament i del context que rep en cada consulta. D’aquesta manera, aquests coneixements poden no incloure informació específica d'una aplicació, documents o dades actualitzades. RAG permet solucionar aquesta limitació proporcionant al model informació rellevant abans de generar la resposta. D'aquesta manera, el LLM pot respondre basant-se en dades que no necessàriament formen part del seu entrenament.

### 4.1. FUNCIONAMENT D'UN SISTEMA RAG

El funcionament d'un sistema RAG es divideix en tres etapes principals: retrieval, augmentation i generation.

1. **Retrieval** (recuperació d'informació):
   Quan l'usuari introdueix una consulta, el sistema busca informació relacionada amb la petició en una font externa. En sistemes que utilitzen bases de dades vectorials, aquesta cerca pot realitzar-se mitjançant representacions numèriques del contingut (embeddings).

   Un embedding és un vector numèric que representa determinades característiques semàntiques d'un text. Això permet comparar el significat de diferents consultes i documents, encara que no utilitzin exactament les mateixes paraules. Per exemple, una consulta com «receptes per a un sopar ràpid» pot recuperar receptes descrites com a «plats fàcils de preparar en pocs minuts».

2. **Augmentation** (ampliació del context):
   Una vegada recuperada la informació, Python prepara un nou prompt que incorpora tant la pregunta original de l'usuari com les dades obtingudes. El model ja no rep únicament la pregunta, sinó també informació addicional que pot utilitzar per elaborar la resposta.

3. **Generation** (generació de la resposta):
   Finalment, el LLM processa el prompt ampliat i genera una resposta en llenguatge natural. En aquesta etapa, el model no necessita conèixer prèviament els documents recuperats. Pot utilitzar-los directament perquè formen part del context proporcionat.

El fet d'utilitzar RAG no garanteix automàticament que totes les respostes siguin correctes, però permet reduir la dependència dels coneixements interns del model i fonamentar les respostes en informació concreta.

**Flux general del sistema RAG**

```mermaid
flowchart LR
    U["Consulta de l'usuari"] --> R["Retrieval: cerca a Weaviate"]
    R --> C["Receptes recuperades"]
    C --> A["Augmentation: prompt amb context"]
    U --> A
    A --> G["Generation: inferència del LLM"]
    G --> F["Resposta basada en dades recuperades"]

    classDef usuari fill:#D6EAF8,stroke:#333333,color:#111111
    classDef retrieval fill:#D5E8E8,stroke:#333333,color:#111111
    classDef dades fill:#FCE5CD,stroke:#333333,color:#111111
    classDef augmentacio fill:#D9EAD3,stroke:#333333,color:#111111
    classDef llm fill:#FFF2CC,stroke:#333333,color:#111111
    classDef resposta fill:#E4DDF1,stroke:#333333,color:#111111

    class U usuari
    class R retrieval
    class C dades
    class A augmentacio
    class G llm
    class F resposta
```

<p align="center">
  <sub>Figura 1. Flux general d'un RAG</sub>
</p>

### 4.2. BASES DE DADES VECTORIALS: WEAVIATE CLOUD

En els exemples desenvolupats a continuació, s'utilitza Weaviate Cloud, una base de dades vectorial que permet emmagatzemar informació estructurada i recuperar registres mitjançant cerques semàntiques. A diferència d'una cerca tradicional basada únicament en la coincidència de paraules, una cerca vectorial permet identificar contingut relacionat amb el significat de la consulta. Per fer-ho, la informació emmagatzemada es representa mitjançant vectors i es comparen les representacions de la consulta i dels registres disponibles.

En aquests exemples (8.7, 8.8, 8.9, 8.10, 8.11) s'utilitza la col·lecció Recetas, que conté informació sobre diferents receptes.

Entre les propietats disponibles es troben:

| **Propietat**       | **Informació**                |
| ------------------- | ----------------------------- |
| `nombre`            | Nom de la recepta             |
| `categoria`         | Categoria del plat            |
| `dieta`             | Tipus de dieta                |
| `tiempoMin`         | Temps de preparació en minuts |
| `raciones`          | Nombre de racions             |
| `ingredientes`      | Ingredients i quantitats      |
| `ingredientesClave` | Ingredients principals        |
| `preparacion`       | Instruccions de preparació    |
| `descripcion`       | Descripció de la recepta      |

La cerca semàntica s'executa amb el mètode near_text() del client Python de Weaviate: result = collection.query.near_text(\*\*kwargs). Aquesta instrucció consulta els vectors de la col·lecció per recuperar receptes relacionades amb el text introduït.

Perquè funcioni, la col·lecció ha de disposar d'una configuració de vectorització o de vectors compatibles amb la consulta.

### 4.3. APLICACIONS I AVANTATGES DE RAG

RAG permet desenvolupar assistents que utilitzen informació específica sense necessitat d'entrenar un nou model. Aquesta arquitectura és especialment útil en aplicacions que requereixen consultar documentació tècnica, manuals, bases de dades internes, normatives o altres fonts d'informació. També permet actualitzar les dades disponibles modificant el contingut de la base de dades, sense haver de modificar els paràmetres del LLM.

La qualitat del sistema depèn tant de la capacitat del model per interpretar les dades com de la rellevància i la qualitat de la informació recuperada.

En el projecte de receptes, això significa que el LLM no inventa les receptes que s'han de mostrar, sinó que rep una selecció de resultats recuperats de Weaviate i genera una explicació a partir d'aquesta informació.
