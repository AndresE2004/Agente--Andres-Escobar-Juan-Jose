from __future__ import annotations

from langgraph.graph import StateGraph

from backend.agents.nodes.alertas import alertas_node
from backend.agents.nodes.analista import analista_node
from backend.agents.nodes.ingesta import ingesta_node
from backend.agents.nodes.insights import insights_node
from backend.agents.nodes.preparacion import preparacion_node
from backend.agents.state import AgentState


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("ingesta", ingesta_node)
    g.add_node("preparacion", preparacion_node)
    g.add_node("analista", analista_node)
    g.add_node("insights", insights_node)
    g.add_node("alertas", alertas_node)

    g.set_entry_point("ingesta")
    g.add_edge("ingesta", "preparacion")
    g.add_edge("preparacion", "analista")
    g.add_edge("analista", "insights")
    g.add_edge("insights", "alertas")

    return g.compile()

