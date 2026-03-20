# Arquitectura Avanzada de Agentes de IA: Caso "Calzados La Sabana S.A.S."

Este repositorio contiene la demostración técnica del caso de uso "Calzados de Cuero La Sabana S.A.S.", una PYME bogotana. El objetivo es ilustrar de manera práctica y auditable cómo se construye un sistema autónomo real, alejándonos del concepto de "caja negra" y entrando al detalle del código de implementación.

---

## Tabla de Contenido

1. [El Reto de Negocio: Un "Empleado Digital" para Cualquier PYME](#1-el-reto-de-negocio-un-empleado-digital-para-cualquier-pyme)
2. [El Marco Teórico: Los 7 Pilares de la IA Agéntica](#2-el-marco-teórico-los-7-pilares-de-la-ia-agéntica)
3. [La Metodología: Stack Tecnológico y Construcción](#3-la-metodología-stack-tecnológico-y-construcción)
4. [Del Concepto al Código: Implementación en Calzados La Sabana](#4-del-concepto-al-código-implementación-en-calzados-la-sabana)
5. [Guía Rápida de Despliegue](#5-guía-rápida-de-despliegue)

---

## 1. El Reto de Negocio: Un "Empleado Digital" para Cualquier PYME

Antes de profundizar en la arquitectura y el código, es fundamental entender qué problema de negocio estamos resolviendo. Aunque este repositorio está configurado específicamente para una fábrica de calzado, el potencial de este sistema es transversal a cualquier industria.

**El Reto Universal:** Toda pequeña y mediana empresa sufre del mismo cuello de botella operativo. Dueños y equipos pequeños pierden horas en tareas repetitivas y fragmentadas: cruzar tablas de inventario, calcular presupuestos manuales, redactar correos o campañas repetitivas y coordinar tareas con proveedores externos.

**La Solución (El Producto):** Hemos construido un "Sistema Operativo Agéntico" donde el humano actúa estrictamente como director y la IA como un Ejecutivo Operativo Autónomo. El objetivo es que, con una simple orden en lenguaje natural (ej. *"Lanza la campaña del mes"*), el agente pueda orquestar un flujo multidisciplinario de principio a fin. 

En nuestra demostración, el agente será capaz de:
*   **Analizar la realidad:** Leer la base de datos de la empresa para encontrar qué producto necesita rotación urgente.
*   **Respetar la identidad corporativa:** Redactar contenido basándose en un archivo de memoria que le exige un tono de voz específico (por ejemplo, orgullo nacional, sin anglicismos).
*   **Cuidar la rentabilidad:** Calcular matemáticas financieras y presupuestos. Si intenta ejecutar una acción que genera pérdidas o viola reglas, el sistema interno lo rechaza y la IA se corrige a sí misma.
*   **Delegar el trabajo:** Tras pedir una aprobación de seguridad al humano, el agente subcontrata a otra Inteligencia Artificial (una agencia de publicidad externa) para que ejecute la pauta.

**La Escalabilidad Real:** El código de este repositorio es 100% agnóstico. Simplemente cambiando el archivo local de memoria y apuntando el servidor de datos a otra fuente, este mismo código se transforma instantáneamente en un analista de seguros, un coordinador logístico o un gestor de atención al paciente, demostrando que el desarrollo de agentes es la nueva frontera del software empresarial.

> *Para construir este empleado digital de forma robusta y no como un simple script frágil, necesitamos apoyarnos en la teoría moderna de sistemas autónomos.*

---

## 2. El Marco Teórico: Los 7 Pilares de la IA Agéntica

Para entender cómo funciona nuestro sistema en el fondo, primero debemos definir el hilo conductor conceptual que separa a un simple chatbot conversacional de un agente verdaderamente autónomo. Estos son los 7 pilares sobre los que construimos:

1. **Fundamentos (Agentes Racionales):** Un agente deja de ser un oráculo pasivo de preguntas y respuestas; se convierte en una entidad capaz de percibir cualquier entorno y ejecutar secuencias de acciones con autonomía para maximizar una métrica de éxito.
2. **El Cerebro (Razonamiento Sys2):** El Modelo de Lenguaje (LLM) asume el rol de motor lógico (CPU), utilizando bucles deliberativos (como ReAct: Pensar, Actuar, Observar) para planificar y resolver problemas complejos paso a paso antes de dar una respuesta.
3. **Sistemas de Memoria:** La capacidad arquitectónica de retener información dinámica en el corto plazo (ventana de contexto o memoria de trabajo) y recuperar conocimiento estructurado en el largo plazo (memoria episódica) para evolucionar y mantener coherencia.
4. **Grounding y Herramientas (Tool Calling):** El mecanismo que otorga "manos y ojos" al agente, anclándolo a la realidad al permitirle interactuar universal y estandarizadamente (ej. mediante el Model Context Protocol) con una infinidad de integraciones: APIs, bases de datos o navegadores web.
5. **Reflexión y Autocorrección:** El bucle continuo de "Generar-Criticar-Corregir" que dota al agente de resiliencia, permitiéndole identificar excepciones del entorno o errores lógicos en tiempo real y recalcular su estrategia sin requerir ayuda humana.
6. **Orquestación Multi-Agente:** El diseño donde la complejidad se divide entre múltiples modelos especializados que colaboran mediante topologías de red (grafos, jerarquías) o se comunican de forma descentralizada a través de protocolos abiertos (Agent-to-Agent).
7. **Evaluación y Producción (Guardrails):** Las estrategias críticas para operar en el mundo real: mecanismos de seguridad perimetral (Human-in-the-loop) para pausas obligatorias, observabilidad profunda de cada "pensamiento", y el uso de otros LLMs como jueces evaluadores para medir el desempeño no-determinista.

> *Con la teoría clara, el siguiente paso es elegir las herramientas adecuadas del ecosistema actual de desarrollo para materializar estos pilares en software funcional.*

---

## 3. La Metodología: Stack Tecnológico y Construcción

Antes de ver la implementación específica, es vital entender el flujo de trabajo estándar que usa un ingeniero de IA para construir un ecosistema agéntico desde cero, utilizando herramientas de vanguardia.

### El Stack Tecnológico Base
*   **Orquestación:** LangGraph (para manejar la gestión de estado, los grafos de enrutamiento cíclico y la persistencia).
*   **Modelos y Abstracción:** LangChain como framework integrador y un Modelo de Lenguaje Fundacional (ej. Gemini, GPT, Claude) como el motor cognitivo.
*   **Protocolos Estándar:** MCP (Model Context Protocol) y frameworks como FastMCP para empaquetar bases de datos y lógica de negocio en servidores seguros y aislados.
*   **Observabilidad:** LangSmith o similares para la telemetría y el rastreo (tracing) de cada ejecución paso a paso.
*   **Gestión de Dependencias:** uv para un empaquetado y resolución de entornos virtuales extremadamente rápida en Python.

### El Paso a Paso: Cómo construir un Agente
Para desarrollar una arquitectura multi-agente de nivel empresarial, la metodología recomendada sigue estos 6 pasos:

1.  **Scaffolding e Inicialización:** Iniciar un proyecto estructurado usando plantillas oficiales (ej. langgraph-cli project create), configurando el entorno y las variables necesarias.
2.  **Definición del Cerebro y el Estado:** Diseñar la clase State (el esquema de variables que viajan entre los nodos) y programar el nodo de razonamiento principal que inyecta el System Prompt y se comunica con el LLM.
3.  **Aislamiento de Herramientas (Grounding):** En lugar de otorgar acceso directo a bases de datos en el código del LLM, se levanta un servidor backend que expone funciones estandarizadas (API o MCP). El agente descubre y se conecta a estas herramientas dinámicamente.
4.  **Inyección de Memoria y Checkpoints:** Configurar un almacén para el conocimiento a largo plazo (archivos locales, bases vectoriales) y activar un Checkpointer nativo (como SQLite o Postgres) en el orquestador para guardar la sesión paso a paso y permitir el Time-Travel (volver atrás en el tiempo).
5.  **Interrupciones y Colaboración:** Configurar nodos de parada (interrupt_before) para forzar la aprobación humana antes de acciones destructivas (Guardrails), y programar llamadas de red estructuradas para delegar tareas a agentes de otros dominios u organizaciones (Agent-to-Agent).
6.  **Observabilidad y Pruebas Continuas:** Activar el registro de trazas en la nube para debugear flujos complejos, y automatizar la calidad escribiendo scripts de integración que utilicen otros modelos LLM como jueces evaluadores para medir el cumplimiento estricto de las reglas.

> *Ya sabemos qué problema queremos resolver, qué teoría lo sustenta y qué herramientas usar. Ahora veamos exactamente cómo se programó esto paso a paso para la fábrica de calzado.*

---

## 4. Del Concepto al Código: Implementación en Calzados La Sabana

A continuación, mostramos cómo los 7 pilares descritos anteriormente se mapean e implementan de forma exacta en el código fuente de nuestro repositorio.

### Pilares I y II: Fundamentos y Razonamiento (El Cerebro ReAct)
**Teoría:** Instanciamos el pilar del cerebro usando un modelo analítico (System 2) dentro de un bucle de enrutamiento constante, permitiéndole ejercer racionalidad y decidir cuándo actuar y cuándo terminar.
**Implementación:** Todo esto se consolida en un Grafo Dirigido mediante LangGraph en [`src/agent/graph.py`](src/agent/graph.py). Observa el flujo condicional que orquesta el bucle de razonamiento:

```python
# Extracto de src/agent/graph.py
def route_after_model(state: AgentState) -> Literal["human_review", "execute_tools", "__end__"]:
    """Routing ReAct: Decide la siguiente acción tras el razonamiento del LLM."""
    last_message = state["messages"][-1]
    
    # Si no hay llamadas a herramientas (Action), el agente terminó su tarea
    if not last_message.tool_calls:
        return "__end__"
    
    # Evalúa el tipo de herramienta solicitada
    for tc in last_message.tool_calls:
        if tc["name"] == "send_to_agency":
            return "human_review" # Requiere aprobación (Guardrail)
            
    # Ejecuta herramientas internas
    return "execute_tools"

# Construcción del Bucle ReAct
builder = StateGraph(AgentState, config_schema=Configuration)
builder.add_node("agent", call_model) # Nivel cognitivo (Pensamiento)
builder.add_node("execute_tools", call_tools) # Nivel de actuación
builder.add_edge("execute_tools", "agent") # Bucle de vuelta a la Observación
```

> `![Grafo de LangGraph Studio](docs/assets/grafo_agente.png)`

### Pilar III: Sistema de Memoria y Contexto
**Teoría:** Separamos la memoria activa de la histórica para hacer al agente eficiente.
**Implementación:** 
1.  **Memoria Episódica:** El agente extrae a largo plazo las preferencias del gerente desde un archivo JSON local (`memory.json`) usando el servidor backend en [`src/mcp_server.py`](src/mcp_server.py):
    ```python
    @mcp.tool()
    def get_manager_preferences() -> str:
        """Extrae la memoria episódica: reglas de marca y preferencias."""
        memory_path = get_memory_path() # Lee memory.json
        with open(memory_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data)
    ```
2.  **Memoria de Trabajo (Checkpointer):** Para la memoria a corto plazo, LangGraph Studio inyecta automáticamente un Checkpointer (base de datos SQLite). Esto guarda la sesión completa (el `AgentState`), permitiendo el Time-Travel y la reanudación de hilos ante interrupciones.

### Pilar IV: Grounding y Herramientas (MCP)
**Teoría:** Por seguridad, no inyectamos la conexión de base de datos directamente en el código del LLM. Utilizamos el estándar de la industria Model Context Protocol (MCP) para separar el cerebro de las herramientas.
**Implementación:** En [`src/agent/graph.py`](src/agent/graph.py), el agente usa el cliente MCP para conectarse vía Server-Sent Events (SSE) a un proceso completamente aislado que alberga `pyme.db`.
```python
# Extracto de src/agent/graph.py
async def get_all_tools(config: RunnableConfig):
    """Obtiene dinámicamente las herramientas expuestas por el Servidor MCP."""
    url = configurable.mcp_server_url # Ej: http://127.0.0.1:8001/sse
    
    client = MultiServerMCPClient({
        "pyme_backend": {
            "transport": "sse",
            "url": url,
        }
    })
    mcp_tools = await client.get_tools() # Descubre las herramientas de datos
    return mcp_tools + [send_to_agency]
```

### Pilar V: Reflexión y Autocorrección
**Teoría:** Un sistema resiliente no cae ante excepciones; las lee y se ajusta automáticamente.
**Implementación:** Si el agente pide más de 20% de descuento, el servidor MCP en [`src/mcp_server.py`](src/mcp_server.py) no lanza un error de código fatal, sino un texto descriptivo. El agente lee esta Observación, razona su equivocación, y vuelve a intentar la herramienta con 20%.
```python
# Extracto de src/mcp_server.py
@mcp.tool()
def calculate_budget(product_name: str, discount_percentage: float) -> str:
    """Calcula el presupuesto. Retorna feedback textual si viola política."""
    if discount_percentage > 20:
        # Esto dispara el mecanismo de Reflexión del Agente
        return (
            "Error de política corporativa: El descuento máximo permitido es del 20%. "
            f"Un descuento del {discount_percentage}% genera un margen negativo inaceptable para '{product_name}'. "
            "Reflexiona sobre tu estrategia y vuelve a llamar a la herramienta con un descuento válido."
        )
    # Lógica de aprobación...
```

### Pilar VI: Orquestación Multi-Agente y Protocolo A2A
**Teoría:** Para escalar la automatización más allá de las fronteras de una empresa, los agentes se delegan tareas entre sí mediante protocolos estándar de comunicación.
**Implementación:** Nuestro agente interno (`graph.py`) usa un llamado HTTP estructurado (Protocolo A2A) para delegar la planificación visual a un Agente Externo (`agency_agent.py`), demostrando colaboración inter-empresarial descentralizada.
```python
# Extracto de src/agent/graph.py
@tool
async def send_to_agency(product: str, text: str, discount: float, budget: float, config: RunnableConfig) -> str:
    """Envía la campaña vía protocolo A2A al agente de la agencia publicitaria externa."""
    client = await ClientFactory.connect(
        agent=configurable.a2a_agent_url, # Ej: http://127.0.0.1:8000
        client_config=ClientConfig(streaming=True, httpx_client=httpx.AsyncClient(timeout=60.0)),
    )
    message = create_text_message_object(content=f"Campaña: {product}...")
    async for event in client.send_message(message):
        # Recibe de vuelta los hashtags y el media mix calculados por la agencia
        pass 
```

### Pilar VII: Evaluación, Producción y Guardrails
**Teoría:** La seguridad operativa requiere pausas antes de gastar presupuesto. A su vez, medir un sistema estocástico (impredecible) requiere de otros LLMs para calificar objetivamente el desempeño.
**Implementación de Guardrails:** Detenemos el grafo explícitamente en [`src/agent/graph.py`](src/agent/graph.py) exigiendo que un humano valide.
```python
# El grafo se pausa en seco y espera la aprobación humana en LangGraph Studio
graph = builder.compile(
    interrupt_before=["human_review"],
    name="ReAct Marketing Agent",
)
```

> *(Nota para el presentador: Insertar captura de pantalla de la pausa de Human-in-the-loop en LangGraph Studio)*
> `![Human in the Loop](docs/assets/human_in_loop.png)`

**Implementación de Evaluación (LLM-as-a-judge):** En [`tests/test_accuracy_llm_as_judge.py`](tests/test_accuracy_llm_as_judge.py), delegamos el aseguramiento de calidad (QA) a un modelo de IA parametrizado como juez estricto.
```python
# Extracto de tests/test_accuracy_llm_as_judge.py
PROMPT_LLM_AS_JUDGE = """
Eres un juez experto evaluando a un Agente de Inteligencia Artificial.
Pregunta del usuario: {input}
Contexto de evaluación: {contexto_evaluador}
Salida del agente: {output}

Evalúa si el agente cumplió con las restricciones (corrigió descuento a <= 20%, tono bogotano, etc.).
Responde ÚNICAMENTE con un JSON con la estructura:
{"score": <0.0 a 1.0>, "comentario": "<tu explicación>"}
"""
```

> *(Nota para el presentador: Insertar captura del panel de trazas y evaluación de LangSmith)*
> `![LangSmith Traces](docs/assets/langsmith_traces.png)`

---

## 5. Guía Rápida de Despliegue

### Requisitos y Variables de Entorno
Crea un archivo `.env` en la raíz de la carpeta `prototipo_clase` con:
```bash
GOOGLE_CLOUD_PROJECT="tu_proyecto_de_gcp"
GOOGLE_CLOUD_LOCATION="us-central1"
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY="tu_api_key_de_langsmith"
LANGCHAIN_PROJECT="Pyme Agent Demo"
```

Dado que el agente utiliza `ChatVertexAI` para interactuar con la infraestructura empresarial de Google Cloud, **no se requiere una GOOGLE_API_KEY**. En su lugar, el entorno debe estar autenticado con GCP. Para estudiantes ejecutándolo localmente, deben instalar `gcloud` CLI y ejecutar:

```bash
gcloud auth application-default login
gcloud config set project tu_proyecto_de_gcp
```

### Instalación e Inicialización
Recomendamos usar `uv` para la gestión del proyecto. Instala las dependencias y genera la base de datos de ventas (el script creará `pyme.db` populando productos como botas industriales y zapatos formales):

```bash
# 1. Sincronizar el entorno virtual y dependencias
uv sync

# 2. Inicializar la base de datos local
uv run python setup_db.py
```

### Levantar el Ecosistema
Para correr la demostración completa, necesitas abrir tres terminales independientes en la raíz del proyecto:

**Terminal 1: El Backend Aislado (Servidor MCP)**
```bash
uv run python src/mcp_server.py
```

**Terminal 2: La Agencia de Publicidad (Agente Externo A2A)**
```bash
uv run python src/agency_agent.py
```

**Terminal 3: El Cerebro y UI (LangGraph Studio)**
```bash
langgraph dev
```
