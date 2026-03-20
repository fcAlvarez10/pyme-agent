"""Graph definition for the Marketing Campaign Agent."""

import json
import logging
from typing import Literal

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_google_vertexai import ChatVertexAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode

from src.agent.config import Configuration
from src.agent.state import AgentState

logger = logging.getLogger(__name__)

# ── Local Tools (A2A) ────────────────────────────────────────────────────

@tool
async def send_to_agency(product: str, text: str, discount: float, budget: float, config: RunnableConfig) -> str:
    """
    Send the approved campaign to the external agency via A2A protocol.
    Use this tool ONLY when the campaign is completely ready and the budget is approved.
    """
    logger.info("Sending campaign to agency...")
    configurable = Configuration.from_runnable_config(config)
    
    import httpx
    from a2a.client import ClientConfig, ClientFactory
    from a2a.client.helpers import create_text_message_object
    
    try:
        # Aumentar el timeout porque el agente remoto usa un LLM y puede demorar en responder
        custom_client = httpx.AsyncClient(timeout=60.0)
        client = await ClientFactory.connect(
            agent=configurable.a2a_agent_url,
            client_config=ClientConfig(streaming=True, httpx_client=custom_client),
        )
        
        message_content = (
            f"Campaña: {product}\n"
            f"Presupuesto: ${budget}\n"
            f"Descuento: {discount}%\n"
            f"Texto: {text}"
        )
        message = create_text_message_object(content=message_content)
        
        final_responses = []
        
        def dump_event(obj):
            """Convierte cualquier evento A2A a un string garantizado mediante un dump profundo."""
            try:
                if hasattr(obj, "model_dump_json") and callable(getattr(obj, "model_dump_json")):
                    return obj.model_dump_json()
                if hasattr(obj, "json") and callable(getattr(obj, "json")):
                    return obj.json()
                return json.dumps(
                    obj, 
                    default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o),
                    ensure_ascii=False
                )
            except Exception:
                return str(obj)

        async for event in client.send_message(message):
            # Convertimos las tuplas a listas para poder hacerles el dump, 
            # ya que A2A emite la respuesta final como una tupla (Task, Event)
            obj_to_dump = list(event) if isinstance(event, tuple) else event
            event_str = dump_event(obj_to_dump)
            
            # Guardamos ABSOLUTAMENTE TODOS los eventos
            final_responses.append(event_str)
                
        if final_responses:
            combined = "\n---\n".join(final_responses)
            return (
                "Campaña enviada exitosamente. Aquí están TODOS los eventos devueltos por el agente de la agencia. "
                "Por favor revisa cuidadosamente estos datos, encuentra el mensaje de la agencia donde especifica el "
                f"Mix de Medios y los Hashtags generados, y preséntaselos de forma limpia al usuario:\n\n{combined}"
            )
            
        return "Campaña enviada exitosamente. No se recibió respuesta de la agencia."
    except Exception as e:
        logger.error("A2A error: %s", e)
        return f"Error conectando con la agencia: {e}"


# ── MCP Tools Helper ─────────────────────────────────────────────────────

async def get_all_tools(config: RunnableConfig):
    """Fetch tools from MCP server and combine with local tools."""
    configurable = Configuration.from_runnable_config(config)
    url = configurable.mcp_server_url
    
    try:
        # Configurar conexión SSE
        client = MultiServerMCPClient({
            "pyme_backend": {
                "transport": "sse",
                "url": url,
            }
        })
        mcp_tools = await client.get_tools()
        logger.info("Loaded %d tools from MCP", len(mcp_tools))
    except Exception as e:
        logger.warning("No se pudo conectar al MCP Server: %s", e)
        mcp_tools = []
        
    return mcp_tools + [send_to_agency]

# ── Nodes ────────────────────────────────────────────────────────────────

async def call_model(state: AgentState, config: RunnableConfig):
    """Call the LLM with all available tools."""
    logger.info("Agent: Razonando y decidiendo siguiente acción...")
    configurable = Configuration.from_runnable_config(config)
    
    llm = ChatVertexAI(
        model_name=configurable.model_name,
        temperature=configurable.temperature,
    )
    
    all_tools = await get_all_tools(config)
    llm_with_tools = llm.bind_tools(all_tools)
    
    # Asegurar que hay un mensaje de sistema
    messages = state.get("messages", [])
    if not any(isinstance(m, SystemMessage) for m in messages):
        sys_msg = SystemMessage(content=(
            "Eres el agente inteligente y autónomo de Calzados de Cuero La Sabana S.A.S., una PYME bogotana de confección y venta de zapatos y botas en cuero. "
            "Cuando el usuario te pida crear o preparar una campaña (sin necesidad de que te dé instrucciones paso a paso), "
            "DEBES ejecutar proactivamente el siguiente Procedimiento Operativo Estándar (SOP):\n\n"
            "Paso 1: Llama a la herramienta para obtener las preferencias del gerente.\n"
            "Paso 2: Llama a la herramienta de la base de datos de ventas y escoge el producto estratégico.\n"
            "Paso 3: Llama a la herramienta para calcular el presupuesto. "
            "Si la herramienta te devuelve un error por violar políticas de la empresa, reflexiona, corrige el valor y vuelve a intentarlo.\n"
            "Paso 4: Redacta un texto para la campaña que cumpla estrictamente con las preferencias del gerente.\n"
            "Paso 5: Llama a la herramienta para enviar la campaña a la agencia externa.\n\n"
            "IMPORTANTE: Cuando la herramienta de la agencia externa te devuelva el resultado, tu mensaje final hacia el usuario DEBE "
            "mostrar explícitamente la respuesta de la agencia, incluyendo el mix de medios y los hashtags que ellos generaron."
        ))
        messages = [sys_msg] + messages
    
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}


async def human_review(state: AgentState, config: RunnableConfig):
    """Pause point for human approval before sending to agency."""
    logger.info("Agent: Esperando aprobación humana para contactar agencia externa...")
    # Update UI state
    return {"human_approved": None}  # Resets or sets flag for UI


async def call_tools(state: AgentState, config: RunnableConfig):
    """Execute the tools requested by the LLM."""
    logger.info("Agent: Ejecutando herramienta(s)...")
    all_tools = await get_all_tools(config)
    tool_node = ToolNode(all_tools)
    result = await tool_node.ainvoke(state, config)
    
    # Optionally update UI state based on tool executed
    # This keeps the original state variables useful for UI observability
    updates = {"messages": result["messages"]}
    
    # Extract info for UI if needed
    for tc in state["messages"][-1].tool_calls:
        if tc["name"] == "calculate_budget":
            updates["budget"] = tc["args"].get("discount_percentage", 0) # Just an example update
            
    return updates

# ── Routing logic ────────────────────────────────────────────────────────

def route_after_model(state: AgentState) -> Literal["human_review", "execute_tools", "__end__"]:
    """Route based on LLM output."""
    last_message = state["messages"][-1]
    
    # Si no hay llamadas a herramientas, terminó
    if not last_message.tool_calls:
        return "__end__"
    
    # Si quiere enviar a la agencia, requerimos revisión humana
    for tc in last_message.tool_calls:
        if tc["name"] == "send_to_agency":
            return "human_review"
            
    # Para herramientas internas (MCP), ejecutamos directo
    return "execute_tools"

# ── Graph construction ───────────────────────────────────────────────────

builder = StateGraph(AgentState, config_schema=Configuration)

builder.add_node("agent", call_model)
builder.add_node("human_review", human_review)
builder.add_node("execute_tools", call_tools)

builder.add_edge(START, "agent")

# Enrutamiento condicional desde el agente
builder.add_conditional_edges(
    "agent",
    route_after_model,
)

# Después de la revisión humana, se ejecutan las herramientas (incluyendo send_to_agency)
builder.add_edge("human_review", "execute_tools")

# Después de ejecutar cualquier herramienta, volvemos al agente para que observe el resultado
builder.add_edge("execute_tools", "agent")

graph = builder.compile(
    interrupt_before=["human_review"],
    name="ReAct Marketing Agent",
)
