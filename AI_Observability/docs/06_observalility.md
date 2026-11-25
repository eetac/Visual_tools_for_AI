## 6. OBSERVABILITAT (OPIK, OPENTELEMETRY I LANGSMITH)

L'observabilitat és la capacitat de monitoritzar, registrar i analitzar el funcionament intern d'una aplicació basada en models de llenguatge.

Quan es desenvolupa una aplicació que incorpora LangChain, LangGraph, Ollama, Weaviate o altres eines, no és suficient comprovar que el sistema genera una resposta correcta. També és important conèixer quines funcions s'han executat, quin recorregut ha seguit la petició, quant temps ha necessitat cada operació i quants recursos s'han consumit.

En aquestes pràctiques s'exploren tres alternatives: **Opik**, una plataforma d'observabilitat desenvolupada per Comet que integra el registre i la visualització de les execucions d'IA. **OpenTelemetry amb Grafana i Tempo**, que separa la instrumentació del programa, l'emmagatzematge de traces i el dashboard. I **LangSmith**, una plataforma d'observabilitat i avaluació amb integració nativa amb LangChain i LangGraph.

### 6.1. CONCEPTES PRINCIPALS

Els principals conceptes que s'utilitzen a Opik són:

| **Concepte**       | **Descripció**                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------- |
| **Trace**          | Registre de l'execució completa d'una petició.                                              |
| **Span**           | Operació individual dins d'una trace.                                                       |
| **Thread**         | Agrupació de traces relacionades amb una mateixa conversa o sessió.                         |
| **Latency**        | Temps necessari per executar una operació o completar una petició.                          |
| **Token usage**    | Nombre de tokens processats i generats pel LLM.                                             |
| **Error rate**     | Percentatge d'execucions que han registrat errors.                                          |
| **Estimated cost** | Estimació del cost associat a les crides als models, quan és calculable.                    |
| **Metadata**       | Informació addicional, com el model utilitzat, el proveïdor o els paràmetres de l'execució. |

Una trace representa el recorregut complet d'una petició. Per exemple, quan un usuari sol·licita una recepta, la trace pot incloure la interpretació del missatge, la consulta a Weaviate, la recuperació de receptes i la generació de la resposta. Dins de cada trace es registren diferents spans, que representen les operacions individuals del procés. Els spans poden contenir altres spans, formant una estructura jeràrquica que permet identificar les dependències i analitzar el temps consumit en cada etapa.

### 6.2. INSTAL·LACIÓ I CONFIGURACIÓ D'OPIK

Per incorporar observabilitat a una aplicació Python, primer cal instal·lar Opik i configurar la connexió amb la plataforma.

**1. Instal·lació:**

Les dependències de Python dels exemples d'observabilitat (Opik, OpenTelemetry i LangSmith) es centralitzen al fitxer [`requirements.txt`](../../requirements.txt) del repositori. S'instal·len una sola vegada en un entorn virtual compartit pels exemples, sempre que siguin compatibles entre si.

Primer cal obrir el terminal a l'arrel del repositori, és a dir, la carpeta que conté `AI_Observability/`. Si l'entorn virtual `.venv` ja existeix, només cal activar-lo. En cas contrari, cal crear-lo primer.

**macOS/Linux (Bash/Zsh):**

```bash
# Només si encara no existeix .venv
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
# Només si encara no existeix .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Amb l'entorn activat, les ordres següents són iguals en els tres sistemes:

```bash
python -m pip install -r requirements.txt
python -m pip check
```

Si no hi ha incompatibilitats entre les dependències instal·lades, la segona ordre retorna:

```text
No broken requirements found.
```

Si les dependències ja s'han instal·lat correctament en un exemple anterior, no cal tornar a executar la instal·lació. Les credencials i la configuració de cada plataforma, en canvi, es preparen per separat.

**2. Configuració del compte:**

Per utilitzar Opik Cloud, cal disposar d'un compte a la plataforma de Comet. Es pot accedir a través de: https://www.comet.com/opik

Una vegada creat el compte, cal identificar el workspace i disposar d'una API key. El workspace és l'espai de treball que agrupa els projectes disponibles. Un projecte organitza les traces i les mètriques d'una aplicació concreta.

Per configurar la connexió des del terminal:

```bash
opik configure
```

Aquesta ordre inicia un assistent de configuració. Cal seleccionar l'entorn corresponent i proporcionar les credencials necessàries, com l'API key i el workspace.

**3. Crear un nou projecte:**

Per separar les traces de diferents aplicacions és recomanable utilitzar un projecte d'Opik per a cadascuna. Per crear-ne un des de la interfície web, s'accedeix al workspace corresponent i a la secció de projectes. Des d'aquesta pàgina es pot crear un projecte nou, assignant-li un nom identificatiu.

Si el projecte encara no existeix, Opik pot crear-lo automàticament quan rep les primeres traces. Per tant, no és obligatori crear-lo manualment abans d'executar el programa.

Per utilitzar un projecte diferent, només cal modificar el valor de `project_name`.

És important que les traces s'enviïn al projecte correcte. En aquest exemple, el nom està especificat directament dins de `OpikTracer`, de manera que aquest valor té prioritat sobre una configuració general del nom del projecte.

### 6.3. ANÀLISI DE LES TRACES

Una vegada executades diferents peticions, les traces es poden consultar des de la interfície web d'Opik. La secció Observability → Logs permet visualitzar les execucions registrades i accedir al detall de cadascuna.

**Visualització general de traces:**
![Figura 1: captura original d’Opik](./img/opik_traces.png)

<p align="center"><sub>Figura 1. Registre de traces amb el nombre d’execucions, errors, durada mitjana i entrades i sortides de les peticions</sub></p>

A la captura es poden observar les traces generades durant les proves de l'assistent.

En el període seleccionat apareixen:

- Traces registrades: 25
- Errors: 1
- Error rate: 4%
- Durada mitjana: 8,6 s

A la taula inferior de la figura 1 es mostren les entrades (Input) i les sortides (Output) de diferents interaccions.

Per exemple, es poden observar peticions relacionades amb la cerca de receptes, l'addició d'ingredients i la modificació de la llista de la compra. Això permet comprovar que les interaccions de l'usuari estan quedant registrades correctament.

També és possible utilitzar els filtres de la interfície per localitzar traces amb errors, consultar una petició concreta o restringir els resultats a un període determinat.

**Dashboard:**

La secció Dashboards proporciona una visió agregada del funcionament de l'aplicació.

![Figura 2: captura original d’Opik](./img/opik_dashboard.png)

<p align="center"><sub>Figura 2. Dashboard (nombre de traces, els errors, els percentils de latència, el consum de tokens i l'evolució temporal de les execucions)</sub></p>

A diferència de Logs, que permet inspeccionar les execucions individualment, aquesta secció facilita l'anàlisi global del rendiment.

En la captura es poden observar les mètriques següents:

- Total trace count: 25
- Total error count: 1
- P50 duration: 5,6 s
- P90 duration: 20,9 s
- P99 duration: 22,9 s
- Cost: no l’especifica (en aquest exemple, les mètriques de cost no proporcionen una estimació útil per al model local. Tot i que executar Qwen amb Ollama no implica un preu per consulta a un proveïdor de LLM, sí que consumeix recursos de l'ordinador, com CPU, GPU, memòria i electricitat)

Els percentils permeten analitzar la distribució dels temps d'execució. El percentil P50 correspon a la mediana, aproximadament la meitat de les execucions tenen una durada igual o inferior a 5,6 segons. El percentil P90 indica que aproximadament el 90% de les execucions tenen una durada igual o inferior a 20,9 segons. Finalment, P99 permet estudiar les execucions més lentes, amb un valor de 22,9 segons en aquesta captura.

Aquests indicadors són útils perquè la durada mitjana no sempre representa adequadament les peticions que necessiten més temps.

**Consum de tokens:**

El dashboard també incorpora una gràfica denominada Token usage - total_tokens. Aquesta gràfica mostra l'evolució dels tokens registrats durant les execucions. El consum pot variar segons la complexitat de la petició, la quantitat de context proporcionat al model i el nombre d'inferències necessàries.

Per exemple, una petició que únicament afegeix un producte pot requerir una sola inferència. En canvi, una consulta RAG pot requerir una primera inferència per interpretar la petició i una segona per generar la resposta utilitzant les receptes recuperades. Això permet comparar el consum de recursos entre diferents tipus d'operacions.

**Volum i durada de les traces:**
![Figura 3: captura original d’Opik](./img/opik_trace_charts.png)

<p align="center"><sub>Figura 3. Trace volume i trace duration al dashboard</sub></p>

Es poden veure dues gràfiques:

- Trace volume: representa el nombre d'execucions registrades al llarg del temps.
- Trace duration: representa l'evolució de la durada de les execucions.

Aquestes gràfiques permeten identificar períodes amb més activitat i detectar possibles increments dels temps de resposta.

### 6.4. ANÀLISI DETALLADA D’UNA TRACE

Es pot observar també el recorregut complet d’una petició.
![Figura 4: captura original d’Opik](./img/opik_trace_detail.png)

<p align="center"><sub>Figura 4. Detall d’una execució de LangGraph mostrant els spans</sub></p>

L'usuari introdueix: “quiero hacer la 1, asi q añademe los ingredientes a la lista”

La trace mostra una durada aproximada de 2,4 segons.

A la part esquerra apareixen els spans que s'han executat, organitzats jeràrquicament:

1. LangGraph: representa l'execució general del graf.
2. `process_input`: és el primer node de LangGraph, encarregat d'interpretar la petició de l'usuari.
3. `ollama_tokens` i `ChatOllama`: corresponen a la inferència amb Qwen i al registre de les metadades associades. En aquesta etapa, el LLM interpreta que l'usuari vol afegir els ingredients d'una recepta seleccionada anteriorment.
4. `add_recipe`: és el node seleccionat per LangGraph després de processar el resultat del model. Aquest node recupera la recepta corresponent de `last_recipes`, que conté les receptes mostrades en la cerca anterior.
5. `add_products`: és la funció Python que afegeix els ingredients de la recepta a la llista de la compra. La captura mostra una durada aproximada de 0,001 segons per a aquesta operació.

La resposta final confirma que s'han afegit els ingredients de la recepta seleccionada.

Aquest exemple permet observar que la major part del temps de la petició està relacionada amb la inferència del LLM, mentre que l'operació Python d’afegir productes necessita molt menys temps. També permet comprovar que no es realitza una nova consulta a Weaviate. El programa reutilitza les receptes emmagatzemades a l'estat de LangGraph i executa directament `add_products()`.

A la part inferior esquerra apareix una representació del graf complet de LangGraph amb els possibles nodes i connexions. Aquest graf representa les rutes disponibles a l'aplicació, no necessàriament totes les operacions executades en aquella petició concreta. A la part dreta es mostren les dades d'entrada i sortida, les etiquetes i les metadades associades a la trace.

Aquest nivell de detall és especialment útil per comprovar que les decisions del LLM es tradueixen correctament en operacions Python.

### 6.5. INTERPRETACIÓ DELS RESULTATS

Les captures anteriors permeten comprovar que la integració d'Opik amb LangGraph, Ollama i Weaviate funciona correctament i que les execucions queden registrades.

A través de la interfície es poden diferenciar tres nivells d'anàlisi:

- Logs: permet consultar les interaccions registrades i identificar les que han produït errors.
- Dashboard: permet estudiar el rendiment global de l'aplicació mitjançant mètriques de durada, volum d'execucions i consum de tokens.
- Detall de les traces: permet inspeccionar el recorregut concret d'una petició i identificar les operacions realitzades per LangGraph, les inferències del LLM i les funcions executades per Python.

D'aquesta manera, Opik facilita la detecció d'errors, l'anàlisi del rendiment i la comprensió del comportament intern dels sistemes basats en intel·ligència artificial.

La seva incorporació no modifica les funcionalitats de l'assistent, però permet estudiar com es generen les respostes i identificar possibles oportunitats de millora.

### 6.6. OPENTELEMETRY

OpenTelemetry (OTel) és un conjunt d'API, SDK i convencions obertes per instrumentar aplicacions i exportar dades d'observabilitat. Permet descriure operacions amb **traces** i **spans**, afegir atributs i transmetre'ls a altres sistemes. No proporciona, per si sol, un dashboard on consultar aquestes dades.

En l'exemple de receptes utilitzem aquesta arquitectura:

```mermaid
flowchart TD
    U["Usuari: receptes i llista de compra"]
    A["Python: LangGraph + Ollama + Weaviate"]
    C["OTLP/HTTP: port 4318"]
    T["Collector i Tempo"]
    G["Grafana: Explore i dashboard"]

    U --> A
    A -. "SDK OpenTelemetry: traces i spans" .-> C
    C --> T
    T --> G

    class U entrada
    class A python
    class C servei
    class T agent
    class G llm

    classDef entrada fill:#D6EAF8,stroke:#333333,color:#111111
    classDef python fill:#D9EAD3,stroke:#333333,color:#111111
    classDef servei fill:#EADCF8,stroke:#333333,color:#111111
    classDef agent fill:#FCE5CD,stroke:#333333,color:#111111
    classDef llm fill:#FFF2CC,stroke:#333333,color:#111111
```

| Component                      | Paper en el sistema                                                                                   |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- |
| **SDK OpenTelemetry (Python)** | Crea spans, els relaciona amb una trace i els afegeix atributs.                                       |
| **OTLP/HTTP**                  | Transporta les traces del programa al receptor HTTP, en aquest cas `http://localhost:4318/v1/traces`. |
| **OpenTelemetry Collector**    | Rep i encamina les dades d'observabilitat.                                                            |
| **Grafana Tempo**              | Emmagatzema les traces i permet cercar-les amb **TraceQL**.                                           |
| **Grafana**                    | Mostra les traces, els grafs dels spans i els panells del dashboard.                                  |

El programa **continua accedint a les receptes de Weaviate** i utilitza la col·lecció `Recetas`. OTel no substitueix Weaviate: només observa què fa l'aplicació. Tampoc decideix les rutes de LangGraph, les decisions continuen depenent del router i del LLM.

**Diferència entre els senyals d'observabilitat:**

- **Traces:** permeten reconstruir el recorregut d'una petició i la relació entre operacions.
- **Mètriques:** mostren valors numèrics agregats al llarg del temps, com el nombre de peticions o el consum de tokens.
- **Logs:** recullen esdeveniments textuals.

En aquest exercici, les dades que el codi exporta són **traces**. Els gràfics i els indicadors de tokens s'obtenen a Grafana mitjançant consultes de mètriques sobre traces amb TraceQL. És diferent de configurar un exportador OTel Metrics propi o de recollir mètriques a Prometheus.

### 6.7. TRACES, SPANS, RELACIONS I ATRIBUTS DEL RAG

Cada missatge de l'usuari crea una trace principal que comença a l'span `langgraph.invoke`. A partir d'aquí, s'instrumenten els nodes i eines que intervenen en la resposta:

| Span o atribut                                   | Què representa?                                               |
| ------------------------------------------------ | ------------------------------------------------------------- |
| `langgraph.invoke`                               | Execució completa d'una consulta de l'usuari.                 |
| `langgraph.node.process_input`                   | Node que interpreta la petició i decideix l'acció.            |
| `langgraph.node.search_recipe`                   | Node que inicia la recuperació de receptes.                   |
| `langgraph.node.add_recipe`                      | Node que afegeix ingredients d'una recepta ja mostrada.       |
| `tool.search_recipes`, `tool.add_products`, etc. | Eines Python executades dins dels nodes.                      |
| `weaviate_near_text`                             | Cerca semàntica a Weaviate.                                   |
| `ollama.clasificacion`                           | Inferència de Qwen per classificar la intenció.               |
| `ollama.generacion_rag`                          | Inferència per elaborar la resposta amb el context recuperat. |
| `langgraph.route`                                | Atribut que registra la decisió del router.                   |

Els spans es relacionen mitjançant un **Trace ID**, un **Span ID** i la relació pare-fill. En el programa s'utilitza la propagació de `traceparent` per conservar el context entre els nodes de LangGraph. Això és important perquè, si es fan operacions sense mantenir el context, el seu registre es podria fragmentar en traces independents i seria més difícil reconstruir l'execució.

El registre d'atributs també permet explicar per què una petició és més lenta que una altra. Per exemple, consultar receptes acostuma a requerir una crida de classificació, una consulta vectorial i una segona inferència de generació RAG. En canvi, afegir un producte a la llista és una acció Python més curta i no necessita consultar Weaviate.

**Atributs de consum de tokens:**

| Atribut del span d'Ollama    | Informació                                                             |
| ---------------------------- | ---------------------------------------------------------------------- |
| `gen_ai.usage.input_tokens`  | Tokens d'entrada del model.                                            |
| `gen_ai.usage.output_tokens` | Tokens generats pel model.                                             |
| `gen_ai.usage.total_tokens`  | Total de tokens, quan les metadades el proporcionen o es pot calcular. |
| `rag.tokens.total`           | Atribut propi utilitzat a les consultes del dashboard.                 |
| `gen_ai.request.model`       | Nom del model, com per exemple `qwen3.5:9b`.                           |
| `llm.etapa`                  | Fase de la inferència: `clasificacion` o `generacion_rag`.             |

### 6.8. INSTAL·LACIÓ LOCAL I CONNEXIÓ AMB GRAFANA

A diferència d'Opik Cloud, en aquesta pràctica la infraestructura d'observabilitat s'executa **localment** amb Docker. La imatge `grafana/otel-lgtm` inclou una instal·lació de prova amb Grafana, Tempo i el receptor OpenTelemetry. Les traces de l'aplicació Python s'envien per OTLP/HTTP al port 4318 i es consulten des del navegador al port 3000.

Els passos següents serveixen per a **macOS, Linux i Windows**. Quan els comandaments són diferents, s'indiquen **dins del mateix pas**, separant **macOS/Linux (Bash/Zsh)** i **Windows (PowerShell)**. Totes les ordres s'executen des de l'**arrel del repositori**, és a dir, la carpeta que conté `AI_Observability/`.

**1. Comprovar els requisits previs**

Abans de començar, cal tenir:

- Docker Desktop instal·lat i obert.
- Python i les biblioteques de LangChain, LangGraph, Weaviate i OpenTelemetry.
- Ollama en execució amb el model configurat.
- Una instància de Weaviate Cloud amb la col·lecció **`Recetas` ja creada i amb dades**, com a l'exemple 8.9.
- Les variables `WEAVIATE_URL` i `WEAVIATE_API_KEY` al fitxer `.env` del projecte.

Els comandaments següents són per a **macOS i Linux** amb bash/zsh i s'executen des de l'arrel del repositori, la carpeta que conté `AI_Observability/`.

Per comprovar la ubicació del terminal abans de començar:

**2. Crear el contenidor Docker la primera vegada**

Primer, es comprova que Docker està disponible. **Aquestes ordres són iguals als tres sistemes operatius:**

```bash
docker info
docker ps -a
```

`docker ps -a` mostra **tots** els contenidors, fins i tot els aturats. Si la llista ja conté un contenidor amb el nom **`grafana-lgtm`**, no cal tornar-lo a crear. Si ja el tenim creat, s'inicia amb `docker start grafana-lgtm`. Si ja està com a `Up`, no cal fer res.

**Només si el contenidor encara no existeix**, es descarrega la imatge. Aquesta ordre és comuna a tots els sistemes:

```bash
docker pull grafana/otel-lgtm:latest
```

**macOS/Linux (Bash/Zsh):**

```bash
docker run -d \
  --name grafana-lgtm \
  -p 3000:3000 \
  -p 4318:4318 \
  -v grafana-lgtm-data:/data \
  grafana/otel-lgtm:latest
```

**Windows (PowerShell):**

```powershell
docker run -d --name grafana-lgtm -p 3000:3000 -p 4318:4318 -v grafana-lgtm-data:/data grafana/otel-lgtm:latest
```

La configuració del contenidor és la mateixa en ambdós casos.

| Paràmetre                    | Funció                                                                        |
| ---------------------------- | ----------------------------------------------------------------------------- |
| `-d`                         | Executa el contenidor en segon pla.                                           |
| `--name grafana-lgtm`        | Dona un nom fix al contenidor, en lloc d'un d'aleatori.                       |
| `-p 3000:3000`               | Permet obrir la interfície web de Grafana a `http://localhost:3000`.          |
| `-p 4318:4318`               | Publica el receptor OTLP/HTTP, al qual Python envia les traces.               |
| `-v grafana-lgtm-data:/data` | Crea un volum per conservar dades entre recreacions en una instal·lació nova. |

Per comprovar si ha arrencat, en qualsevol dels tres sistemes:

```bash
docker ps
```

Després s'obre **[Grafana](http://localhost:3000)**. En una instal·lació de prova nova, l'usuari i la contrasenya inicials solen ser `admin` / `admin`. Grafana pot demanar canviar la contrasenya.

**3. Com aturar-lo i tornar-lo a arrencar un altre dia**

Aquestes ordres s'utilitzen després d'haver creat el contenidor i són **iguals** a macOS, Linux i Windows (PowerShell):

| Acció                                              | Comandament                          |
| -------------------------------------------------- | ------------------------------------ |
| Aturar Grafana quan acabem                         | `docker stop grafana-lgtm`           |
| Tornar-lo a iniciar després d'obrir Docker Desktop | `docker start grafana-lgtm`          |
| Reiniciar-lo                                       | `docker restart grafana-lgtm`        |
| Comprovar si està iniciat                          | `docker ps`                          |
| Veure'l encara que estigui aturat                  | `docker ps -a`                       |
| Consultar registres                                | `docker logs --tail 50 grafana-lgtm` |

La diferència és important: **`docker run` crea** un contenidor, **`docker start` inicia** un contenidor existent, **`docker stop` l'atura sense esborrar-lo**. No s'ha de fer servir `docker rm` per tancar, ja que esborraria el contenidor.

**4. Instal·lar les dependències del programa Python**

Si encara no s'ha creat un entorn virtual a l'arrel del projecte, cal seguir l'opció del sistema operatiu corresponent.

**macOS/Linux (Bash/Zsh):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si Windows no reconeix `python`, però té instal·lat el llançador de Python, es pot utilitzar `py -3 -m venv .venv`.

Amb l'entorn activat, les ordres per instal·lar les dependències són **iguals** en els tres sistemes:

```bash
python -m pip install -r requirements.txt
```

o bé

```bash
python -m pip install langchain langgraph langchain-ollama weaviate-client python-dotenv
python -m pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

Es comprova que Ollama té disponible el model. Les ordres d'Ollama també són iguals a macOS, Linux i Windows:

```bash
ollama list
```

Si el model encara no s'ha descarregat i l'ordinador té prou espai i memòria:

```bash
ollama pull qwen3.5:9b
```

**5. Configurar Weaviate i l'exportador de traces**

El programa continua utilitzant la mateixa base de dades de receptes. Al fitxer `.env` de l'arrel del repositori cal posar les credencials del teu clúster. Per obrir-lo des del terminal:

- **macOS/Linux (Bash/Zsh):** `nano .env` (o qualsevol editor de text).
- **Windows (PowerShell):** `notepad .env`. Cal desar-lo com a **`.env`**, no `.env.txt`.

Si el fitxer ja existeix, cal actualitzar o afegir aquestes claus **sense esborrar les altres configuracions**:

```dotenv
WEAVIATE_URL=https://EL_TEU_CLUSTER.weaviate.network
WEAVIATE_API_KEY=LA_TEVA_CLAU_REAL
OLLAMA_MODEL=qwen3.5:9b
```

Els dos primers valors s'han de substituir pels reals i **no s'ha de publicar `.env` al repositori**. No és necessari crear cap col·lecció a Grafana ni a OpenTelemetry: `Recetas` només pertany a Weaviate.

A continuació, **en el mateix terminal on s'executarà Python**, s'indica el nom del servei i el receptor de les traces.

**macOS/Linux (Bash/Zsh):**

```bash
export OTEL_CONSOLE_ONLY=0
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:4318/v1/traces
export OTEL_SERVICE_NAME=shopping-rag-weaviate-otel
```

**Windows (PowerShell):**

```powershell
$env:OTEL_CONSOLE_ONLY = "0"
$env:OTEL_EXPORTER_OTLP_TRACES_ENDPOINT = "http://localhost:4318/v1/traces"
$env:OTEL_SERVICE_NAME = "shopping-rag-weaviate-otel"
```

Aquestes variables només s'apliquen a **la sessió actual del terminal**. Si es tanca la finestra i s'obre una altra, cal definir-les de nou abans d'executar l'exemple.

El valor `OTEL_CONSOLE_ONLY=0` fa que l'SDK exporti els spans a Grafana, en comptes d'imprimir-ne la representació completa per terminal.

**6. Executar el cas pràctic**

Primer s'ha de comprovar que Weaviate està ben configurat i després iniciar l'assistent. Els dos comandaments següents es poden executar en ordre.

**macOS/Linux (Bash/Zsh):**

```bash
python AI_Observability/code/src/11_shopping_list_weaviate_otel.py --check
python AI_Observability/code/src/11_shopping_list_weaviate_otel.py
```

**Windows (PowerShell):**

```powershell
python .\AI_Observability\code\src\11_shopping_list_weaviate_otel.py --check
python .\AI_Observability\code\src\11_shopping_list_weaviate_otel.py
```

**Atenció:** només s'ha d'executar la segona ordre quan la comprovació `--check` indiqui que la col·lecció **`Recetas`** és accessible. Si a Windows no s'ha pogut activar l'entorn, es pot utilitzar `.\.venv\Scripts\python.exe` en lloc de `python` en totes dues ordres.

Per generar traces de diferents rutes, es poden introduir aquestes peticions:

1. «Recomiéndame recetas con huevos y patatas en menos de 30 minutos».
2. «Añade los ingredientes de la segunda receta».
3. «Muéstrame la lista».
4. `exit` per acabar.

Cada missatge genera un span principal `langgraph.invoke`.

**7. Comprovar les traces a Grafana abans de fer el dashboard**

1. Obrir `http://localhost:3000` i entrar a **Explore**.
2. Seleccionar **Tempo** com a font de dades.
3. Seleccionar **TraceQL** i escriure:

   ```traceql
   { resource.service.name = "shopping-rag-weaviate-otel" }
   ```

4. Escollir un interval que inclogui les peticions acabades de fer (`Last 1 hour`, `Last 6 hours` o un rang absolut).
5. Prémer **Run query / Refresh**.

Si apareixen traces amb el nom `langgraph.invoke`, la connexió és correcta. Des d'aquesta mateixa pantalla es poden obrir les traces i revisar-ne els spans. **Només quan aquest pas funciona té sentit crear els panels del dashboard.** Aquests passos d'interfície són **els mateixos a macOS, Linux i Windows**.

### 6.9. CREACIÓ I CONFIGURACIÓ DEL DASHBOARD DE GRAFANA

Quan les traces ja arriben a Tempo, es pot construir un **dashboard** que combini el rendiment general de l'aplicació amb l'anàlisi individual de les traces. En aquest cas s'ha creat el dashboard `RAG recetas`.

Per començar:

1. Entrar a **Dashboards → New → New dashboard**.
2. Assignar-li el nom **RAG recetas**.
3. Seleccionar **+ Add panel**, que obre l'editor del primer panell.
4. Configurar **Data source: Tempo** i **Query type: TraceQL**.
5. Escollir la visualització de cada panell a **All visualizations** i desar els canvis amb **Save**.

Els noms de menús poden variar lleugerament segons la versió de Grafana. A les captures de la pràctica s'utilitza Grafana 13.3.

#### 6.9.1. Gràfics de rendiment

**A. Nombre d'execucions — RAG Executions**

- **Visualització:** `Time series`.
- **Títol:** `RAG Executions`.
- **Consulta TraceQL:**

```traceql
{ resource.service.name = "shopping-rag-weaviate-otel" && span:name = "langgraph.invoke" } | count_over_time()
```

Aquesta consulta compta les execucions de `langgraph.invoke` per interval temporal. En aquest codi, cada petició de l'usuari genera un d'aquests spans. El resultat mostra el **nombre d'execucions per interval**, no la taxa per segon que retornaria `rate()`.

**B. Durada de les execucions — Execution Duration**

- **Visualització:** `Time series`.
- **Títol:** `Execution Duration`.
- **Consulta TraceQL:**

```traceql
{ resource.service.name = "shopping-rag-weaviate-otel" && span:name = "langgraph.invoke" } | avg_over_time()
```

Mostra la durada mitjana de les peticions executades per LangGraph. A les opcions del panell, es pot configurar la unitat de l'eix vertical com a **segons (`s`)**.

**C. Temps consumit per Ollama — Ollama Duration**

- **Visualització:** `Time series`.
- **Títol:** `Ollama Duration`.
- **Consulta TraceQL:**

```traceql
{ resource.service.name = "shopping-rag-weaviate-otel" && span:name =~ "ollama.*" } | avg_over_time() by (span.llm.etapa)
```

El programa diferencia dues etapes: `clasificacion`, que interpreta la petició de l'usuari, i `generacion_rag`, que redacta la resposta amb les receptes trobades. La consulta permet observar la durada de cada etapa per separat. Una petició que només modifica la llista de la compra pot no tenir cap span de `generacion_rag`.

**D. Cerca semàntica — Weaviate Search Duration (near_text())**

- **Visualització:** `Time series`.
- **Títol:** `Weaviate Search Duration (near_text())`.
- **Consulta TraceQL:**

```traceql
{ resource.service.name = "shopping-rag-weaviate-otel" && span:name = "weaviate_near_text" } | avg_over_time()
```

Aquesta consulta mostra quant dura la cerca vectorial amb `near_text()` a la col·lecció `Recetas`. Si l'usuari únicament consulta o modifica una llista existent, pot no aparèixer cap punt nou: això és **normal** perquè no s'ha fet una cerca a Weaviate.

![Dashboard Grafana amb els quatre gràfics de rendiment](./img/grafana_dashboard.png)

<p align="center"><sub>Figura 5. Dashboard RAG recetas: nombre d'execucions, durada total, durada d'Ollama i durada de les cerques a Weaviate.</sub></p>

En comparar aquests gràfics, es pot observar quina part de la petició consumeix més temps. En una cerca RAG, habitualment la inferència del model és més costosa que les operacions Python de gestió de la llista.

#### 6.9.2. Taula de traces

Els gràfics anteriors ofereixen una vista agregada. Per inspeccionar una petició concreta, s'afegeix una taula amb les traces registrades.

1. Des de l'edició del dashboard, seleccionar **+ Add panel**.
2. Escollir **Data source: Tempo** i **Query type: TraceQL**.
3. Escriure aquesta consulta:

   ```traceql
   { resource.service.name = "shopping-rag-weaviate-otel" && span:name = "langgraph.invoke" }
   ```

4. A **All visualizations**, seleccionar **Table**.
5. Posar el títol `Traces` i desar el panell.

La taula conté camps com **Trace ID**, **Start time**, **Service**, **Name** i **Duration**. També pot incloure el camp tècnic `nested`, que es pot ocultar si no és necessari. El camp intern `traceID`, en canvi, es necessita per construir l'enllaç al graf.

![Taula de traces del dashboard Grafana](./img/grafana_traces&nodes.png)

<p align="center"><sub>Figura 6. Taula de traces i graf de l'execució seleccionada en el dashboard.</sub></p>

Aquesta informació permet identificar consultes lentes, comparar execucions i seleccionar una trace per analitzar què ha fet LangGraph.

#### 6.9.3. Variable per seleccionar una trace

L'objectiu és que **el graf no estigui associat a un Trace ID fix**. Ha de mostrar la petició que es tria des de la taula.

Per crear el selector:

1. Tornar al dashboard i entrar a **Edit**.
2. Prémer **+ → Variable** a la barra lateral dreta.
3. Seleccionar **Textbox**, que permet introduir un identificador de trace.
4. Configurar la variable:

   | Camp              | Valor                                                        |
   | ----------------- | ------------------------------------------------------------ |
   | **Name**          | `TraceId`                                                    |
   | **Label**         | `Selected Trace`                                             |
   | **Default value** | Un Trace ID real de Tempo, com els que apareixen a la taula. |

5. Guardar la variable i el dashboard.

A la part superior apareixerà el camp **Selected Trace**.

#### 6.9.4. Graf de nodes d'una trace concreta

Per mostrar el recorregut de la trace seleccionada:

1. Afegir un panell nou.
2. Escollir **Tempo** com a font de dades.
3. Seleccionar **Query type: TraceQL** (no `Service Graph`).
4. Introduir la variable a la consulta:

   ```text
   ${TraceId}
   ```

5. Seleccionar **Node Graph** a **All visualizations**.
6. Escriure el títol `LangGraph - Nodes`.
7. Provar la visualització amb un Trace ID que existeixi abans de desar el panell.

La consulta és una **plantilla de Grafana**: perquè funcioni, Grafana ha de substituir `${TraceId}` pel valor escollit abans d'enviar la petició a Tempo. El valor final ha de ser un identificador hexadecimal real, no el text literal de la variable.

Per canviar de graf directament des de la taula:

1. Editar el panell `Traces`.
2. Obrir la configuració del camp **Trace ID → Data links → Add link**.
3. Escriure el títol **View execution graph**.
4. Introduir l'URL del mateix dashboard, passant-hi l'identificador de la fila:

   ```text
   /d/adkxzjf/rag-recetas?var-TraceId=${__data.fields["traceID"]}
   ```

5. **Substituir el camí `/d/adkxzjf/rag-recetas` pel del propi dashboard** si el seu UID o slug és diferent. Es pot copiar de la barra d'adreces del navegador.
6. Desar els canvis. En clicar un ID de la taula, seleccionar **View execution graph** i comprovar que `Selected Trace` canvia.

El camp visible `Trace ID` pot tenir el nom intern **`traceID`**. Si l'enllaç no canvia la variable, cal revisar el nom del camp a **Inspect → Data**.

**Què representa el Node Graph?** Cada cercle correspon a un span executat i les fletxes indiquen dependències pare-fill. No és el diagrama estàtic de tots els camins disponibles a LangGraph, sinó el recorregut de **la petició concreta**. Per exemple, una consulta RAG pot mostrar `process_input` → `search_recipe` → `search_recipes` → `weaviate_near_text`, mentre que afegir ingredients d'una recepta ja mostrada pot seguir una ruta diferent.

#### 6.9.5. Personalitzar el graf perquè es vegin només els noms

La visualització inicial pot mostrar durades i percentatges a l'interior dels cercles, que dificulten la lectura. En aquesta pràctica s'ha simplificat perquè quedin visibles els noms de les operacions.

1. Editar el panell **LangGraph - Nodes**.
2. Obrir **Transformations → Add transformation**.
3. Escollir **Filter fields by name**.
4. Al camp **Identifier / Regular expression pattern**, escriure:

   ```regex
   ^(id|subtitle|source|target)$
   ```

5. Comprovar que es mantenen els camps `id`, `subtitle`, `source` i `target` i guardar els canvis.

![Node Graph simplificat amb els noms dels spans](./img/grafana_nodes_LangGraph.png)

<p align="center"><sub>Figura 7. Node Graph simplificat: només es mostren els noms de les operacions, sota els cercles, sense durades ni percentatges interns.</sub></p>

#### 6.9.6. Consum de tokens: Input, Output i Total

El programa afegeix atributs numèrics als spans d'Ollama. Aquests atributs permeten construir tres indicadors que mostren els tokens consumits en el període de temps seleccionat.

Per a cada indicador:

1. Seleccionar **+ Add panel**.
2. Escollir **Tempo → TraceQL**.
3. Seleccionar la visualització **Stat**.
4. Configurar **Calculation = Total**, **Decimals = 0** i el títol corresponent.
5. Introduir la consulta i desar.

**Input Tokens:** suma els tokens que el model rep com a entrada.

```traceql
{ resource.service.name = "shopping-rag-weaviate-otel" && span:name =~ "ollama.*" } | sum_over_time(span.gen_ai.usage.input_tokens)
```

**Output Tokens:** suma els tokens que el model genera.

```traceql
{ resource.service.name = "shopping-rag-weaviate-otel" && span:name =~ "ollama.*" } | sum_over_time(span.gen_ai.usage.output_tokens)
```

**Total Tokens:** suma el consum total registrat en el camp propi `rag.tokens.total`.

```traceql
{ resource.service.name = "shopping-rag-weaviate-otel" && span:name =~ "ollama.*" } | sum_over_time(span.rag.tokens.total)
```

![Grafana: consum de tokens d'entrada, sortida i totals](./img/grafana_tokens_usage.png)

<p align="center"><sub>Figura 8. Input Tokens, Output Tokens i Total Tokens.</sub></p>

En aquest cas, es compleix `861 + 42 = 903`. Aquestes xifres són només un exemple: variaran amb el model, el text de les consultes i les respostes generades.

**Important:** els tres indicadors sumen els tokens de totes les inferències dins del rang temporal del dashboard.

#### 6.9.7. Interpretació final del dashboard

Les quatre zones permeten estudiar el comportament de l'assistent des de diferents perspectives:

- Els **gràfics de rendiment** indiquen quan s'han executat peticions i quines parts són més lentes.
- La **taula de traces** identifica cada consulta amb el seu ID, hora d'inici i durada.
- El **Node Graph** mostra els nodes, eines i inferències que s'han executat en una petició concreta.
- Els **panells de tokens** resumeixen el consum del model durant el període triat.

Per comprovar les rutes, es pot comparar una petició per **cercar receptes**, una per **afegir ingredients de la recepta seleccionada** i una tercera per **mostrar la llista de la compra**. Les traces haurien de mostrar seqüències diferents, perquè el router de LangGraph escull accions diferents.

OpenTelemetry registra el comportament de l'aplicació. És a dir, no modifica el resultat de les operacions Python ni les decisions del model. Això fa possible comprendre el flux del RAG i detectar oportunitats d'optimització sense alterar-ne la lògica.

### 6.10. REFERÈNCIES I EXEMPLE D'OPENTELEMETRY

**Relació amb els exemples:** l'explicació detallada del codi i del flux es troba a l'[exemple 8.12](./08_examples.md#812-observabilitat-del-rag-amb-opentelemetry-i-grafana--11_shopping_list_weaviate_otelpy), i el [programa complet](../code/src/11_shopping_list_weaviate_otel.py).

**Referències tècniques:**

- [Grafana Labs: Docker OpenTelemetry LGTM](https://grafana.com/docs/opentelemetry/docker-lgtm/)
- [Grafana: visualització de traces en dashboards](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/traces/)
- [Grafana Tempo: funcions de TraceQL metrics](https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-queries/functions/)
- [Grafana: Data links i variables](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/configure-data-links/)
- [OpenTelemetry: traces i spans](https://opentelemetry.io/docs/concepts/signals/traces/)

### 6.11. LANGSMITH: CONCEPTES, INSTAL·LACIÓ I CONFIGURACIÓ

LangSmith és una plataforma d'observabilitat i avaluació d'aplicacions d'IA desenvolupada per LangChain. Permet registrar les execucions d'un agent, inspeccionar les crides al model, les eines i els nodes, i analitzar les mètriques de rendiment des d'una interfície web.

En aquest exercici s'utilitza LangSmith Cloud com a tercera alternativa a Opik i OpenTelemetry amb Grafana. El programa continua executant-se localment amb Python, LangGraph i Ollama, i conserva la col·lecció `Recetas` de Weaviate Cloud. **No cal Docker ni desplegar l'agent a LangSmith**: només s'envien les dades d'observabilitat.

```mermaid
flowchart TD
    U["Usuari: receptes i llista de compra"] --> P["Python + LangGraph"]
    P --> O["Ollama: Qwen"]
    P --> W["Weaviate: Recetas"]
    P --> F["Resposta final"]
    P -. "Runs, traces i metadades" .-> S["SDK LangSmith"]
    S --> C["LangSmith Cloud: API HTTPS"]
    C --> D["Tracing i Monitoring"]
    class U,F entrada
    class P python
    class O llm
    class W,C servei
    class S,D opik
    classDef entrada fill:#D6EAF8,stroke:#333333,color:#111111
    classDef llm fill:#FFF2CC,stroke:#333333,color:#111111
    classDef python fill:#D9EAD3,stroke:#333333,color:#111111
    classDef decisio fill:#F4CCCC,stroke:#333333,color:#111111
    classDef servei fill:#EADCF8,stroke:#333333,color:#111111
    classDef agent fill:#FCE5CD,stroke:#333333,color:#111111
    classDef opik fill:#F5F5F5,stroke:#333333,color:#111111
```

| Concepte            | Descripció                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| **Trace**           | Registre d'una petició completa. En aquest programa, el run arrel és `langgraph.invoke`.       |
| **Run**             | Operació individual, equivalent conceptualment a un span. Pot tenir runs fills.                |
| **Run type**        | Tipus d'operació: `chain`, `llm`, `tool`, entre altres.                                        |
| **Thread**          | Agrupació de peticions relacionades mitjançant un identificador de conversa.                   |
| **Tracing project** | Destinació de les traces identificada per `LANGSMITH_PROJECT`.                                 |
| **Metadata**        | Informació addicional, com la col·lecció, l'etapa del LLM o el nombre de receptes recuperades. |
| **Feedback**        | Valoració d'una execució. És diferent del registre automàtic de latència o errors.             |

La integració amb LangChain i LangGraph permet registrar automàticament el graf, els nodes, el router, les eines `@tool` i les crides a `ChatOllama`. En canvi, la crida directa al client de Weaviate s'instrumenta explícitament amb `ls.trace()` per separar la durada de la cerca vectorial de la resta de l'eina. No s'afegeix cap inferència del LLM per registrar les traces.

#### 6.11.1. Instal·lació i configuració

Els comandaments es llancen **des de l'arrel del repositori `Visual_tools_for_AI`**, la carpeta que conté `AI_Observability/`. En cada pas es mostren les variants de macOS/Linux i Windows quan són diferents. El programa complet és [`12_shopping_list_weaviate_langsmith.py`](../code/src/12_shopping_list_weaviate_langsmith.py).

**1. Crear un compte gratuït i obtenir l'API key:**

Accedeix a [LangSmith](https://smith.langchain.com/) o a la [regió europea](https://eu.smith.langchain.com/) i crea un compte personal amb el pla **Developer**. Segons les [tarifes oficials](https://www.langchain.com/pricing), inclou un usuari i fins a 5.000 traces bàsiques mensuals, amb retenció base de 14 dies. Els límits i les tarifes poden canviar. No cal activar Plus, Engine, Agent Server ni avaluadors automàtics. No afegeixis un mètode de pagament si només vols fer la pràctica gratuïta.

A la interfície, entra a **Settings → API Keys** i crea una clau de tracing (o una clau personal autoritzada per enviar traces). Copia-la al fitxer `.env` local. No la publiquis ni la mostris a les captures.

**2. Preparar l'entorn virtual i instal·lar les dependències:**

Si l'entorn `.venv` ja existeix, només cal activar-lo. Si no existeix, crea'l primer.

**macOS/Linux (Bash/Zsh):**

```bash
# Només si encara no existeix .venv
python3 -m venv .venv
# Activació
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
# Només si encara no existeix .venv
python -m venv .venv
# Activació
.\.venv\Scripts\Activate.ps1
```

Amb l'entorn activat, s'utilitza el mateix fitxer `requirements.txt` del repositori que als apartats anteriors. Si les dependències ja s'han instal·lat tal com s'indica a l'apartat 6.2, no cal repetir la instal·lació. En cas contrari, des de l'arrel del repositori:

```bash
python -m pip install -r requirements.txt
python -m pip check
```

Si no hi ha incompatibilitats, `python -m pip check` retorna `No broken requirements found.` En cas contrari, cal revisar els paquets i les restriccions de versions indicades abans de modificar les dependències. Una vegada instal·lades, només cal preparar els serveis externs i configurar el compte i afegir al fitxer `.env` el referent a LangSmith.

**3. Preparar Ollama i Weaviate:**

Cal tenir Ollama en funcionament i una instància de Weaviate Cloud amb la col·lecció `Recetas` ja poblada, igual que a l'exemple 8.9. Per comprovar el model instal·lat:

```bash
ollama list
```

Si el model escollit encara no està disponible, es pot descarregar, sempre que hi hagi prou memòria i espai al dispositiu:

```bash
ollama pull qwen3.5:9b
```

Si Ollama no està iniciat, executa `ollama serve` en un altre terminal (no cal si l'aplicació ja està en funcionament). No cal tornar a crear la col·lecció de receptes ni iniciar Grafana.

**4. Configurar el fitxer `.env`:**

El programa executa `load_dotenv()` per carregar les variables. Crea o edita `.env` a l'arrel del repositori. Si ja tens les credencials de Weaviate, conserva-les i afegeix només el bloc de LangSmith. La plantilla [`.env.example`](../../.env.example), conté els camps necessaris sense secrets (s'ha de posar el que toqui en cada lloc).

El que hi hauria d'haver en el .env és el següent:

```dotenv
# Weaviate
WEAVIATE_URL=https://EL_TEU_CLUSTER.weaviate.network
WEAVIATE_API_KEY=LA_TEVA_CLAU_WEAVIATE

# Ollama
OLLAMA_MODEL=qwen3.5:9b

# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=LA_TEVA_CLAU_LANGSMITH
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
LANGSMITH_PROJECT=shopping-rag-weaviate-langsmith
```

| Variable             | Funció                                                              |
| -------------------- | ------------------------------------------------------------------- |
| `WEAVIATE_URL`       | URL del clúster on es troba `Recetas`.                              |
| `WEAVIATE_API_KEY`   | Credencial d'accés al clúster.                                      |
| `OLLAMA_MODEL`       | Model local que es fa servir per classificar i generar la resposta. |
| `LANGSMITH_TRACING`  | Activa (`true`) o desactiva (`false`) l'enviament de traces.        |
| `LANGSMITH_API_KEY`  | Credencial per enviar les traces al compte de LangSmith.            |
| `LANGSMITH_ENDPOINT` | URL de l'API de la regió del compte.                                |
| `LANGSMITH_PROJECT`  | Nom del projecte que agrupa les execucions.                         |

Substitueix els valors de mostra per les credencials pròpies. Si s'utilitzen diversos workspaces, comprova que la clau tingui accés al workspace correcte.

No publiquis `.env` a GitHub. Comprova que `.gitignore` inclou `.env` i conserva únicament `.env.example` amb valors de mostra. Si una clau s'ha exposat, revoca-la i crea'n una de nova. A més, `LANGSMITH_TRACING=true` pot activar el tracing automàtic en altres programes LangChain que carreguin el mateix `.env`.
**Posa'l a `false` quan vulguis provar Opik o OpenTelemetry de manera independent, i torna'l a `true` per a l'exemple 12**. El context del programa controla les seves pròpies invocacions, però no modifica el comportament de tots els altres scripts.

**5. Executar el programa i rebre les primeres traces:**

**macOS/Linux (Bash/Zsh):**

```bash
python AI_Observability/code/src/12_shopping_list_weaviate_langsmith.py --check
python AI_Observability/code/src/12_shopping_list_weaviate_langsmith.py
```

**Windows (PowerShell):**

```powershell
python .\AI_Observability\code\src\12_shopping_list_weaviate_langsmith.py --check
python .\AI_Observability\code\src\12_shopping_list_weaviate_langsmith.py
```

`--check` comprova únicament Weaviate i la col·lecció, no valida LangSmith ni Ollama. En executar l'assistent, s'hauria de veure `[LANGSMITH] Proyecto: shopping-rag-weaviate-langsmith`. Introdueix `Añade leche` i després `Recomiéndame recetas con huevos y patatas`. Escriu `exit` per sortir.

**6. Localitzar les traces a la interfície web:**

El projecte es pot crear automàticament en rebre les primeres traces, segons la configuració del compte. A la interfície actual de la pràctica, entra a **All agents** o **Tracing** i busca `shopping-rag-weaviate-langsmith`.

Selecciona la destinació que rep les noves traces i el seu entorn, si apareix un selector (en les captures d’aquesta pràctica, `Production`). Aquest nom correspon a la destinació de tracing de LangSmith, no implica que Ollama ni Python s’executin en un servidor de producció. No cal crear manualment un segon agent amb el mateix nom. Revisa el rang temporal i actualitza la pàgina.

### 6.12. ANÀLISI DE LES TRACES I DEL FLUX D'EXECUCIÓ

**Visualització general de les traces:**

Accedeix a **Tracing**, selecciona l'entorn que conté les traces (en aquest exemple, `Production`), marca `Traces` i escull l'interval temporal `Last 1 day`.

![Llistat de traces de LangSmith](./img/langsmith_overview.png)

<p align="center"><sub>Figura 9. Llistat de traces del projecte LangSmith amb les entrades, les accions, les latències i el consum de tokens.</sub></p>

A la figura 9 es mostren **9 traces correctes** (`langgraph.invoke`). Cada fila representa una petició de l'usuari. Les columnes permeten consultar el missatge d'entrada (`Input`), l'acció seleccionada (`Output`, en aquesta vista), els errors, l'hora d'inici, la durada (`Latency`), els tokens i el temps fins al primer token (`First Token`), quan està disponible.

En aquesta prova es poden identificar les accions `add`, `remove`, `show`, `search_recipe` i `add_recipe`. Les dues cerques de receptes registren durades de 8,38 s i 18,57 s, amb aproximadament 1.267 i 2.386 tokens respectivament. Les operacions que reutilitzen una recepta o mostren la llista necessiten menys temps en aquestes execucions, al voltant de 2–2,4 s. Les dues peticions d'afegir llet duren 6,62 s i 6,03 s: els temps d'inferència també poden variar en operacions senzilles.

Els colors de la columna de latència ajuden a identificar les peticions més lentes. Un valor en vermell no implica necessàriament un error. L'estat de la trace s'indica separadament amb la marca de verificació verda.

**Detall d'una trace i d'un thread:**

Obre una execució `langgraph.invoke` corresponent a una cerca de receptes i selecciona **Details**. Desplega els nodes per veure les inferències, les eines i la cerca vectorial. La vista `Threads` permet agrupar peticions que comparteixen `thread_id`.

![Detall jeràrquic d'una cerca RAG a LangSmith](./img/langsmith_trace.png)

<p align="center"><sub>Figura 10. Detall de la petició «Recomiéndame recetas con huevos y patatas» amb els runs de LangGraph, Ollama i Weaviate.</sub></p>

La captura mostra una execució de 8,38 s i un consum de 1.267 tokens. Les operacions es registren jeràrquicament:

| Run                     | Durada | Tokens | Funció                                       |
| ----------------------- | -----: | -----: | -------------------------------------------- |
| `langgraph.invoke`      | 8,38 s |  1.267 | Execució completa.                           |
| `process_input`         | 2,79 s |      — | Node que interpreta la petició.              |
| `ollama.clasificacion`  | 2,79 s |    847 | Inferència per determinar l'acció.           |
| `route_after_input`     | 0,00 s |      — | Selecció de la branca del graf.              |
| `search_recipe`         | 5,59 s |      — | Node de cerca i generació RAG.               |
| `search_recipes`        | 2,22 s |      — | Eina que recupera i valida les receptes.     |
| `weaviate_near_text`    | 1,29 s |      — | Consulta vectorial instrumentada manualment. |
| `ollama.generacion_rag` | 3,37 s |    420 | Inferència que redacta la resposta.          |

La classificació i la generació sumen 847 + 420 = 1.267 tokens. Les durades dels runs fills ja estan incloses en les dels pares. Per tant, no s'han de sumar totes les files per calcular el temps total.

A la part dreta, `Input`, `Output` i `Attributes` permeten consultar el missatge original, l'acció seleccionada (`action=search_recipe`), la resposta i l'estat, incloses les receptes recuperades a `last_recipes`. El run `route_after_input` permet inspeccionar la decisió del router. Els runs de tipus LLM mostren les entrades, les sortides i els tokens quan el model proporciona aquestes dades. El missatge `[LANGSMITH] Tokens ...` del terminal no és el que alimenta el dashboard: LangChain registra automàticament les inferències.

**Visualització temporal (Waterfall):**

Dins del detall de la mateixa trace, prem **Waterfall**, a la part superior de la columna central.

![Waterfall de la cerca de receptes](./img/langsmith_waterfall.png)

<p align="center"><sub>Figura 11. Distribució temporal dels runs de la cerca RAG mitjançant Waterfall.</sub></p>

A diferència de l'arbre jeràrquic, aquesta vista representa les operacions sobre un eix temporal. La classificació ocupa els primers 2,79 s. Després s'executa `search_recipe` durant 5,59 s. Dins d'aquest node es veu la recuperació de receptes (2,22 s, inclosa la consulta vectorial d'1,29 s) i la generació de la resposta (3,37 s). Això facilita localitzar els colls d'ampolla i distingir el temps del LLM del temps de recuperació de dades.

### 6.13. MONITORING I INTERPRETACIÓ DELS RESULTATS

Entra a **Monitoring → Analytics**, selecciona el projecte i un interval temporal que inclogui les proves. En les captures següents s'utilitza `Last 3 hours`. A diferència dels panells de Grafana de l'apartat 6.9, LangSmith ofereix visualitzacions agregades sense haver d'escriure consultes TraceQL.

**Volum i latència de les traces (Traces):**

![Monitoring: volum i latència de les traces](./img/langsmith_monitoring1.png)

<p align="center"><sub>Figura 12. Trace Count i Trace Latency al Monitoring de LangSmith.</sub></p>

`Trace Count` representa el nombre de traces correctes i fallides per interval temporal. A la captura hi ha diversos pics d'activitat, amb un màxim visible de cinc traces correctes en un interval. `Trace Latency` mostra els percentils P50 (mediana) i P99. Les variacions permeten detectar intervals amb respostes més lentes. El rang temporal i l'actualització de les mètriques poden fer que els gràfics no coincideixin exactament amb el recompte de la taula de traces.

**Execució de les eines (Tools):**

Selecciona la secció `Tools` del Monitoring o desplaça't fins als seus gràfics.

![Monitoring: nombre de crides i latència de les eines](./img/langsmith_monitoring2.png)

<p align="center"><sub>Figura 13. Run Count by Tool i Median Latency by Tool.</sub></p>

`Run Count by Tool` mostra la freqüència d'execució de `add_products`, `remove_products`, `search_recipes` i `show_products`. `Median Latency by Tool` permet comparar el temps de cada eina. En la captura, `search_recipes` presenta una latència mediana d'aproximadament 2,2–2,3 s, mentre que les operacions directes sobre la llista es mantenen molt a prop de zero segons. La diferència s'explica perquè la cerca inclou l'accés remot a Weaviate i el processament dels resultats, mentre que les altres eines modifiquen o consulten una llista en memòria.

**Execució dels nodes (Run Types):**

Selecciona `Run Types` i localitza els gràfics amb `depth=1`.

![Monitoring: nombre d'execucions i latència dels nodes](./img/langsmith_monitoring3.png)

<p align="center"><sub>Figura 14. Run Count by Name i Median Latency by Run Name per als runs de profunditat 1.</sub></p>

El filtre `depth=1` selecciona els fills directes del run arrel (`depth=0`). En aquest exemple permet estudiar els nodes de LangGraph: `process_input`, `add`, `add_recipe`, `search_recipe` i `show`, entre d'altres. `process_input` s'executa abans de seleccionar l'acció, mentre que la resta de nodes apareixen quan s'escull la seva branca. El gràfic de latències mostra que `search_recipe` és més costós que les operacions directes sobre la llista en aquestes proves. La seva mediana és d'uns 5,6 s en un interval i d'uns 12,8 s en un altre.

Aquesta visualització ajuda a estudiar la freqüència de les branques del router i el rendiment de cada node, sense confondre el recompte de nodes amb el nombre total de traces.

**Altres mètriques disponibles:**

| Pestanya            | Què permet analitzar?                                                        |
| ------------------- | ---------------------------------------------------------------------------- |
| **Traces**          | Nombre de traces correctes i fallides, percentils de durada i taxa d'errors. |
| **LLM Calls**       | Freqüència i latència de les inferències.                                    |
| **Cost & Tokens**   | Consum de tokens i cost estimat quan es disposa de les dades corresponents.  |
| **Tools**           | Nombre de crides i rendiment de les eines Python.                            |
| **Run Types**       | Distribució i latència dels runs segons el nom o tipus.                      |
| **Feedback Scores** | Valoracions disponibles de les execucions.                                   |

El consum de tokens també es pot consultar directament a les figures 9 i 10. El cost monetari estimat del model no equival al cost de recursos locals ni a les tarifes de LangSmith. El rang temporal i `Group by` permeten estudiar les mètriques segons les opcions disponibles. Amb poques mostres, els percentils són poc representatius, s'han repetir les proves abans de treure conclusions generals de rendiment.

La secció **Dashboards** del workspace pot permetre crear visualitzacions personalitzades segons el pla i la versió de la interfície. En aquesta pràctica és suficient Monitoring. No s'ha configurat un dashboard personalitzat ni s'han activat avaluadors automàtics. Es pot afegir feedback manual per comprovar si el router tria l'acció esperada i si la resposta respecta les receptes recuperades. Les avaluacions automàtiques poden tenir costos o requisits addicionals.

**Relació amb el codi:** l'[exemple 8.13](./08_examples.md#exemple-12-langsmith) explica la instrumentació, els nodes, les crides del model i les proves de l'assistent. El [snippet](../code/snippets/12_shopping_list_weaviate_langsmith_snippet.py) recull les parts principals del programa.

**Referències tècniques:** [preus i límits de LangSmith](https://www.langchain.com/pricing), [SDK Python de LangSmith](https://reference.langchain.com/python/langsmith), [tracing_context](https://reference.langchain.com/python/langsmith/run_helpers/tracing_context).

### 6.14. COMPARACIÓ ENTRE OPIK, OPENTELEMETRY I LANGSMITH

En els tres exemples s'utilitza el mateix assistent de receptes amb LangGraph, Ollama i Weaviate. Les funcionalitats de l'aplicació es mantenen, però canvia la manera de registrar, emmagatzemar i visualitzar les dades d'observabilitat.

| Aspecte                             | Opik                                                                               | OpenTelemetry + Tempo + Grafana                                                                                                                  | LangSmith                                                                                                                           |
| ----------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Enfocament**                      | Plataforma d'observabilitat i avaluació d'aplicacions d'IA.                        | Estàndard obert d'instrumentació i exportació de traces, mètriques i logs. Requereix altres components per emmagatzemar i visualitzar les dades. | Plataforma d'observabilitat i avaluació d'aplicacions d'IA, amb integració nativa amb LangChain i LangGraph.                        |
| **Instrumentació Python**           | Integració amb `OpikTracer`, callbacks i spans personalitzats amb `@track`.        | SDK d'OpenTelemetry, creació manual de spans i propagació del context en el nostre exemple.                                                      | Tracing automàtic de LangChain i LangGraph amb `ls.tracing_context()`. instrumentació manual de funcions externes amb `ls.trace()`. |
| **Emmagatzematge de traces**        | Opik Cloud en aquesta pràctica.                                                    | Grafana Tempo, executat localment amb Docker en aquesta pràctica.                                                                                | LangSmith Cloud en aquesta pràctica.                                                                                                |
| **Visualització de les execucions** | Logs i arbre jeràrquic de spans.                                                   | Explore, taula de traces i Node Graph configurat a Grafana.                                                                                      | Tracing, arbre jeràrquic de runs, Waterfall i agrupació per threads.                                                                |
| **Mètriques de rendiment**          | Nombre de traces, errors i percentils de latència.                                 | Consultes TraceQL sobre els spans per obtenir les mètriques i representar-les als panells de Grafana.                                            | Monitoring amb nombre de traces, errors, latències, crides al LLM, eines i nodes.                                                   |
| **Consum de tokens**                | Registre de tokens mitjançant la integració i les metadades del model.             | Atributs numèrics als spans d'Ollama i consultes TraceQL.                                                                                        | Registre automàtic de les crides a `ChatOllama` quan es disposa de les metadades d'ús.                                              |
| **Dashboard**                       | Dashboard amb mètriques predefinides.                                              | Dashboard personalitzat creat manualment amb panells i consultes.                                                                                | Gràfics de Monitoring predefinits. Opcions de personalització segons el pla i la interfície.                                        |
| **Configuració inicial**            | Configurar l'API key i el workspace després d'instal·lar les dependències comunes. | Arrencar Docker, configurar l'exportador OTLP/HTTP i crear els panells de Grafana.                                                               | Configurar l'API key, l'endpoint i el projecte al `.env` després d'instal·lar les dependències comunes.                             |
| **Docker en aquesta pràctica**      | No és necessari.                                                                   | Sí, per executar `grafana/otel-lgtm`.                                                                                                            | No és necessari.                                                                                                                    |
| **Ús gratuït en aquesta pràctica**  | Pla gratuït d'Opik Cloud, subjecte als seus límits.                                | Eines de codi obert executades localment, sense quota de traces d'un servei Cloud. Consumeixen recursos de l'ordinador.                          | Pla gratuït de LangSmith Cloud, subjecte a límits d'ús i retenció.                                                                  |
| **Avaluació de respostes**          | Eines de feedback i avaluació de respostes.                                        | No incorpora per si sol avaluadors específics de LLM. Cal implementar-los o integrar altres eines.                                               | Feedback, datasets, experiments i avaluadors. Algunes opcions poden tenir costos addicionals.                                       |
| **Avantatge principal**             | Facilita l'observabilitat de LLM amb una plataforma integrada.                     | Gran flexibilitat i control sobre la instrumentació, les dades i les visualitzacions. Aplicable també a altres tipus de serveis.                 | Registra automàticament bona part del flux de LangGraph, amb poca instrumentació addicional.                                        |
| **Limitació principal**             | En el servei Cloud, dependència dels límits i les condicions de la plataforma.     | Més configuració i manteniment de la infraestructura i dels dashboards.                                                                          | En el servei Cloud, dependència dels límits, la retenció i les condicions de la plataforma.                                         |

**Interpretació de la comparació:**

- **Opik** permet analitzar aplicacions d'IA mitjançant una interfície especialitzada que integra traces i mètriques de rendiment.
- **OpenTelemetry amb Tempo i Grafana** permet controlar de manera més detallada la instrumentació i construir visualitzacions adaptades a les necessitats del sistema. OpenTelemetry no és un dashboard: genera i exporta les dades, Tempo les emmagatzema i Grafana les visualitza.
- **LangSmith** facilita especialment l'observabilitat de programes desenvolupats amb LangChain i LangGraph, ja que registra automàticament els nodes, el router, les eines i les inferències compatibles. Les operacions externes, com la consulta directa a Weaviate, es poden instrumentar manualment.

Cal diferenciar **LangGraph**, que defineix i executa el flux de l'agent, de **LangSmith**, que observa les execucions. LangGraph continua sent el mateix en els tres exemples, no és una alternativa a Opik o OpenTelemetry com a plataforma d'observabilitat.

Cap de les tres integracions modifica per si sola les decisions del router ni millora automàticament les respostes del LLM. El seu objectiu és facilitar la comprensió del funcionament intern, la detecció d'errors i l'anàlisi del rendiment. L'elecció depèn del grau de personalització, de la infraestructura disponible, de la privadesa de les dades i de la facilitat d'integració amb l'aplicació.
