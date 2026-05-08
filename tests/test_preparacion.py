import pandas as pd

from backend.agents.nodes.preparacion import preparacion_node


def test_preparacion_node_limpia_datos():
    raw_data = [
        {" CODIGO ": "001", "Departamento": "BOYACA", "Numero Personas": "123"},
        {" CODIGO ": "001", "Departamento": "BOYACA", "Numero Personas": "123"},
        {" CODIGO ": "002", "Departamento": "CUNDINAMARCA", "Numero Personas": "456"},
    ]

    estado_inicial = {
        "query": "test",
        "dataset_id": "test-id",
        "data": raw_data,
        "insights": [],
        "alerts": [],
    }

    resultado = preparacion_node(estado_inicial)
    df = resultado["data"]

    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(df.drop_duplicates())
    assert "codigo" in df.columns
    assert "departamento" in df.columns
    assert "numero_personas" in df.columns
    assert pd.api.types.is_numeric_dtype(df["numero_personas"])
