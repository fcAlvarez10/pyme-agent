"""Configuration for the Marketing Campaign Agent."""

import os
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field


class Configuration(BaseModel):
    """Runtime-configurable parameters for the agent.

    These appear in the LangGraph Studio UI.
    """

    model_name: str = Field(
        default="gemini-2.5-flash",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "gemini-2.5-flash",
                "description": "Vertex AI model for generating campaign proposals.",
            }
        },
    )
    temperature: float = Field(
        default=0.2,
        metadata={
            "x_oap_ui_config": {
                "type": "slider",
                "default": 0.2,
                "min": 0.0,
                "max": 2.0,
                "step": 0.1,
                "description": "Temperature for the LLM.",
            }
        },
    )
    mcp_server_url: str = Field(
        default="http://127.0.0.1:8001/sse",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "http://127.0.0.1:8001/sse",
                "description": "URL of the MCP sales data server.",
            }
        },
    )
    a2a_agent_url: str = Field(
        default="http://127.0.0.1:8000",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "http://127.0.0.1:8000",
                "description": "URL of the A2A Agency agent.",
            }
        },
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None,
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = config.get("configurable", {}) if config else {}
        field_names = list(cls.model_fields.keys())
        values: dict[str, Any] = {
            field_name: os.environ.get(field_name.upper(), configurable.get(field_name))
            for field_name in field_names
        }
        return cls(**{k: v for k, v in values.items() if v is not None})
