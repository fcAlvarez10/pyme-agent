"""States for the Marketing Campaign Agent graph."""

from typing import Any, Dict, Optional

from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """State for the Marketing Campaign Agent.

    Central repository for all data passed between nodes.
    """

    # Data
    preferences: Optional[str]
    sales_data: Optional[str]
    budget: Optional[float]
    error_msg: Optional[str]
    campaign_proposal: Optional[Dict[str, Any]]

    # Human-in-the-loop
    human_approved: Optional[bool]

    # Output
    final_status: Optional[str]
