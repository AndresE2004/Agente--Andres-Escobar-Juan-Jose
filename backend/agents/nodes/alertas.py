from backend.agents.state import AgentState


def alertas_node(state: AgentState) -> AgentState:
    # Placeholder: reglas/umbral para alertas
    alerts = state.get("alerts") or []
    return {**state, "alerts": alerts}

