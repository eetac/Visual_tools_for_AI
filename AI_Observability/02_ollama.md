## 2. QUÈ ÉS OLLAMA?
Ollama és una eina de codi obert que permet descarregar, gestionar i executar LLMs directament en un ordinador. És compatible amb diferents famílies de models, com Qwen, Llama o Gemma i facilita la seva execució sense necessitat de dependre de serveis externs al núvol. Ollama no és un model d'intel·ligència artificial en si mateix, sinó el programari que s'encarrega de carregar els models i gestionar els recursos de càlcul necessaris per executar-los, aprofitant la CPU i, quan és compatible, la GPU de l'ordinador per accelerar la inferència.

Un dels principals avantatges d'Ollama és que permet executar models d'intel·ligència artificial de manera local, mantenint el control sobre les dades i sense costos per consulta. Un cop descarregats, els models es poden utilitzar sense connexió a Internet per realitzar tasques com generar text, respondre preguntes, analitzar codi o processar imatges, segons les capacitats de cada model. A més, Ollama proporciona una API local que facilita la integració dels models amb aplicacions Python, interfícies gràfiques i frameworks com LangChain o LangGraph, permetent desenvolupar aplicacions i agents d'intel·ligència artificial personalitzats.

## 3. INSTAL·LACIÓ I ÚS D’OLLAMA A macOS
### 3.1. COMPROVACIÓ DE LES CARACTERÍSTIQUES
Abans d’instal·lar Ollama es pot comprovar el processador i la memòria disponible.

Des del Terminal: 

```bash
system_profiler SPHardwareDataType
```

Apareixerà informació similar a:

**Figura 2. Informació del mac**

En alguns ordinadors Mac amb Apple Silicon (com M1, M2, M3, M4), Ollama pot utilitzar la GPU integrada del xip per accelerar l’execució dels models.

### 3.2. INSTAL·LAR OLLAMA
Obrir l’aplicació Terminal i executar: 

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Aquest script descarrega i instal·la Ollama a macOS i afegeix la comanda ollama al sistema.

En acabar, comprovar que s’ha instal·lat correctament: 
```bash
ollama --version
```

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
Per veure quins models estan actualment carrgats i també per mirar si el model és adequat pel nostre mac, en un altre terminal executem: 

```bash
ollama ps
```

Per terminal apareixerà una mena de taula amb informació rellevant:

**Figura 4. ollama ps**

El cas ideal és 100% GPU ja que indica que el model està utilitzant completament l’acceleració gràfica.

També es pot obrir Monitor d’Activitat → Memòria i comprovar la pressió de memòria.
Si la pressió es manté en verd i el sistema continua funcionant amb fluïdesa, el model és adequat.
Si  la pressió de memòria és groga o vermella, el Mac va molt lent o el model tarda excessivament convé utilitzar un model més petit o reduir el context.

### 3.8. PER ATURAR UN MODEL
Quan ja no necessitem fer més preguntes a un model, s’escriu: ollama stop qwen3.5:9b

Amb aquesta comanda, aturem el model. És a dir, no s’elimina del disc sinó que es descarrega de memòria, deixa d’utilitzar GPU i allibera recursos.

Per comprovar que s’ha aturat correctament: 

```bash
ollama ps 
```

(i ha de sortir buit)
