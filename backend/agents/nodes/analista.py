from backend.agents.state import AgentState


def analista_node(state: AgentState) -> AgentState:
    # Placeholder: análisis estadístico/ML/LLM
    return {**state, "analysis": state.get("analysis")}

