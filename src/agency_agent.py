import uvicorn
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AFastAPIApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import (
    AgentCard, AgentCapabilities, AgentSkill
)
from a2a.utils import new_agent_text_message, new_task

# --- Imports para el Agente Interno de la Agencia ---
from langchain_core.tools import tool
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# --- Tools de la Agencia ---
@tool
def calculate_media_mix(budget: float) -> str:
    """
    Calcula la distribución óptima del mix de medios (Media Mix) 
    para un presupuesto dado.
    """
    if budget < 100000:
        return "100% Instagram Reels / Ads"
    
    instagram_budget = budget * 0.6
    tiktok_budget = budget * 0.4
    return f"60% Instagram Ads (${instagram_budget:,.2f}), 40% TikTok Ads (${tiktok_budget:,.2f})"

@tool
def generate_hashtags(product: str) -> str:
    """Genera hashtags virales y creativos para un producto usando un LLM."""
    llm = ChatVertexAI(model_name="gemini-2.5-flash", temperature=0.7)
    prompt = f"Genera 5 hashtags virales, creativos y muy específicos para una campaña de marketing en Colombia sobre el producto de cuero 100% bogotano: '{product}'. Devuelve solo los hashtags separados por espacio."
    response = llm.invoke(prompt)
    return response.content.strip()


class AgencyAgentExecutor(AgentExecutor):
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ) -> None:
        message = context.message

        # Create or get task
        if not context.current_task:
            task = new_task(request=message)
        else:
            task = context.current_task

        updater = TaskUpdater(event_queue, task.id, context.context_id)

        # Process message
        if message and message.parts:
            text = message.parts[0].root.text
            print(f"\n[Agencia Externa] Recibida nueva solicitud (A2A Protocol):")
            print(f"{text}\n")
            
            try:
                # Instanciamos el Agente de la Agencia
                llm = ChatVertexAI(model_name="gemini-2.5-flash", temperature=0.1)
                
                # Creamos el grafo ReAct preconstruido con las herramientas de la agencia
                agency_graph = create_react_agent(
                    llm, 
                    tools=[calculate_media_mix, generate_hashtags]
                )
                
                system_prompt = (
                    "Eres el agente inteligente de una Agencia de Publicidad externa. "
                    "Acabas de recibir una solicitud de campaña de un cliente. "
                    "Tu tarea es analizar el texto recibido, extraer el presupuesto y el producto, "
                    "y utilizar tus herramientas para calcular el mix de medios y generar hashtags. "
                    "Finalmente, responde al cliente resumiendo qué se va a ejecutar, incluyendo el "
                    "mix de medios calculado y los hashtags. Sé muy profesional."
                )
                
                print("[Agencia Externa] Razonando y ejecutando herramientas locales...")
                
                # Ejecutamos el agente interno
                result_state = await agency_graph.ainvoke({
                    "messages": [
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=text)
                    ]
                })
                
                # Extraemos la respuesta final del LLM
                final_agent_response = result_state["messages"][-1].content
                print(f"[Agencia Externa] Respuesta final generada:\n{final_agent_response}\n")

                response = new_agent_text_message(
                    final_agent_response,
                    context.context_id,
                    task.id
                )
                await updater.complete(response)
                
            except Exception as e:
                print(f"[Agencia Externa] Error ejecutando agente interno: {e}")
                await updater.failed(
                    new_agent_text_message(
                        f"Error interno en la agencia: {e}",
                        context.context_id,
                        task.id
                    )
                )
        else:
            await updater.failed(
                new_agent_text_message(
                    "No se proporcionó información de campaña.",
                    context.context_id,
                    task.id
                )
            )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ) -> None:
        if context.current_task:
            updater = TaskUpdater(event_queue, context.current_task.id, context.context_id)
            await updater.cancel()

def create_agency_card() -> AgentCard:
    return AgentCard(
        name='Agencia Marketing',
        description='Agencia externa con agente de IA autónomo para pautar campañas',
        url='http://127.0.0.1:8000/a2a/v1',
        version='2.0.0',
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=False
        ),
        skills=[
            AgentSkill(
                id='pautar_campana',
                name='Pautar Campaña',
                description='Recibe información de campañas, planifica el mix de medios y la ejecuta',
                tags=['marketing', 'campaigns', 'agentic'],
                examples=['Lanzar campaña de descuento para Botas Industriales con presupuesto de $500000']
            )
        ]
    )

if __name__ == '__main__':
    agent_card = create_agency_card()
    task_store = InMemoryTaskStore()
    
    executor = AgencyAgentExecutor()
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=task_store
    )
    
    a2a_app = A2AFastAPIApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )
    app = a2a_app.build(rpc_url="/a2a/v1")

    uvicorn.run(app, host='127.0.0.1', port=8000)
