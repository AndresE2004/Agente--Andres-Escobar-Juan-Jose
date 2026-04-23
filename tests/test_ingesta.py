from backend.agents.nodes.ingesta import ingesta_node


def test_ingesta_node_obtiene_datos():
    estado_inicial = {"query": "test", "data": None, "insights": [], "alerts": []}
    resultado = ingesta_node(estado_inicial)

    assert "data" in resultado
    assert isinstance(resultado["data"], list)
    assert len(resultado["data"]) > 0

