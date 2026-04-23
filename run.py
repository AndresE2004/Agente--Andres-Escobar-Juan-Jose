import argparse

from backend.agents.graph import build_graph
from backend.agents.nodes.ingesta import ingesta_node


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner del sistema multiagente")
    parser.add_argument(
        "--mode",
        choices=["ingesta", "all"],
        default="ingesta",
        help="Ejecuta solo ingesta o el flujo completo",
    )
    args = parser.parse_args()

    estado_inicial = {"query": "Prueba de ejecución", "data": None, "insights": [], "alerts": []}

    if args.mode == "ingesta":
        resultado = ingesta_node(estado_inicial)
        data = resultado.get("data") or []
        print("[run] Éxito: ingesta ejecutada.")
        print(f"[run] Registros obtenidos: {len(data)}")
        if len(data) > 0:
            print("[run] Primer registro:")
            print(data[0])
        return 0

    app = build_graph()
    app.invoke(estado_inicial)
    print("[run] Flujo completo terminado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

