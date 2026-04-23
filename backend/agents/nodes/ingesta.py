from backend.agents.state import AgentState


def ingesta_node(state: AgentState) -> AgentState:
    # Placeholder: aquí se consumirían datos (Socrata / APIs / DB)
    return {**state, "data": state.get("data")}

