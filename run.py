import argparse

from backend.agents.graph import build_graph
from backend.agents.nodes.ingesta import ingesta_node


DATASETS = {
    "afiliados": "hn4i-593p",
    "sivigila": "4hyg-wa9d",
    "ips": "ugc5-acjp",
}


def _build_estado_inicial(dataset_id: str) -> dict:
    return {
        "query": "Prueba de ejecución",
        "dataset_id": dataset_id,
        "data": None,
        "insights": [],
        "alerts": [],
    }


def _run_one(mode: str, alias: str, dataset_id: str, app=None) -> None:
    print(f"\n=== [run] Procesando dataset '{alias}' ({dataset_id}) ===")
    estado_inicial = _build_estado_inicial(dataset_id)

    if mode == "ingesta":
        resultado = ingesta_node(estado_inicial)
        data = resultado.get("data") or []
        print("[run] Éxito: ingesta ejecutada.")
        print(f"[run] Registros obtenidos: {len(data)}")
        if len(data) > 0:
            print("[run] Primer registro:")
            print(data[0])
        return

    app.invoke(estado_inicial)
    print(f"[run] Flujo completo terminado para '{alias}'.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner del sistema multiagente")
    parser.add_argument(
        "--mode",
        choices=["ingesta", "all"],
        default="ingesta",
        help="Ejecuta solo ingesta o el flujo completo",
    )
    parser.add_argument(
        "--dataset",
        choices=["afiliados", "sivigila", "ips", "all"],
        default="afiliados",
        help="Dataset a consultar (o 'all' para procesar los tres)",
    )
    args = parser.parse_args()

    if args.dataset == "all":
        targets = list(DATASETS.items())
    else:
        targets = [(args.dataset, DATASETS[args.dataset])]

    app = build_graph() if args.mode == "all" else None

    for alias, dataset_id in targets:
        try:
            _run_one(args.mode, alias, dataset_id, app=app)
        except Exception as exc:
            print(f"[run] Error procesando '{alias}' ({dataset_id}): {exc}")

    print("\n[run] Proceso finalizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
