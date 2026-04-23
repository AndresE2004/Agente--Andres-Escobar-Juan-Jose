from backend.agents.state import AgentState


def insights_node(state: AgentState) -> AgentState:
    # Placeholder: generación de insights a partir de análisis
    insights = state.get("insights") or []
    return {**state, "insights": insights}

