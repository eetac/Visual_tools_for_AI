# Manual d’explicacions i exemples

## 1. LLM (LARGE LANGUAGE MODEL)
Un LLM (Large Language Model) és un model d’intel·ligència artificial entrenat amb grans quantitats de dades per aprendre patrons del llenguatge i generar respostes a partir d’una entrada proporcionada per l’usuari.

Aquests models poden realitzar diferents tipus de tasques, com ara respondre preguntes, generar i resumir text, traduir contingut, analitzar i generar codi, entre d’altres. Alguns exemples de famílies de LLM són Qwen, Gemma, Llama, Mistral, DeepSeek...

El funcionament d’un LLM es basa en la generació de text token a token. Un token pot correspondre a una paraula, una part d’una paraula o un símbol. A partir del text introduït i del context disponible, el model calcula quin és el següent token més adequat i repeteix aquest procés fins a construir la resposta completa.

### 1.1. FUNCIONAMENT D’UN LLM
El següent esquema representa com un LLM processa una pregunta i genera una resposta, des del moment en què l'usuari introdueix el text fins que el model acaba de respondre.

**Figura 1. Esquema funcionament LLM**

1. Entrada de l’usuari: l'usuari introdueix una pregunta o instrucció (prompt). Aquesta entrada pot incloure una pregunta, instruccions, codi o informació addicional. El model utilitzarà tant aquesta entrada com el context disponible de la conversa per generar una resposta.

2. Tokenització: un LLM no processa directament les paraules tal com les llegim nosaltres. Primer utilitza un tokenitzador, que transforma el text en unitats més petites anomenades tokens. Un token pot representar una paraula completa, una part d'una paraula, un número o un símbol. La divisió real depèn del tokenitzador utilitzat per cada model. Posteriorment, aquests identificadors es transformen en representacions numèriques (vectors) que poden ser processades per la xarxa neuronal.

3. Processament mitjançant LLM: aquesta és la part principal del funcionament. El model rep els tokens i els processa mitjançant la seva xarxa neuronal. 

Durant aquest processament utilitza diferents elements:
Paràmetres: valors numèrics apresos durant l'entrenament que permeten identificar patrons i relacions entre conceptes.
Context: informació de la pregunta, de la conversa anterior i dels tokens generats fins al moment.
Mecanismes d'atenció: permeten relacionar diferents parts de la seqüència per interpretar-ne el significat.

Per exemple, quan el model rep la pregunta “Què és la fotosíntesi?”, pot relacionar el concepte de fotosíntesi amb els coneixements apresos durant l'entrenament sobre les plantes, la llum solar i la transformació d'energia.

A partir d'aquesta informació, el model calcula una distribució de probabilitats dels possibles tokens següents.

4. Generació de la resposta: el model selecciona un token a partir de les probabilitats calculades i de l'estratègia de generació configurada.

Per exemple, podria començar generant: La. Després, torna a processar la seqüència tenint en compte els tokens que acaba de generar: La fotosíntesi. I continuar amb: La fotosíntesi és. Fins a construir una resposta completa, com ara: La fotosíntesi és el procés mitjançant el qual les plantes, les algues i alguns microorganismes transformen l'energia de la llum en energia química.

Per tant, el model no genera tota la resposta de cop, sinó que la construeix progressivament, token a token.

5. Finalització: després de generar cada token, el procés continua fins que es compleix alguna condició de finalització.

### 1.2. INFERÈNCIA
Tot aquest procés rep el nom d'inferència. La inferència consisteix a utilitzar un model que ja ha estat entrenat per processar una entrada i generar una resposta.

És important diferenciar-la de l'entrenament. Les definicions són les següents:
Entrenament: procés durant el qual el model aprèn patrons a partir de grans quantitats de dades i s'ajusten els seus paràmetres.
Inferència: procés durant el qual el model utilitza els paràmetres apresos per generar respostes a noves consultes.

Quan s'executa un model com Qwen mitjançant Ollama, el sistema està realitzant inferència local. Això significa que el model utilitza els recursos de càlcul de l'ordinador per generar respostes, sense tornar-se a entrenar ni modificar els seus paràmetres amb cada consulta.

## 2. QUÈ ÉS OLLAMA?
Ollama és una eina de codi obert que permet descarregar, gestionar i executar LLMs directament en un ordinador. És compatible amb diferents famílies de models, com Qwen, Llama o Gemma i facilita la seva execució sense necessitat de dependre de serveis externs al núvol. Ollama no és un model d'intel·ligència artificial en si mateix, sinó el programari que s'encarrega de carregar els models i gestionar els recursos de càlcul necessaris per executar-los, aprofitant la CPU i, quan és compatible, la GPU de l'ordinador per accelerar la inferència.

Un dels principals avantatges d'Ollama és que permet executar models d'intel·ligència artificial de manera local, mantenint el control sobre les dades i sense costos per consulta. Un cop descarregats, els models es poden utilitzar sense connexió a Internet per realitzar tasques com generar text, respondre preguntes, analitzar codi o processar imatges, segons les capacitats de cada model. A més, Ollama proporciona una API local que facilita la integració dels models amb aplicacions Python, interfícies gràfiques i frameworks com LangChain o LangGraph, permetent desenvolupar aplicacions i agents d'intel·ligència artificial personalitzats.

## 3. INSTAL·LACIÓ I ÚS D’OLLAMA A macOS
### 3.1. COMPROVACIÓ DE LES CARACTERÍSTIQUES
Abans d’instal·lar Ollama es pot comprovar el processador i la memòria disponible.

Des del Terminal: system_profiler SPHardwareDataType
Apareixerà informació similar a:

**Figura 2. Informació del mac**

En alguns ordinadors Mac amb Apple Silicon (com M1, M2, M3, M4), Ollama pot utilitzar la GPU integrada del xip per accelerar l’execució dels models.

### 3.2. INSTAL·LAR OLLAMA
Obrir l’aplicació Terminal i executar: 

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Aquest script descarrega i instal·la Ollama a macOS i afegeix la comanda ollama al sistema.

En acabar, comprovar que s’ha instal·lat correctament: ollama --version
Hauria d’aparèixer una resposta similar a: ollama version X.X.X

Per obrir l’assistent inicial d’Ollama: ollama

### 3.3. ESCOLLIR UN MODEL
Abans de descarregar un model és important escollir-ne un que s’adapti als recursos disponibles de l’ordinador. Els principals factors a tenir en compte són la memòria disponible del MAC, la mida del model, el context que es vol utilitzar i el tipus de tasca.

Ollama disposa d’una biblioteca de models on es poden consultar les diferents famílies i versions disponibles. Aquesta biblioteca es va actualitzant contínuament amb nous models.

És important saber que mateix model pot tenir mides diferents. Per exemple,  qwen3.5:4b i qwen3.5:9b. On la lletra B indica aproximadament el nombre de milers de milions de paràmetres.

En general, que un model sigui més gran indica més capacitat i més raonament, però també més memòria, més consum i menys velocitat. Un model més gran no és necessàriament sempre millor. També depèn de la seva arquitectura, entrenament i especialització.

Per mirar la mida aproximada de cada model es pot buscar a la biblioteca d’Ollama.  Per exemple, la família Qwen 3.5 disposa actualment de variants com:
qwen3.5:0.8b → aproximadament 1,2-1,3 GB
qwen3.5:2b → aproximadament 2,7-3,1 GB
qwen3.5:4b → aproximadament 3,3-4,0 GB

La mida del fitxer no correspon exactament a la memòria total que consumirà durant l’execució. També cal memòria per a context, cache, buffers, sistema operatiu…. Per tant, no és recomanable escollir un model que ocupi pràcticament tota la memòria disponible.

### 3.4. DESCARREGAR UN MODEL
Un cop escollit el model, es descarrega.

Per descarregar un model: ollama pull nom_del_model (per exemple: qwen3.5:9b)

Durant la descàrrega es mostrarà el progrés (pulling manifest, pulling …, success).

Es poden instal·lar diversos models. Aquests models queden guardats al disc del Mac. Tenir diversos models instal·lats no significa que tots estiguin ocupant RAM simultàniament. La memòria important es consumeix quan el model està carregat i en execució.

### 3.5. COMPROVAR MODELS INSTAL·LATS
Per comprovar els models que es tenen instal·lats: ollama list

Exemple:

**Figura 3. Models instal·lats**

### 3.6. EXECUTAR UN MODEL
Per executar el model i iniciar una conversa: ollama run qwen3.5:9b

Llavors, apareixerà >>> i ja es pot iniciar la conersa.
### 3.7. COMPROVAR MODELS CARREGATS A MEMÒRIA
Per veure quins models estan actualment carrgats i també per mirar si el model és adequat pel nostre mac, en un altre terminal executem: ollama ps

Per terminal apareixerà una mena de taula amb informació rellevant:

**Figura 4. ollama ps**

El cas ideal és 100% GPU ja que indica que el model està utilitzant completament l’acceleració gràfica.

També es pot obrir Monitor d’Activitat → Memòria i comprovar la pressió de memòria.
Si la pressió es manté en verd i el sistema continua funcionant amb fluïdesa, el model és adequat.
Si  la pressió de memòria és groga o vermella, el Mac va molt lent o el model tarda excessivament convé utilitzar un model més petit o reduir el context.

### 3.8. PER ATURAR UN MODEL
Quan ja no necessitem fer més preguntes a un model, s’escriu: ollama stop qwen3.5:9b

Amb aquesta comanda, aturem el model. És a dir, no s’elimina del disc sinó que es descarrega de memòria, deixa d’utilitzar GPU i allibera recursos.

Per comprovar que s’ha aturat correctament: ollama ps (i ha de sortir buit)

## 4. LANGCHAIN I LANGGRAPH
Abans d'analitzar els exemples de Python, és important entendre el paper de LangChain i LangGraph en el desenvolupament d'aplicacions basades en models de llenguatge.

### 4.1. LANGCHAIN
LangChain és un framework que facilita la integració de models de llenguatge (LLM) amb aplicacions Python i altres recursos externs, com funcions, bases de dades, documents o APIs.

Permet desenvolupar aplicacions en què el model no es limita a respondre preguntes, sinó que també pot utilitzar eines per obtenir informació o executar determinades operacions.

Per exemple, si un usuari pregunta quin temps fa en una ciutat, un LLM sense eines només pot respondre amb els coneixements que té o amb la informació que se li proporciona. En canvi, amb LangChain es pot connectar el model a una funció Python que consulti dades meteorològiques.

Els principals components són:
LLM: model que interpreta les instruccions i genera respostes. En aquests exemples s'utilitza Qwen, executat localment amb Ollama.
Tools: funcions o recursos externs que el model pot sol·licitar quan necessita realitzar una operació.
Agent: sistema que utilitza el LLM per decidir quines eines ha de fer servir per completar una tasca.
Messages: missatges que representen les instruccions, les preguntes de l'usuari, les respostes del model i els resultats de les eines.

Aplicació en Python
Per connectar LangChain amb Ollama s'utilitza la classe ChatOllama:
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3.5:9b",
    temperature=0,
)

Aquest codi crea un objecte que permet comunicar-se amb Qwen mitjançant el servidor local d'Ollama.

Per enviar una consulta:
response = llm.invoke(
    "Explica què és un LLM"
)
print(response.content)

En aquest cas, LangChain envia la pregunta a Ollama, Ollama executa el model i retorna la resposta generada.

Quan s'incorporen eines, el funcionament es modifica:
Usuari → Agent LangChain → LLM → Sol·licitud d'eina → Execució Python → Resultat → 
→ LLM → Resposta final
És important remarcar que el LLM no executa directament el codi Python. El model pot generar una sol·licitud per utilitzar una eina, però és LangChain qui s'encarrega de cridar la funció corresponent.

### 4.2. LANGGRAPH
LangGraph és un framework orientat a construir aplicacions i agents amb fluxos d'execució més estructurats, utilitzant grafs formats per nodes i connexions.

Mentre que LangChain facilita la integració de models i eines, LangGraph permet definir explícitament quines operacions s'executen, en quin ordre, com es prenen les decisions i quin estat es conserva.

Els principals components són:
State (estat): estructura que emmagatzema la informació compartida entre els diferents passos del programa.
Nodes: funcions Python que realitzen una operació determinada.
Edges: connexions que indiquen quin node s'executarà després.
Conditional edges: connexions condicionals que permeten seleccionar diferents camins segons el resultat d'una funció.
Router: funció que decideix quin camí ha de seguir l'execució.
Checkpointer: mecanisme que permet conservar l'estat entre diferents execucions del graf.

Exemple de funcionament
Suposem una aplicació que gestiona una llista de la compra.

L'usuari introdueix: afegeix llet a la llista.
El procés podria ser:
Usuari → process_input → LLM interpreta la petició → action = "add" → Router → Node add →
→ Funció Python add_products() → Llista actualitzada → Resposta final

En aquest exemple, el LLM interpreta el llenguatge natural i retorna l'acció que considera adequada. Posteriorment, el router de LangGraph llegeix aquesta acció i selecciona el node corresponent. La modificació real de la llista es fa mitjançant una funció Python, no directament amb el LLM.

Creació d'un graf
En Python, LangGraph permet definir una estructura com aquesta:
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

Amb add_conditional_edges() es poden definir connexions condicionals que determinen quin node s'executa segons el resultat del router.

Finalment, amb compile() es construeix el graf executable i amb invoke() s'inicia una execució.

### 4.3. DIFERÈNCIA ENTRE LANGCHAIN I LANGGRAPH (no són excloents l’un de l’altre)
Les diferències principals entre LangChain i LangGraph són les següents:
LangChain
LangGraph
Connecta models amb eines i altres recursos
Organitza l'execució mitjançant un graf
Facilita la creació d'agents
Permet controlar explícitament nodes i transicions
Gestiona interaccions amb el LLM
Gestiona l'estat i el recorregut de l'aplicació
Permet fer tool calling
Permet incorporar condicions, bucles i diferents camins

## 5. RAG (RETRIEVAL-AUGMENTED GENERATION)
RAG (Retrieval-Augmented Generation) és una tècnica que permet millorar les respostes d'un model de llenguatge incorporant informació recuperada d'una font externa, com ara una base de dades, documents o altres sistemes d'emmagatzematge.

Un LLM genera respostes a partir dels coneixements adquirits durant l'entrenament i del context que rep en cada consulta. D’aquesta manera, aquests coneixements poden no incloure informació específica d'una aplicació, documents  o dades actualitzades. RAG permet solucionar aquesta limitació proporcionant al model informació rellevant abans de generar la resposta. D'aquesta manera, el LLM pot respondre basant-se en dades que no necessàriament formen part del seu entrenament.

### 5.1. FUNCIONAMENT D'UN SISTEMA RAG
El funcionament d'un sistema RAG es divideix en tres etapes principals: retrieval, augmentation i generation.

1. Retrieval (recuperació d'informació)
Quan l'usuari introdueix una consulta, el sistema busca informació relacionada amb la petició en una font externa. En sistemes que utilitzen bases de dades vectorials, aquesta cerca pot realitzar-se mitjançant representacions numèriques del contingut (embeddings).
Un embedding és un vector numèric que representa determinades característiques semàntiques d'un text. Això permet comparar el significat de diferents consultes i documents, encara que no utilitzin exactament les mateixes paraules. Per exemple, una consulta com «receptes per a un sopar ràpid» pot recuperar receptes descrites com a «plats fàcils de preparar en pocs minuts».

2. Augmentation (ampliació del context)
Una vegada recuperada la informació, Python prepara un nou prompt que incorpora tant la pregunta original de l'usuari com les dades obtingudes. El model ja no rep únicament la pregunta, sinó també informació addicional que pot utilitzar per elaborar la resposta.

3. Generation (generació de la resposta)
Finalment, el LLM processa el prompt ampliat i genera una resposta en llenguatge natural. En aquesta etapa, el model no necessita conèixer prèviament els documents recuperats. Pot utilitzar-los directament perquè formen part del context proporcionat.

El fet d'utilitzar RAG no garanteix automàticament que totes les respostes siguin correctes, però permet reduir la dependència dels coneixements interns del model i fonamentar les respostes en informació concreta.

### 5.2. BASES DE DADES VECTORIALS: WEAVIATE
En els exemples desenvolupats a continuació, s'utilitza Weaviate Cloud, una base de dades vectorial que permet emmagatzemar informació estructurada i recuperar registres mitjançant cerques semàntiques. A diferència d'una cerca tradicional basada únicament en la coincidència de paraules, una cerca vectorial permet identificar contingut relacionat amb el significat de la consulta. Per fer-ho, la informació emmagatzemada es representa mitjançant vectors i es comparen les representacions de la consulta i dels registres disponibles.

En aquests exemples (8.7, 8.8, 8.9, 8.10) s'utilitza la col·lecció Recetas, que conté informació sobre diferents receptes.

Entre les propietats disponibles es troben:
Propietat
Informació
Propietat
Informació
nombre
Nom de la recepta
ingredientes
Ingredients i quantitats
categoria
Categoria del plat
ingredientesClave
Ingredients principals
dieta
Tipus de dieta
preparacion
Instruccions de preparació
tiempoMin
Temps de preparació en minuts
descripcion
Descripció de la recepta
raciones
Nombre de racions

La cerca semàntica s'executa amb el mètode near_text() del client Python de Weaviate: result = collection.query.near_text(**kwargs). Aquesta instrucció consulta els vectors de la col·lecció per recuperar receptes relacionades amb el text introduït.

Perquè funcioni, la col·lecció ha de disposar d'una configuració de vectorització o de vectors compatibles amb la consulta.

### 5.3. APLICACIONS I AVANTATGES DE RAG
RAG permet desenvolupar assistents que utilitzen informació específica sense necessitat d'entrenar un nou model. Aquesta arquitectura és especialment útil en aplicacions que requereixen consultar documentació tècnica, manuals, bases de dades internes, normatives o altres fonts d'informació. També permet actualitzar les dades disponibles modificant el contingut de la base de dades, sense haver de modificar els paràmetres del LLM.

La qualitat del sistema depèn tant de la capacitat del model per interpretar les dades com de la rellevància i la qualitat de la informació recuperada.

En el projecte de receptes, això significa que el LLM no inventa les receptes que s'han de mostrar, sinó que rep una selecció de resultats recuperats de Weaviate i genera una explicació a partir d'aquesta informació.

## 6. MCP SERVER (MODEL CONTEXT PROTOCOL)
MCP (Model Context Protocol) és un protocol obert i estandarditzat que permet connectar aplicacions d'intel·ligència artificial amb eines, fonts de dades i serveis externs. Habitualment, un LLM genera respostes a partir de la informació proporcionada en el prompt i dels coneixements adquirits durant el seu entrenament. Tanmateix, el model no pot accedir directament als fitxers d'un ordinador, consultar una base de dades o executar determinades operacions si l'aplicació no li proporciona els mecanismes necessaris.

MCP facilita aquesta integració mitjançant una arquitectura de comunicació estandarditzada entre aplicacions i servidors que ofereixen diferents funcionalitats.

Per exemple, mitjançant MCP es podria connectar un assistent basat en un LLM amb:
El sistema de fitxers local, per llegir documents o consultar directoris.
Una base de dades, per recuperar informació emmagatzemada.
Una API externa, per obtenir dades d'un servei.
Un repositori de codi, per consultar fitxers i informació d'un projecte.
Una aplicació que executi funcions Python específiques.

Un dels principals avantatges és que les eines es poden desenvolupar independentment de l'aplicació que utilitza el LLM. D'aquesta manera, un mateix servidor MCP pot ser utilitzat per diferents aplicacions compatibles.

### 6.1. ARQUITECTURA MCP
MCP utilitza una arquitectura client-servidor formada per tres components principals:
MCP Host
MCP Client
MCP Server

1. MCP Host
És l'aplicació principal que necessita accedir a funcionalitats externes. El host gestiona l'experiència de l'usuari, la integració amb els models de llenguatge i les connexions amb els servidors MCP. Per exemple, un editor de codi amb assistent d'intel·ligència artificial pot actuar com a MCP Host.

2. MCP Client
És el component que estableix i gestiona la comunicació amb un servidor MCP. Les seves responsabilitats principals són establir la connexió, descobrir les funcionalitats que ofereix el servidor, enviar sol·licituds i rebre els resultats. Normalment, el host crea un client MCP per a cada connexió amb un servidor.

3. MCP Server
És el programa que proporciona les funcionalitats a través del protocol. El servidor pot executar funcions Python, consultar bases de dades, accedir a fitxers o comunicar-se amb altres serveis.

El servidor no necessita incorporar un LLM. Pot limitar-se a oferir funcions que posteriorment seran utilitzades per altres aplicacions. Per exemple, un servidor MCP especialitzat en fitxers podria exposar les operacions list_files() i read_file(). Quan el client sol·licita executar list_files(), és el servidor qui executa la funció corresponent i retorna el resultat.

**Figura 5. Arquitectura MCP**

### 6.2. FUNCIONALITATS D'UN MCP SERVER
Un servidor MCP pot proporcionar diferents tipus de funcionalitats. Les tres primitives principals són Tools, Resources i Prompts.

1. Tools
Les tools són funcions executables que el servidor posa a disposició dels clients. Permeten realitzar operacions concretes, com consultar una API, executar un càlcul o modificar informació.

Per exemple, un servidor podria exposar la funció següent:
@mcp.tool()
def calculate_flight_time(
    distance_km: float,
    speed_kmh: float
) -> float:
    """Calculate flight time in minutes."""
    return (distance_km / speed_kmh) * 60

Aquesta funció rep una distància i una velocitat, i retorna el temps de vol en minuts. El decorador @mcp.tool() registra la funció com una eina del servidor.

D'aquesta manera, quan un client MCP consulta les eines disponibles, pot descobrir calculate_flight_time(), els arguments que necessita i la seva descripció. Si posteriorment sol·licita executar-la, el servidor realitza el càlcul amb Python i retorna el resultat.

El LLM no executa directament la fórmula. El model pot sol·licitar que s'utilitzi l'eina, però el càlcul real és responsabilitat del servidor.

2. Resources
Els resources permeten proporcionar informació que una aplicació pot llegir i incorporar al seu context. A diferència de les tools, que representen operacions executables, els resources estan orientats a exposar contingut.

Per exemple, un servidor podria proporcionar el contingut d'un document o informació sobre la configuració d'un sistema.

3. Prompts
Els prompts són plantilles reutilitzables que permeten estructurar les instruccions proporcionades a un model.

Per exemple:
@mcp.prompt()
def explain_code(language: str) -> str:
    """Generate a prompt to explain code."""
    return (
        f"Explain how this {language} "
        "code works step by step."
    )

El servidor proporciona la plantilla, però no executa necessàriament cap inferència. El client pot recuperar el prompt i utilitzar-lo posteriorment en una interacció amb un LLM.

### 6.3. COMUNICACIÓ ENTRE CLIENT I SERVIDOR
MCP utilitza missatges estructurats basats en JSON-RPC 2.0 per intercanviar sol·licituds, respostes i notificacions. El protocol defineix els mecanismes necessaris perquè un client pugui descobrir les capacitats d'un servidor i utilitzar-les.

Per exemple, un client pot sol·licitar la llista d'eines disponibles mitjançant l'operació tools/list. Si vol executar una eina concreta, utilitza tools/call, proporcionant-ne el nom i els arguments.

Una sol·licitud per calcular un temps de vol (amb la tool anteriorment descrita) podria tenir una estructura equivalent a:
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculate_flight_time",
    "arguments": {
      "distance_km": 12,
      "speed_kmh": 40
    }
  }
}

El servidor interpreta la sol·licitud, valida els arguments i executa la funció Python. En aquest cas, el resultat seria un temps de vol de 18 minuts. Posteriorment, el servidor retorna el resultat al client mitjançant una resposta estructurada del protocol.

La biblioteca MCP s'encarrega de la comunicació, la serialització de les dades i la validació dels arguments.

Hi ha diferents mecanismes de transport: stdio, streamable HTTP.
stdio (Standard Input/Output)
S'utilitza principalment quan el servidor s'executa localment. El client inicia el servidor com un procés i es comunica amb ell mitjançant l'entrada i la sortida estàndard. És una opció adequada per connectar aplicacions amb eines locals sense necessitat d'obrir un port de xarxa.

Streamable HTTP
Permet establir comunicació amb un servidor a través d'HTTP. És especialment útil quan el servidor es troba en una altra màquina o s'ha desplegat com un servei accessible per xarxa. Aquest transport facilita que diferents clients es puguin comunicar amb un servidor remot.

La selecció del transport no modifica la finalitat de les eines: el servidor continua proporcionant les mateixes operacions, però canvia el mecanisme utilitzat per comunicar-se amb els clients.

### 6.4. FUNCIONAMENT I FLUX D’EXECUCIÓ
Per entendre com funciona MCP, suposem una aplicació amb un LLM que disposa d'un servidor MCP amb una eina per calcular temps de vol (la que s’ha vist anteriorment).

L'usuari introdueix: “¿Cuánto tardaría un dron en recorrer 12 km a 40 km/h?”

En una aplicació en què el LLM disposa de les eines del servidor, el funcionament podria ser el següent:
Entrada de l'usuari: l'usuari introdueix la pregunta a l'aplicació principal (MCP Host).
Disponibilitat de les eines: el client MCP es connecta al servidor i consulta les eines disponibles. Aquesta operació pot haver-se realitzat prèviament i no és necessari repetir-la a cada pregunta.
Interpretació del LLM: l'aplicació proporciona al model la pregunta i la descripció de les eines disponibles. El LLM interpreta que necessita calcular un temps de vol i pot generar una sol·licitud per utilitzar calculate_flight_time().
Sol·licitud al MCP Client: l'aplicació rep la decisió del model i demana al client MCP que executi l'eina, proporcionant els arguments distance_km=12 i speed_kmh=40.
Comunicació MCP: el client envia la sol·licitud al servidor mitjançant el protocol.
Execució al servidor: el MCP Server executa la funció Python calculate_flight_time() i obté un resultat de 18 minuts.
Retorn del resultat: el servidor retorna el resultat al client MCP, que el proporciona a l'aplicació principal.
Resposta del LLM: l'aplicació pot enviar el resultat al model perquè generi una explicació en llenguatge natural.
Resposta final: l'aplicació mostra la resposta a l'usuari.

**Figura 6. Flux d’execució d’una petició amb MCP i LLM**

Aquest esquema mostra que el LLM intervé per interpretar la petició i, quan l'aplicació ho permet, decidir quina eina utilitzar. En canvi, el client MCP s'encarrega de la comunicació i el servidor executa la funció.

## 7. OBSERVABILITAT (OPIK)
L'observabilitat és la capacitat de monitoritzar, registrar i analitzar el funcionament intern d'una aplicació basada en models de llenguatge.

Quan es desenvolupa una aplicació que incorpora LangChain, LangGraph, Ollama, Weaviate o altres eines, no és suficient comprovar que el sistema genera una resposta correcta. També és important conèixer quines funcions s'han executat, quin recorregut ha seguit la petició, quant temps ha necessitat cada operació i quants recursos s'han consumit.

Per obtenir aquesta informació s'utilitza Opik, una plataforma d'observabilitat desenvolupada per Comet que permet registrar les execucions d'aplicacions d'IA, visualitzar les seves operacions internes i analitzar mètriques de rendiment.

### 7.1. CONCEPTES PRINCIPALS
Els principals conceptes que s'utilitzen a Opik són:

Descripció
Trace
Registre de l'execució completa d'una petició.
Span
Operació individual dins d'una trace.
Thread
Agrupació de traces relacionades amb una mateixa conversa o sessió.
Latency
Temps necessari per executar una operació o completar una petició.
Token usage
Nombre de tokens processats i generats pel LLM.
Error rate
Percentatge d'execucions que han registrat errors.
Estimated cost
Estimació del cost associat a les crides als models, quan és calculable.
Metadata
Informació addicional, com el model utilitzat, el proveïdor o els paràmetres de l'execució.

Una trace representa el recorregut complet d'una petició. Per exemple, quan un usuari sol·licita una recepta, la trace pot incloure la interpretació del missatge, la consulta a Weaviate, la recuperació de receptes i la generació de la resposta. Dins de cada trace es registren diferents spans, que representen les operacions individuals del procés. Els spans poden contenir altres spans, formant una estructura jeràrquica que permet identificar les dependències i analitzar el temps consumit en cada etapa.

### 7.2. INSTAL·LACIÓ I CONFIGURACIÓ D'OPIK
Per incorporar observabilitat a una aplicació Python, primer cal instal·lar Opik i configurar la connexió amb la plataforma.

Instal·lació:
Primer s'obre el Terminal i s'accedeix a la carpeta del projecte.

Si ja existeix un entorn virtual, s'activa: source .venv/bin/activate
A continuació, s'instal·la Opik: python -m pip install opik

Configuració del compte:
Per utilitzar Opik Cloud, cal disposar d'un compte a la plataforma de Comet. Es pot accedir a través de: https://www.comet.com/opik

Una vegada creat el compte, cal identificar el workspace i disposar d'una API key. El workspace és l'espai de treball que agrupa els projectes disponibles. Un projecte organitza les traces i les mètriques d'una aplicació concreta.

Per configurar la connexió des del terminal: opik configure. Aquesta ordre inicia un assistent de configuració. Cal seleccionar l'entorn corresponent i proporcionar les credencials necessàries, com l'API key i el workspace.

Crear un nou projecte:
Per separar les traces de diferents aplicacions és recomanable utilitzar un projecte d'Opik per a cadascuna. Per crear-ne un des de la interfície web, s'accedeix al workspace corresponent i a la secció de projectes. Des d'aquesta pàgina es pot crear un projecte nou, assignant-li un nom identificatiu.

Si el projecte encara no existeix, Opik pot crear-lo automàticament quan rep les primeres traces. Per tant, no és obligatori crear-lo manualment abans d'executar el programa.

Per utilitzar un projecte diferent, només cal modificar el valor de project_name.

És important que les traces s'enviïn al projecte correcte. En aquest exemple, el nom està especificat directament dins de OpikTracer, de manera que aquest valor té prioritat sobre una configuració general del nom del projecte.

### 7.3. ANÀLISI DE LES TRACES
Una vegada executades diferents peticions, les traces es poden consultar des de la interfície web d'Opik. La secció Observability → Logs permet visualitzar les execucions registrades i accedir al detall de cadascuna.

Visualització general de traces:

**Figura 7. Registre de traces amb el nombre d’execucions, errors, durada mitjana i entrades i sortides de les peticions**
A la captura es poden observar les traces generades durant les proves de l'assistent.

En el període seleccionat apareixen:
Traces registrades: 25
Errors: 1
Error rate: 4%
Durada mitjana: 8,6 s

A la taula inferior de la figura 7 es mostren les entrades (Input) i les sortides (Output) de diferents interaccions.

Per exemple, es poden observar peticions relacionades amb la cerca de receptes, l'addició d'ingredients i la modificació de la llista de la compra. Això permet comprovar que les interaccions de l'usuari estan quedant registrades correctament.

També és possible utilitzar els filtres de la interfície per localitzar traces amb errors, consultar una petició concreta o restringir els resultats a un període determinat.

**Dashboard:**
La secció Dashboards proporciona una visió agregada del funcionament de l'aplicació.

**Figura 8. Dashboard (nombre de traces, els errors, els percentils de latència, el consum de tokens i**
l'evolució temporal de les execucions)

A diferència de Logs, que permet inspeccionar les execucions individualment, aquesta secció facilita l'anàlisi global del rendiment.

En la captura es poden observar les mètriques següents:
Total trace count: 25
Total error count: 1
P50 duration: 5,6 s
P90 duration: 20,9 s
P99 duration: 22,9 s
Cost: no l’especifica (en aquest exemple, les mètriques de cost no proporcionen una estimació útil per al model local. Tot i que executar Qwen amb Ollama no implica un preu per consulta a un proveïdor de LLM, sí que consumeix recursos de l'ordinador, com CPU, GPU, memòria i electricitat)

Els percentils permeten analitzar la distribució dels temps d'execució. El percentil P50 correspon a la mediana, aproximadament la meitat de les execucions tenen una durada igual o inferior a 5,6 segons. El percentil P90 indica que aproximadament el 90% de les execucions tenen una durada igual o inferior a 20,9 segons. Finalment, P99 permet estudiar les execucions més lentes, amb un valor de 22,9 segons en aquesta captura.

Aquests indicadors són útils perquè la durada mitjana no sempre representa adequadament les peticions que necessiten més temps.

**Consum de tokens:**
El dashboard també incorpora una gràfica denominada Token usage - total_tokens. Aquesta gràfica mostra l'evolució dels tokens registrats durant les execucions. El consum pot variar segons la complexitat de la petició, la quantitat de context proporcionat al model i el nombre d'inferències necessàries.

Per exemple, una petició que únicament afegeix un producte pot requerir una sola inferència. En canvi, una consulta RAG pot requerir una primera inferència per interpretar la petició i una segona per generar la resposta utilitzant les receptes recuperades. Això permet comparar el consum de recursos entre diferents tipus d'operacions.

**Volum i durada de les traces:**

**Figura 9. Trace volume i trace duration al dashboard**

Es poden veure també per defecte dues gràfiques més:
Trace volume: representa el nombre d'execucions registrades al llarg del temps.
Trace duration: representa l'evolució de la durada de les execucions.

Aquestes gràfiques permeten identificar períodes amb més activitat i detectar possibles increments dels temps de resposta.
### 7.4. ANÀLISI DETALLADA D’UNA TRACE
Es pot observar també el recorregut complet d’una petició.

**Figura 10. Detall d’una execució de LangGraph mostrant els spans**

L'usuari introdueix: “quiero hacer la 1, asi q añademe los ingredientes a la lista”

La trace mostra una durada aproximada de 2,4 segons.

A la part esquerra apareixen els spans que s'han executat, organitzats jeràrquicament:
LangGraph: representa l'execució general del graf.
process_input: és el primer node de LangGraph, encarregat d'interpretar la petició de l'usuari.
ollama_tokens i ChatOllama: corresponen a la inferència amb Qwen i al registre de les metadades associades. En aquesta etapa, el LLM interpreta que l'usuari vol afegir els ingredients d'una recepta seleccionada anteriorment.
add_recipe: és el node seleccionat per LangGraph després de processar el resultat del model. Aquest node recupera la recepta corresponent de last_recipes, que conté les receptes mostrades en la cerca anterior.
add_products: és la funció Python que afegeix els ingredients de la recepta a la llista de la compra. La captura mostra una durada aproximada de 0,001 segons per a aquesta operació.

La resposta final confirma que s'han afegit els ingredients de la recepta seleccionada.
Aquest exemple permet observar que la major part del temps de la petició està relacionada amb la inferència del LLM, mentre que l'operació Python d’afegir productes necessita molt menys temps. També permet comprovar que no es realitza una nova consulta a Weaviate. El programa reutilitza les receptes emmagatzemades a l'estat de LangGraph i executa directament add_products().

A la part inferior esquerra apareix una representació del graf complet de LangGraph amb els possibles nodes i connexions. Aquest graf representa les rutes disponibles a l'aplicació, no necessàriament totes les operacions executades en aquella petició concreta. A la part dreta es mostren les dades d'entrada i sortida, les etiquetes i les metadades associades a la trace.

Aquest nivell de detall és especialment útil per comprovar que les decisions del LLM es tradueixen correctament en operacions Python.

### 7.5. INTERPRETACIÓ DELS RESULTATS
Les captures anteriors permeten comprovar que la integració d'Opik amb LangGraph, Ollama i Weaviate funciona correctament i que les execucions queden registrades.

A través de la interfície es poden diferenciar tres nivells d'anàlisi:
Logs: permet consultar les interaccions registrades i identificar les que han produït errors.
Dashboard: permet estudiar el rendiment global de l'aplicació mitjançant mètriques de durada, volum d'execucions i consum de tokens.
Detall de les traces: permet inspeccionar el recorregut concret d'una petició i identificar les operacions realitzades per LangGraph, les inferències del LLM i les funcions executades per Python.

D'aquesta manera, Opik facilita la detecció d'errors, l'anàlisi del rendiment i la comprensió del comportament intern dels sistemes basats en intel·ligència artificial.

La seva incorporació no modifica les funcionalitats de l'assistent, però permet estudiar com es generen les respostes i identificar possibles oportunitats de millora.

## 8. EXEMPLES D’ÚS EN PROGRAMES DE PYTHON
### 8.1. test_ollama.py
Aquest primer exemple permet comprovar que Python es pot comunicar correctament amb Ollama i generar respostes utilitzant el model Qwen.

**Funcionament del codi:**
llm = ChatOllama(    
model="qwen3.5:9b",    
temperature=0,
)

response = llm.invoke(    
"Explícame qué es LangChain en dos frases."
)

print(response.content)

**Intervenció del LLM:**
El model intervé quan Python executa: response = llm.invoke(...). En aquest moment, LangChain envia la consulta a Ollama, que carrega o utilitza el model i realitza la inferència.

**Operacions de Python:**
Python s'encarrega de preparar la consulta, executar invoke(), rebre el resultat i mostrar-lo amb print(). En aquest exemple no hi ha eines ni agents. El model únicament genera text.

**Flux d'execució:**
Python → ChatOllama → Ollama → Qwen → Resposta → Python.

Execució: python test_ollama.py

Si apareix una resposta, es comprova que la comunicació entre Python, LangChain, Ollama i Qwen funciona correctament.

### 8.2. 01_simple_agent.py
Aquest exemple introdueix el concepte de tool calling, que permet que el model sol·liciti l'execució de funcions Python.

L'agent disposa d'una eina anomenada get_weather() que retorna informació meteorològica simulada.

**Components del codi:**
La funció Python és:
def get_weather(city: str) -> str:
    """Get weather for a given city."""

    print(
        f"[TOOL EXECUTED] get_weather(city={city})"
    )

    return f"It's always sunny in {city}!"

Aquesta funció rep el nom d'una ciutat i retorna una resposta fictícia.

Posteriorment, es crea l'agent:
agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

Amb tools=[get_weather] s'indica que l'agent pot utilitzar aquesta funció.

**En quin moment intervé el LLM?:**
Quan es crida: result = agent.invoke(...)

LangChain envia al LLM la pregunta de l'usuari, les instruccions del sistema i la descripció de les eines disponibles. El model interpreta la pregunta i pot decidir sol·licitar get_weather().

Per exemple, si l'usuari pregunta: What's the weather in San Francisco?

El model pot retornar una crida estructurada equivalent a: get_weather(city="San Francisco")

**Què fa Python?:**
LangChain rep la sol·licitud del model i executa la funció Python.

La funció retorna: It's always sunny in San Francisco! Aquest resultat es torna a proporcionar al LLM, que el pot utilitzar per redactar una resposta final.

**Flux d'execució:**
L'usuari introdueix una pregunta.
El LLM interpreta la pregunta i decideix si necessita l'eina.
LangChain executa get_weather().
Python retorna les dades meteorològiques simulades.
El LLM rep el resultat i genera la resposta final.

Execució: python 01_simple_agent.py

La traça [TOOL EXECUTED] permet comprovar que la funció s'ha executat realment.

Aquest exemple mostra com el LLM pren la decisió d'utilitzar una eina, mentre que Python realitza l'operació.

### 8.3. 02_multi_agent.py
Aquest exemple amplia l'anterior introduint una arquitectura multiagent, en què diversos agents especialitzats col·laboren per resoldre una petició de l'usuari. En lloc de disposar d'un únic agent amb diferents eines, el programa utilitza un agent supervisor que coordina dos agents independents: un especialitzat en meteorologia i un altre en càlculs de temps de vol.
Els tres agents utilitzen el mateix model Qwen, executat localment mitjançant Ollama, però tenen instruccions i eines diferents. Per tant, no són tres models diferents, sinó tres agents configurats amb el mateix LLM.

Els tres agents són:
Supervisor Agent: rep la pregunta de l'usuari i decideix a quin agent especialitzat ha de delegar cada tasca.
Weather Agent: s'encarrega de respondre preguntes meteorològiques mitjançant la funció get_weather().
Flight Agent: calcula el temps de vol d'un dron mitjançant la funció calculate_flight_time().

Els tres agents utilitzen el mateix model Qwen executat amb Ollama, però tenen instruccions i eines diferents.

**Components del codi:**
Primer es configura el model mitjançant ChatOllama, de la mateixa manera que en l'exemple anterior.

A continuació, es defineixen els agents especialitzats:
weather_agent: disposa de la funció Python get_weather(city), que retorna informació meteorològica simulada d'una ciutat.
flight_agent: disposa de la funció calculate_flight_time(distance_km, speed_kmh), que calcula el temps de vol d'un dron a partir de la distància i la velocitat.
El temps de vol es calcula amb la fórmula: tmin=dkmvkm/h60
Aquest càlcul es realitza directament amb Python. El LLM no calcula el resultat numèric, sinó que interpreta la petició i determina si necessita executar l'eina.

Per permetre que el supervisor utilitzi aquests agents, es defineixen dues funcions intermèdies decorades amb @tool:
@tool
def ask_weather_agent(query: str) -> str:
    """Delegate weather-related questions
    to the weather specialist agent."""

    result = weather_agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    return result["messages"][-1].content

La funció ask_flight_agent() funciona de la mateixa manera, però invoca flight_agent.

Aquestes funcions són importants perquè el supervisor no disposa directament de get_weather() ni de calculate_flight_time(). En canvi, té accés a ask_weather_agent() i ask_flight_agent(), que permeten delegar les tasques als agents especialitzats.

Es crea el supervisor:
supervisor_agent = create_agent(
    model=llm,
    tools=[
        ask_weather_agent,
        ask_flight_agent,
    ],
    system_prompt=(
        "You are a supervisor agent "
        "that coordinates specialized agents."
    ),
)

La instrucció system_prompt estableix que el supervisor ha d'identificar les tasques de l'usuari, delegar-les a l'agent corresponent i combinar els resultats.

**Flux d’execució:**
Suposem que l'usuari introdueix la petició següent: “I want to fly a drone in Barcelona. Tell me the weather and calculate how long it would take to fly 12 km at 40 km/h.”

El recorregut és el següent:
Entrada de l'usuari: Python envia la petició al supervisor executant supervisor_agent.invoke(). Aquesta instrucció inicia una inferència del LLM mitjançant LangChain i Ollama.
Interpretació del supervisor: Qwen analitza la petició i identifica que conté dues tasques diferents: consultar la meteorologia i calcular el temps de vol. El model pot generar dues sol·licituds d'eina, una per a cada agent especialitzat.
Delegació als agents: LangChain rep les sol·licituds i executa les funcions Python ask_weather_agent() i ask_flight_agent(). Aquestes funcions criden els agents corresponents mitjançant .invoke().
Execució dels agents especialitzats: cada agent realitza una nova inferència amb Qwen. El Weather Agent pot sol·licitar get_weather("Barcelona"), mentre que el Flight Agent pot sol·licitar calculate_flight_time(12, 40).
Execució de les funcions Python: LangChain executa les eines sol·licitades. get_weather() retorna informació meteorològica fictícia i calculate_flight_time() calcula un temps de 18 minuts.
Retorn dels resultats: els resultats de Python es proporcionen als agents especialitzats, que poden utilitzar el LLM per generar una resposta. Les funcions intermèdies retornen aquestes respostes al supervisor.
Resposta final: el supervisor rep les dues respostes i utilitza novament Qwen per combinar-les en un únic missatge que es mostra a l'usuari.
És important destacar que el LLM intervé tant en el supervisor com en cadascun dels agents especialitzats, mentre que les funcions Python són les encarregades de proporcionar les dades i realitzar els càlculs.

**Figura 11. Flux d’execució multi agent**

Per executar-lo: python 02_multi_agent.py

Aquest exemple demostra com es poden distribuir les responsabilitats entre diferents agents. El supervisor decideix a quin especialista delegar cada operació i els agents especialitzats gestionen les seves pròpies eines.

### 8.4. 03_my_drone_mission_agent.py
Aquest exemple implementa un assistent capaç d'analitzar la viabilitat d'una missió de dron a partir de diferents paràmetres, com la distància, la velocitat, la direcció del vol, el vent i la bateria disponible.

A diferència dels exemples anteriors, el programa no utilitza el LLM per decidir quines funcions executar. La lògica principal està programada en Python, mentre que el model s'utilitza per respondre preguntes i explicar els resultats dels càlculs.

**Components del codi:**
El programa defineix una estructura MissionState que emmagatzema els paràmetres de la missió. Aquesta estructura permet que l'usuari introdueixi la informació progressivament i que el programa conservi els valors entre diferents missatges.

La funció update_state() analitza el text introduït per l'usuari i actualitza els paràmetres corresponents. Per identificar els valors utilitza expressions regulars de Python, mitjançant la biblioteca re. Per exemple, si l'usuari introdueix una distància de 10 km i una velocitat de 40 km/h, Python identifica els nombres i les unitats a partir de patrons predefinits. Aquesta extracció no requereix una inferència del LLM.

Un cop es disposa de la informació necessària, la funció analyse_mission() coordina tres eines:
calculate_flight_time(): calcula les components del vent, la velocitat efectiva del dron i el temps de vol.
check_wind_safety(): comprova si les condicions de vent respecten els límits de seguretat.
check_battery(): determina si la bateria disponible és suficient per completar la missió mantenint la reserva exigida.

Aquestes funcions estan decorades amb @tool, però són invocades directament pel codi Python, sense que el LLM decideixi quan executar-les.

Per exemple:
flight_result = calculate_flight_time.invoke({
    "distance_km": state.distance_km,
    "drone_speed_kmh": state.drone_speed_kmh,
    "wind_speed_kmh": state.wind_speed_kmh,
    "flight_bearing_deg": state.flight_bearing_deg,
    "wind_direction_from_deg":
        state.wind_direction_from_deg,
})

En aquest cas, .invoke() executa una eina de Python, no el model Qwen. La distinció és important perquè el mateix mètode invoke() es pot utilitzar amb diferents components de LangChain.

**Flux d’execució:**
Entrada de l'usuari: l'usuari introdueix una descripció de la missió al terminal. La funció main() rep el text i determina com s'ha de processar.
Actualització de l'estat: si el missatge conté paràmetres, update_state() els identifica mitjançant expressions regulars i els guarda a MissionState.
Selecció de l'operació: el programa comprova si l'usuari ha proporcionat dades noves, ha demanat una anàlisi, vol consultar els passos de càlcul o ha formulat una pregunta.
Anàlisi de la missió: quan correspon realitzar una anàlisi, Python executa analyse_mission(). Aquesta funció comprova quines dades estan disponibles i crida les eines de vol, vent i bateria quan disposa dels paràmetres necessaris.
Generació de l'informe: Python recull els resultats de les comprovacions i construeix un informe. També genera una traça amb les operacions efectuades, que permet consultar posteriorment com s'han obtingut els resultats.
Intervenció del LLM: si l'usuari formula una pregunta explicativa, com “Why is my mission not feasible?”, el programa executa answer_question(). Aquesta funció prepara un prompt amb l'estat de la missió, l'últim informe i la traça dels càlculs, i crida llm.invoke().
Resposta final: Qwen utilitza la informació proporcionada per generar una explicació en llenguatge natural, sense modificar els paràmetres ni tornar a calcular els resultats de seguretat.

Per tant, existeixen dues rutes principals: una ruta de càlcul, executada íntegrament amb Python, i una ruta d'explicació, en què intervé el LLM.

Si l'usuari únicament demana visualitzar la traça dels càlculs, tampoc no és necessari executar Qwen, ja que aquesta informació està guardada al programa.

**Figura 12. Flux d’execució mission agent**

Per executar-lo: python 03_my_drone_mission_agent.py

Aquest exemple mostra com es poden combinar operacions deterministes amb intel·ligència artificial. Python garanteix que els càlculs s'executin segons les fórmules programades, mentre que el LLM facilita la interpretació dels resultats.

### 8.5. 04_langgraph_drone_mission_agent.py
Aquest exemple implementa les funcionalitats de l'assistent de dron anterior, però reorganitza el programa mitjançant LangGraph. La principal diferència és que el flux d'execució es defineix com un graf format per nodes i connexions. Cada node executa una operació concreta i les connexions condicionals determinen quin serà el següent pas.

D'aquesta manera, LangGraph permet separar la lògica d'interpretació, els càlculs, la generació d'informes i les respostes del LLM.

**Components del codi:**
L'estat compartit del graf es defineix mitjançant DroneMissionState, que conté els paràmetres de la missió, els resultats de les comprovacions i les variables de control necessàries per seleccionar les operacions.

Per conservar la informació entre diferents execucions s'utilitza InMemorySaver, un mecanisme de memòria que permet recuperar l'estat associat a una mateixa sessió.

El primer node és process_input_node(). Aquest node rep el missatge de l'usuari, executa extract_updates() per identificar els paràmetres i actualitza l'estat de la missió. També determina si l'usuari vol iniciar una anàlisi, consultar els passos de càlcul o formular una pregunta.

Posteriorment, el router route_after_input() decideix quin camí seguir. Aquesta funció consulta els valors de l'estat i retorna el nom del següent node.

Els principals nodes disponibles són:
flight_check_node(): executa calculate_flight_time().
wind_check_node(): executa check_wind_safety().
battery_check_node(): executa check_battery().
final_report_node(): prepara l'informe final.
show_trace_node(): mostra els passos dels càlculs.
answer_question_node(): utilitza el LLM per respondre preguntes sobre la missió.

Els nodes de càlcul utilitzen funcions Python. Només answer_question_node() realitza una inferència amb Qwen.

**Flux d'execució:**
Entrada de l'usuari: la funció main() rep el missatge i inicia l'execució del graf mitjançant drone_mission_graph.invoke().
Processament de l'entrada: LangGraph executa process_input_node(). Python interpreta les dades, actualitza l'estat i identifica quines comprovacions s'han de realitzar.
Selecció de la ruta: LangGraph consulta route_after_input(). Aquest router és una funció Python que selecciona el node següent segons les condicions de l'estat. No utilitza el LLM.
Execució dels nodes de càlcul: si la missió requereix una anàlisi, el graf passa pels nodes corresponents de vol, vent i bateria. Cada node executa la seva eina Python i guarda el resultat a l'estat compartit.
Transicions condicionals: després de cada comprovació, els routers route_after_flight() i route_after_wind() determinen si cal executar un altre node o passar directament a l'informe.
Generació de l'informe: final_report_node() recupera els resultats disponibles i construeix la resposta que es mostra al terminal.
Ruta alternativa del LLM: si l'usuari formula una pregunta, route_after_input() selecciona answer_question_node(). Aquest node prepara la informació de la missió i executa llm.invoke() perquè Qwen generi una explicació.

El programa també pot reutilitzar resultats ja calculats. Quan l'usuari modifica un paràmetre, process_input_node() identifica els camps que han canviat i determina quines comprovacions s'han de repetir. D'aquesta manera s'evita executar operacions innecessàries.

És important remarcar que drone_mission_graph.invoke() no significa executar directament el LLM. Aquesta instrucció inicia el graf i LangGraph va executant els nodes. Només es realitza una inferència si el recorregut arriba a un node que crida Qwen.

**Figura 13. Flux d’execució de LangGraph**

Aquest exemple mostra com LangGraph facilita l'organització de processos que disposen de diferents camins d'execució, permetent conservar l'estat i separar les responsabilitats de cada funció.

Execució: python 04_langgraph_drone_mission_agent.py

### 8.6. 05_langgraph_autonomous_mission_planner.py
Aquest exemple amplia el sistema anterior incorporant la planificació, l'avaluació i la proposta de replanificació d'una missió de dron. L'aplicació no es limita a comprovar si una missió és viable, sinó que també identifica les causes que poden impedir completar-la i prepara possibles accions correctives.

El sistema s'organitza mitjançant LangGraph, que controla el recorregut entre les diferents etapes de planificació i validació.

**Components del codi:**
El programa defineix un estat compartit, AutonomousMissionState, que emmagatzema els paràmetres de la missió, el pla actual, la versió del pla, els resultats de les comprovacions i les possibles accions de replanificació.

El graf incorpora diversos nodes:
process_input_node(): interpreta les dades de l'usuari i actualitza l'estat.
mission_planner_node(): construeix el pla de missió a partir dels paràmetres disponibles.
flight_check_node(), wind_check_node() i battery_check_node(): executen les comprovacions corresponents.
evaluate_plan_node(): determina l'estat global de la missió.
replanner_node(): proposa accions correctives si la missió no és viable.
final_report_node(): genera l'informe final.
answer_question_node(): utilitza el LLM per explicar els resultats.

El node evaluate_plan_node() pot classificar la missió amb els estats següents:
Feasible: les comprovacions disponibles indiquen que la missió és viable.
Not Feasible: s'ha detectat alguna condició que impedeix considerar-la viable.
Undetermined: falta informació o alguna comprovació necessària
Invalid: s'ha detectat alguna dada o resultat invàlid.

La selecció de la ruta de replanificació es realitza mitjançant una condició Python dins de route_after_evaluation():
def route_after_evaluation(state):
    if state.get("mission_status") == "NOT FEASIBLE":
        return "replan"

    return "report"

Això significa que, quan l'estat és NOT FEASIBLE, LangGraph dirigeix l'execució cap a replanner_node().

**Flux d'execució:**
Entrada i interpretació: l'usuari introdueix els paràmetres de la missió. Python inicia el graf i process_input_node() identifica i actualitza les dades.
Planificació: el router selecciona mission_planner_node(), que construeix una descripció del pla i actualitza la versió quan correspon. Aquesta etapa utilitza funcions Python.
Comprovacions: LangGraph executa els nodes necessaris per calcular el temps de vol, avaluar el vent i comprovar la bateria. Els càlculs els efectuen les eines Python, no Qwen.
Avaluació: evaluate_plan_node() recupera els resultats, comprova les condicions i determina l'estat global de la missió.
Decisió de replanificació: route_after_evaluation() consulta l'estat obtingut. Si la missió és NOT FEASIBLE, selecciona replanner_node(). En els altres casos, el graf continua cap a l'informe.
Proposta d'accions correctives: replanner_node() analitza els problemes detectats i prepara possibles solucions mitjançant regles Python. Per exemple, pot proposar revisar les condicions de vent, augmentar la disponibilitat de bateria o modificar la ruta. Aquestes propostes no s'apliquen automàticament ni impliquen tornar a executar indefinidament els càlculs.
Generació de l'informe: final_report_node() recull el pla, les comprovacions i les possibles accions correctives, i construeix el resultat final.
Explicació mitjançant el LLM: si posteriorment l'usuari formula una pregunta sobre el pla o els resultats, LangGraph executa answer_question_node(), que proporciona aquesta informació a Qwen mitjançant llm.invoke().

En aquest exemple, la planificació i la replanificació són processos programats en Python. El LLM s'utilitza per respondre preguntes explicatives, no per calcular la viabilitat ni determinar les accions correctives.

**Figura 14. Flux d’execució autonomous mission planner**

Aquest exemple demostra com construir un procés de planificació amb diferents etapes, condicions i rutes alternatives mitjançant LangGraph.

Execució: python 05_langgraph_autonomous_mission_planner.py

### 8.7. 06_shopping_list.py
Aquest exemple implementa un assistent per gestionar una llista de la compra mitjançant llenguatge natural. L'usuari pot afegir, eliminar, substituir o consultar productes sense necessitat d'escriure instruccions amb una sintaxi específica.

El programa utilitza un agent LangChain que interpreta les peticions amb Qwen i disposa de diferents funcions Python per modificar la llista.

**Components del codi:**
La llista de la compra es representa mitjançant una variable Python: shopping_list = []

A continuació, es defineixen quatre eines decorades amb @tool:
add_product(): afegeix un producte.
remove_product(): elimina un producte.
replace_product(): substitueix un producte per un altre.
show_list(): mostra la llista actual.

Aquestes eines realitzen les operacions sobre la variable shopping_list utilitzant instruccions Python, com append(), remove() o l'accés als elements per índex.

Posteriorment es crea l'agent amb create_agent(), proporcionant-li les quatre eines i un system_prompt que defineix el comportament de l'assistent.

Entre les instruccions s'estableix que els noms dels productes s'han de traduir al castellà abans de cridar les eines, que s'han de conservar els detalls dels productes i que les correccions de l'usuari s'han de gestionar amb replace_product().

El programa també conserva un historial de missatges. Aquest historial permet que el model disposi del context de les interaccions anteriors.

**Flux d'execució:**
Suposem que l'usuari introdueix: “Add milk”
Entrada de l'usuari: Python afegeix el missatge a l'historial i crida agent.invoke().
Interpretació del LLM: LangChain envia a Qwen el missatge, les instruccions i les descripcions de les eines. El model interpreta que l'usuari vol afegir un producte i el tradueix al castellà.
Sol·licitud d'eina: Qwen pot generar una sol·licitud estructurada equivalent a add_product(product="leche").
Execució de Python: LangChain rep la sol·licitud i executa add_product(). La funció normalitza el nom, comprova si el producte ja existeix i l'afegeix amb shopping_list.append().
Retorn del resultat: la funció retorna un missatge de confirmació. LangChain proporciona aquest resultat al LLM.
Resposta final: Qwen genera una resposta per a l'usuari i Python actualitza l'historial de missatges.

Si posteriorment l'usuari escriu “pero quería leche de soja”, el model pot utilitzar el context anterior per interpretar que es tracta d'una correcció. En aquest cas, sol·licita replace_product() i Python substitueix el producte original.

El model és qui interpreta la intenció i selecciona la funció, però la llista real només es modifica quan s'executa l'eina Python.

**Figura 16. Flux de gestor de llista de la compra**

Aquest exemple introdueix la gestió d'informació modificable mitjançant tool calling. També mostra la importància de conservar l'historial per interpretar referències i correccions de l'usuari.

Execució: python 06_shopping_list.py

### 8.8. 07_shopping_list_langgraph.py
Aquest exemple implementa la mateixa funcionalitat de llista de la compra, però utilitzant LangGraph per organitzar les operacions en nodes.

La diferència principal respecte a l'exemple anterior és que el LLM no sol·licita directament l'execució de les eines de gestió. En aquest cas, el model interpreta la petició i retorna una estructura JSON amb l'acció que s'ha de realitzar. Posteriorment, un router Python selecciona el node corresponent.

**Components del codi:**
El programa defineix ShoppingState, una estructura que conté la llista de la compra, el missatge de l'usuari, l'últim producte afegit i els camps necessaris per descriure una operació. També utilitza InMemorySaver per conservar l'estat entre les diferents interaccions de la sessió.

El primer node és process_input_node(), que prepara un prompt amb les instruccions del sistema i executa:
response = llm.invoke([
    ("system", system_prompt),
    ("human", state["user_input"]),
])
Aquesta és la crida al LLM. Qwen interpreta la petició i retorna un JSON amb els camps action, products, old_product i new_product.

Per exemple, si l'usuari escriu “añade huevos y harina”, el model pot retornar:
{
  "action": "add",
  "products": ["huevos", "harina"],
  "old_product": "",
  "new_product": ""
}

Python interpreta aquest resultat amb json.loads(), comprova que els camps siguin vàlids i els guarda a l'estat.

A continuació, la funció route_after_input() consulta el valor d'action:
def route_after_input(state: ShoppingState):
      action = state.get("action", "other")
      print(f"[ROUTER] {action}")
      return action

El router pot seleccionar els nodes add, remove, replace, show o other.

Cada node executa la funció Python corresponent, com add_products(), remove_products(), replace_product() o show_products().

**Flux d'execució:**
Entrada de l'usuari: la funció main() rep el missatge i inicia el graf amb shopping_graph.invoke().
Interpretació del LLM: LangGraph executa process_input_node(), que crida Qwen mitjançant llm.invoke(). El model identifica la intenció de l'usuari i genera una resposta JSON.
Processament del JSON: Python executa json.loads(), valida els camps i actualitza l'estat compartit.
Selecció del node: LangGraph executa route_after_input(), que consulta el camp action i retorna el nom del node que s'ha d'executar. Aquesta decisió es basa en el valor del JSON i no requereix una nova inferència.
Execució de l'operació: el node seleccionat executa una funció Python. Per exemple, add_node() invoca add_products(), que afegeix els productes a la llista.
Actualització de l'estat: la funció retorna la llista actualitzada i un missatge de confirmació. LangGraph guarda els resultats a l'estat i finalitza l'execució.
Resposta final: Python mostra la resposta i el contingut real de la llista al terminal, sense necessitat de tornar a consultar el LLM.

Per tant, en aquest exemple Qwen decideix què vol fer l'usuari, el router determina quin node executar i Python realitza l'operació.

Aquesta arquitectura és diferent de 06_shopping_list.py, on el LLM utilitzava directament el mecanisme de tool calling de LangChain. Aquí la decisió es transforma primer en JSON i després és LangGraph qui controla explícitament el recorregut.

**Figura 17. Flux d’execució amb LangGraph**

Aquest exemple permet entendre la diferència entre la decisió del model i l'encaminament del graf, així com el paper dels nodes i de l'estat compartit.

Execució: python 07_shopping_list_langgraph.py

### 8.9. 08_shopping_list_weaviate.py
Aquest exemple amplia l'assistent de llista de la compra incorporant una connexió amb Weaviate Cloud, una base de dades vectorial que permet recuperar informació mitjançant cerques semàntiques.

L'aplicació continua permetent gestionar productes, però incorpora la possibilitat de buscar receptes i afegir els seus ingredients a la llista de la compra. La informació es treu de la col·lecció Recetas de Weaviate.

**Components del codi:**
El programa utilitza dos objectes ChatOllama amb finalitats diferents:
llm = ChatOllama(
    model="qwen3.5:9b",
    temperature=0,
    format="json",
    reasoning=False,
)

rag_llm = ChatOllama(
    model="qwen3.5:9b",
    temperature=0,
    reasoning=False,
)

Tots dos utilitzen el mateix model, però es configuren per a dues tasques diferents.El primer objecte (llm) interpreta les peticions de l'usuari i genera una estructura JSON. El segon (rag_llm) genera explicacions en llenguatge natural a partir de les receptes recuperades.

El programa incorpora la funció weaviate_connection(), que prepara la connexió amb Weaviate Cloud. Per consultar les receptes, search_recipes() executa una cerca semàntica amb: result = collection.query.near_text(**kwargs). Aquesta operació permet recuperar receptes relacionades amb el significat de la consulta, encara que no continguin exactament les mateixes paraules.

El programa també aplica condicions addicionals. Si l'usuari estableix un temps màxim, s'incorpora un filtre sobre tiempoMin (temps en minuts). Posteriorment, Python executa has_required_ingredients() per comprovar que les receptes continguin tots els ingredients obligatoris. Per tant, es combina una cerca vectorial a Weaviate amb comprovacions exactes programades en Python.

**Flux d'execució:**
Suposem que l'usuari introdueix: “Quiero recetas con huevos y patatas que se preparen en menos de 30 minutos.”

El flux seria el següent:
Entrada de l'usuari: Python rep el missatge i inicia el graf de LangGraph.
Primera inferència del LLM: process_input_node() envia la petició a Qwen, que identifica l'acció search_recipe, genera una consulta semàntica i extreu els filtres. El JSON pot contenir required_ingredients=["huevos", "patatas"] i max_minutes=30.
Selecció de la ruta: Python interpreta el JSON i el router selecciona search_recipe_node().
Consulta a Weaviate: el node executa search_recipes(). Aquesta funció obre una connexió amb weaviate Cloud i realitza la cerca amb near_text(), aplicant el filtre de temps.
Filtratge amb Python: el programa examina les receptes recuperades i comprova amb has_required_ingredients() que continguin tots els ingredients obligatoris.
Segona inferència del LLM: si s'han trobat receptes, search_recipe_node() prepara un prompt amb la pregunta original i les dades recuperades. Després executa rag_llm.invoke() perquè Qwen generi una explicació basada en aquestes receptes.
Resposta final: LangGraph guarda les receptes a last_recipes i Python mostra al terminal els resultats numerats i l'explicació generada.

Aquesta segona inferència és un exemple de RAG (Retrieval-Augmented Generation), ja que el model genera la resposta utilitzant informació recuperada d'una font externa.

El procés també permet una altra interacció. Si l'usuari escriu “añade los ingredientes de la segunda receta”, el primer LLM interpreta l'acció add_recipe i identifica el número de recepta.

En aquest cas, add_recipe_node() recupera la segona recepta de last_recipes, extreu els ingredients de ingredientesClave i executa add_products() per actualitzar la llista. No cal repetir la cerca a weaviate ni executar el segon LLM per generar una nova explicació.

Així, el primer LLM interpreta les instruccions, Weaviate proporciona les dades, Python aplica els filtres i modifica la llista, i el segon LLM explica les receptes recuperades.

**Figura 18. Flux d’execució afegint weaviate**

Aquest exemple mostra com integrar una base de dades vectorial amb un assistent basat en LLM per respondre consultes utilitzant informació externa al model.

Execució: python 08_shopping_list_weaviate.py

### 8.10. 09_shopping_list_weaviate_opik.py
Aquest exemple incorpora Opik a l'assistent de llista de la compra amb Weaviate. L'objectiu és afegir observabilitat, és a dir, la capacitat de registrar i analitzar les diferents operacions que es produeixen durant una execució.

El funcionament principal de l'assistent es manté com en l'exemple anterior, però ara és possible observar les crides al LLM, les consultes a Weaviate, els temps d'execució i les mètriques de consum disponibles.

**Components del codi:**
El programa incorpora OpikTracer i track_langgraph(), que permeten instrumentar el graf de LangGraph.

També defineix una funció per registrar el consum del model:
@track(
    name="ollama_tokens",
    type="llm",
    capture_input=False,
    capture_output=False
)
def invoke_with_opik_usage(
    model,
    messages,
    etapa: str
):
    answer = model.invoke(messages)
    usage = answer.usage_metadata or {}
    if usage:
        opik_context.update_current_span(
            model=MODEL,
            provider="ollama",
            metadata={"etapa": etapa},
            usage={
                "prompt_tokens":
                    usage.get("input_tokens", 0),
                "completion_tokens":
                    usage.get("output_tokens", 0),
                "total_tokens":
                    usage.get("total_tokens", 0),
            },
        )

    return answer

Així, si cliquem una trace al dashboard veurem el següent:

**Figura 19. Consum de tokens**
Aquesta funció executa el model i recupera les metadades de consum proporcionades per Ollama. Els tokens es poden diferenciar entre els utilitzats per processar l'entrada i els generats a la sortida.

També s'utilitza la funció weaviate_near_text() per registrar les consultes semàntiques a la base de dades.

La integració amb LangGraph es realitza mitjançant:
shopping_graph = track_langgraph(
    shopping_graph,
    opik_tracer
)

Això permet associar les execucions del graf amb les traces registrades a Opik.

**Flux d’execució:**
Entrada de l'usuari: Python rep la petició i inicia el graf LangGraph instrumentat amb Opik.
Interpretació del LLM: process_input_node() executa Qwen a través de invoke_with_opik_usage(). El model genera el JSON amb l'acció corresponent, mentre que Opik registra les metadades de la invocació.
Selecció del node: LangGraph utilitza el router per determinar l'operació necessària. Opik permet observar el recorregut del graf i els components instrumentats.
Execució de les eines: si l'usuari sol·licita receptes, Python executa la consulta a Weaviate. weaviate_near_text() permet registrar aquesta operació i el seu temps d'execució.
Generació RAG: quan hi ha receptes recuperades, el programa executa el segon LLM mitjançant invoke_with_opik_usage(), indicant l'etapa generacion_rag.
Resposta final: Python mostra les receptes i l'explicació generada. Paral·lelament, Opik disposa de les traces que permeten analitzar les operacions registrades.
Finalització: quan es tanca el programa, opik_tracer.flush() envia les traces pendents a Opik i el codi intenta tancar les connexions HTTP d'Ollama.

La diferència principal és que Opik no intervé en la interpretació de la pregunta ni en la selecció de les eines. El seu paper és observar i registrar el funcionament de l'aplicació.

A partir de les traces es pot estudiar, per exemple, si el temps total d'una consulta prové principalment de la primera inferència de Qwen, de la cerca a Weaviate o de la generació de la resposta RAG. Les mètriques de tokens es registren quan Ollama proporciona les metadades corresponents.

**Figura 20. Flux d'execució afegint opik**

### 8.11. 10_shopping_list_weaviate_opik_hermes.py
Aquest exemple amplia l'assistent de llista de la compra desenvolupat anteriorment incorporant Hermes, un assistent d'intel·ligència artificial que s'utilitza per generar una planificació setmanal d'àpats a partir de receptes reals emmagatzemades a Weaviate.

L'aplicació manté les funcionalitats dels exemples anteriors, com gestionar la llista de la compra, buscar receptes a Weaviate i registrar les execucions amb Opik. La principal novetat és que ara també permet planificar els dinars i sopars de la setmana, identificar els ingredients necessaris i afegir a la llista de la compra els productes que encara no hi apareixen.

En aquest exemple es combinen diferents components amb responsabilitats específiques. Qwen interpreta les peticions de l'usuari, LangGraph organitza el flux d'execució, Weaviate proporciona les receptes, Hermes proposa la distribució del menú setmanal i Python s'encarrega de validar els resultats i gestionar la llista de la compra. A més, s'incorporen comprovacions Python per interpretar determinades peticions contextuals sense necessitat de consultar sempre el LLM.

**Components del codi:**
Configuració d'Ollama i Hermes
El programa continua utilitzant dos objectes ChatOllama, igual que en l'exemple anterior (llm i rag_llm). El primer LLM interpreta les peticions de l'usuari i determina l'acció que s'ha d'executar. El segon s'utilitza per generar les explicacions de les receptes recuperades mitjançant RAG.

Hermes, en canvi, s'integra d'una manera diferent. No es crida mitjançant ChatOllama, sinó que s'executa com un procés extern a través de la seva interfície de línia d'ordres (CLI). Això significa que el model utilitzat internament per Hermes depèn de la seva pròpia configuració i no ha de coincidir necessàriament amb el model Qwen configurat a Ollama.

Els principals paràmetres són:
COLLECTION = "Recetas"

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3.5:9b"
)

THREAD_ID = "shopping-session-hermes"

HERMES_TIMEOUT = int(
    os.getenv("HERMES_TIMEOUT", "240")
)

DAYS = (
    "lunes", "martes", "miércoles",
    "jueves", "viernes", "sábado", "domingo"
)

MEALS = ("comida", "cena")

HERMES_TIMEOUT estableix el temps màxim que el programa espera una resposta del procés Hermes. Per defecte, aquest límit és de 240 segons. També es defineix un identificador de sessió diferent de l'utilitzat a l'exemple anterior, per evitar que els estats de les dues aplicacions es barregin.

Ampliació de ShoppingState
L'estat compartit de LangGraph s'amplia amb nous camps:
class ShoppingState(TypedDict, total=False):
    user_input: str
    shopping_list: list[str]
    last_product: str
    last_recipes: list[dict]

    action: str
    products: list[str]

    search_query: str
    required_ingredients: list[str]
    max_minutes: int

    meal_type: str
    weekly_plan: dict
    last_shown_products: list[str]
    last_context: str

    response: str

Les noves variables són:
meal_type: indica si es volen planificar únicament dinars (comida), sopars (cena) o tots dos.
weekly_plan: emmagatzema el menú setmanal generat.
max_minutes: permet restringir la planificació a receptes que compleixin un temps màxim de preparació.
last_shown_products: guarda els ingredients pendents que s'han mostrat a l'usuari.
last_context: identifica l'últim context de la conversa, com ara el menú setmanal, els ingredients pendents, les receptes o la llista de la compra.

Aquestes dues últimes variables permeten gestionar millor les referències a missatges anteriors. Per exemple, si el programa mostra els ingredients que falten per preparar el menú i posteriorment l'usuari escriu “añade estos productos”, Python pot recuperar exactament els ingredients mostrats sense haver de tornar-los a identificar mitjançant el LLM.

El programa continua utilitzant InMemorySaver per conservar l'estat entre les interaccions d'una mateixa sessió.

Nous nodes de LangGraph
S'incorporen tres accions principals:
plan_week_node(): genera el menú setmanal utilitzant Weaviate i Hermes.
missing_ingredients_node(): identifica els ingredients del menú que encara no apareixen a la llista de la compra.
add_missing_node(): afegeix els ingredients pendents quan l'usuari ho sol·licita expressament.

Aquestes accions s'afegeixen a les que ja existien per gestionar productes i buscar receptes. Per tant, LangGraph continua utilitzant el mateix mecanisme de process_input_node() i route_after_input(), però ara disposa d’aquestes tres noves rutes.

Recuperació de receptes amb Weaviate:
Abans de generar el menú, el programa necessita obtenir les receptes que Hermes podrà seleccionar. Per fer-ho, s'utilitza la funció:
@track(
    name="weekly_weaviate_candidates",
    type="tool",
    capture_input=False,
    capture_output=False
)
def retrieve_week_candidates(
    query: str,
    max_minutes: int = 0,
    user_input: str = ""
) -> list[dict]:

Aquesta funció es connecta a la col·lecció Recetas de Weaviate i executa una cerca semàntica (utilitzant near_text()).

A diferència de search_recipes(), que retorna com a màxim cinc receptes, aquesta funció també utilitza fetch_objects(limit=100) per recuperar altres receptes de la col·lecció que podrien no aparèixer entre els primers resultats de la cerca semàntica. Posteriorment, Python combina els resultats i prepara fins a 45 receptes candidates vàlides. Això permet disposar de més opcions per construir un menú setmanal de fins a 14 plats (set dinars i set sopars).

Posteriorment, Python aplica diferents comprovacions (utilitzant eligible_week_recipe()):
Descarta receptes que no disposen d'ingredients estructurats a ingredientesClave.
Comprova que compleixin el temps màxim indicat.
Elimina receptes duplicades.
Assigna identificadors com R01, R02, R03, etc.

Per exemple, si l'usuari demana «planifica cenas de menos de 20 minutos», Python identifica que la condició és estrictament inferior a 20 minuts i estableix max_minutes=19. D'aquesta manera, la validació no depèn únicament de la interpretació del LLM.

Planificació setmanal amb Hermes:
La funció principal encarregada de comunicar-se amb Hermes és:
@track(
    name="hermes_weekly_planning",
    type="llm",
    capture_input=False,
    capture_output=False
)
def ask_hermes_for_week(
    user_input: str,
    candidates: list[dict],
    meal_type: str
) -> dict:

Aquesta funció rep la petició original de l'usuari, les receptes candidates recuperades de Weaviate i el tipus d'àpats que s'han de planificar.

Primer es prepara una versió simplificada de les receptes. ​​Aquesta informació s'incorpora al prompt que es proporcionarà a Hermes. El prompt indica que ha de generar un menú de set dies, utilitzant únicament les referències de les receptes proporcionades i sense inventar plats. Hermes ha de retornar preferentment set línies de text, una per cada dia.

Per exemple, una possible resposta per planificar únicament els sopars seria:
lunes: cena=R03
martes: cena=R01
miércoles: cena=R07
jueves: cena=R04
viernes: cena=R02
sábado: cena=R06
domingo: cena=R05

Els identificadors són referències a receptes recuperades prèviament de Weaviate. El prompt també indica a Hermes que ha de prioritzar les categories adequades per a cada àpat i intentar variar els plats sense repetir-los innecessàriament.

Per executar Hermes, Python utilitza subprocess.run():
result = subprocess.run(
                ["hermes", "-z", prompt, "--toolsets", "search",
                 "--usage-file", str(usage_path)],
                capture_output=True, text=True, timeout=HERMES_TIMEOUT,
                check=False, env=env,
            )

La crida executa Hermes en mode no interactiu amb -z, proporciona el prompt i recupera la resposta generada. El paràmetre --usage-file permet guardar informació del consum de tokens quan Hermes la proporciona.

El programa limita les eines habilitades al conjunt search, excloent els conjunts d'eines de terminal, fitxers i MCP. Tot i això, les eines de cerca poden continuar disponibles, i el mode no interactiu pot aprovar automàticament les eines habilitades. Per aquesta raó també s'indica al prompt que no executi eines.

Validació del menú amb Python:
Una vegada Hermes retorna la planificació, el programa executa:
plan, completed = build_verified_plan(
    raw,
    candidates,
    meal_type,
    minute_limit,
    state["user_input"]
)

Aquesta funció és important perquè el programa no accepta directament qualsevol recepta proposada per Hermes. Python comprova que les referències retornades corresponguin a receptes reals recuperades de Weaviate i que compleixin els filtres establerts. També comprova que les receptes siguin adequades com a plats principals, que compleixin les restriccions de dieta i temps i que no es repeteixin innecessàriament quan existeixen altres opcions disponibles.

Si Hermes retorna una referència incorrecta, omet algun dia o no proporciona una selecció vàlida, Python pot completar les posicions del menú utilitzant receptes candidates que sí que han estat validades. D'aquesta manera, el sistema evita incorporar plats inexistents o receptes que no compleixen el límit de temps.

El programa pot generar un menú alternatiu encara que Hermes falli. Si la invocació de Hermes genera un error, supera el temps màxim o no proporciona una resposta aprofitable, Python pot construir la planificació utilitzant directament les receptes vàlides de Weaviate. En aquest cas, el programa mostra un avís indicant que el menú ha estat seleccionat automàticament o corregit per Python. En canvi, si no existeixen receptes candidates que compleixin els requisits de l'usuari, no es pot construir un menú vàlid i el programa informa d'aquesta situació.

Aquesta separació permet diferenciar dues responsabilitats. Es pot veure clarament que Hermes proposa la planificació, però Python verifica i construeix el resultat definitiu.

Comprovació dels ingredients del menú:
Una vegada generat el menú setmanal, el programa pot identificar quins ingredients són necessaris per preparar-lo.

Aquesta operació es realitza amb:
@track(
    name="calculate_missing_ingredients",
    type="tool",
    capture_input=False,
    capture_output=False
)
def calculate_missing_ingredients(
    plan: dict,
    shopping_list: list[str]
) -> dict:

La funció recorre les receptes assignades als diferents dies de la setmana, extreu els seus ingredientesClave i elimina els duplicats. Posteriorment, compara aquests ingredients amb els productes que ja apareixen a shopping_list. Per exemple, si el menú necessita ous, llet, arròs i patates, però la llista de la compra ja conté llet i ous, Python identifica arròs i patates com a productes pendents.

És important remarcar que aquesta comprovació no determina quins aliments té realment l'usuari a casa. Únicament compara els ingredients del menú amb els productes que ja estan apuntats a la llista de la compra. Tampoc no calcula les quantitats totals necessàries, ja que treballa amb els ingredients principals de cada recepta.

El node missing_ingredients_node() permet consultar aquests productes sense modificar la llista. També guarda els estats per quan l'usuari demana posteriorment “añade estos productos”, el programa pot recuperar exactament els ingredients que acaba de mostrar. En canvi, add_missing_node() només executa add_products() quan l'usuari demana explícitament afegir-los. Així, consultar els ingredients pendents no provoca automàticament cap modificació de la llista.

**Flux d'execució:**
Suposem que l'usuari introdueix: “Planifica las comidas y cenas de esta semana, con recetas de menos de 30 minutos.”

El procés és el següent:
Entrada de l'usuari: Python rep el missatge i inicia el graf amb shopping_graph.invoke().
Interpretació de la petició: process_input_node() comprova primer si existeix una acció contextual identificable amb contextual_menu_action(). Si no n'hi ha, envia la petició a Qwen mitjançant invoke_with_opik_usage(). El model identifica l'acció plan_week, el tipus d'àpats (ambas), la consulta de receptes i el temps màxim.
Selecció de la ruta: route_after_input() consulta el valor action i selecciona plan_week_node(). Aquesta operació és una decisió programada en Python.
Recuperació de receptes: plan_week_node() executa retrieve_week_candidates(), que consulta Weaviate i prepara fins a 45 receptes candidates, comprovant els filtres de categoria, dieta i temps, i assignant-ne les referències.
Invocació de Hermes: Python executa ask_hermes_for_week(). Aquesta funció construeix el prompt amb les receptes disponibles i inicia Hermes CLI mitjançant subprocess.run().
Generació i interpretació del menú: Hermes processa les instruccions i retorna una proposta de planificació, preferentment en set línies de text. Posteriorment, parse_hermes_selection() interpreta la resposta i la transforma en una estructura que Python pugui utilitzar.
Validació amb Python: build_verified_plan() comprova que totes les seleccions corresponguin a receptes reals i vàlides. Si falten posicions o hi ha seleccions incorrectes, les completa o corregeix amb receptes verificades. Si Hermes falla, també pot construir un menú alternatiu.
Comprovació d'ingredients: calculate_missing_ingredients() recorre el menú i compara els ingredients necessaris amb els productes presents a la llista de la compra.
Generació de l'informe: format_week() prepara el menú setmanal. Python també incorpora un resum del nombre d'ingredients diferents i dels que encara no apareixen a la llista.
Resposta final: LangGraph guarda el menú a weekly_plan, actualitza el context de la conversa i Python mostra el resultat al terminal.

Si posteriorment l'usuari pregunta “¿Qué productos me faltan para preparar el menú?”, Qwen interpreta l'acció missing_ingredients i LangGraph selecciona el node corresponent, que calcula els ingredients pendents i els guarda a last_shown_products. En aquesta segona petició no cal executar Hermes ni tornar a consultar Weaviate, perquè el menú ja està emmagatzemat a l'estat.

Finalment, si l'usuari escriu “Añade los ingredientes que faltan a mi lista”, LangGraph executa add_missing_node(), que utilitza la funció Python add_products().

**Figura 21. Flux d’execució afegint hermes**

Integració amb Opik:
El programa manté la integració amb Opik desenvolupada en l'exemple anterior. Les inferències amb Qwen, les consultes a Weaviate i les execucions dels nodes de LangGraph continuen registrant-se mitjançant traces.

A més, s'incorporen spans específics per a les noves funcionalitats:
weekly_weaviate_candidates: recuperació de receptes candidates per al menú.
weaviate_near_text: cerca semàntica a Weaviate.
hermes_weekly_planning: invocació de Hermes CLI per generar la planificació.
calculate_missing_ingredients: comparació dels ingredients del menú amb la llista de la compra.

Per registrar el consum de Hermes, el programa utilitza el fitxer JSON de mètriques generat mitjançant --usage-file. Quan aquest fitxer conté dades de consum, Python incorpora al span d'Opik els tokens d'entrada, els tokens de sortida i el total. Això permet comparar les operacions realitzades per Qwen amb la inferència de planificació executada mitjançant Hermes.
