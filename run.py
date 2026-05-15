import argparse
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from backend.agents.graph import build_graph
from backend.agents.nodes.analista import analista_node
from backend.agents.nodes.ingesta import ingesta_node
from backend.agents.nodes.preparacion import preparacion_node
from backend.core.storage import load_clean_data, load_raw_data


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


def _run_ingesta(estado: dict) -> dict:
    resultado = ingesta_node(estado)
    data = resultado.get("data") or []
    print("[run] Éxito: ingesta ejecutada.")
    print(f"[run] Registros obtenidos: {len(data)}")
    if len(data) > 0:
        print("[run] Primer registro:")
        print(data[0])
    return resultado


def _run_preparacion(estado: dict, dataset_id: str) -> dict:
    raw = load_raw_data(dataset_id)
    if raw:
        print(f"[run] Usando datos crudos guardados: data/raw/{dataset_id}.json")
        estado = {**estado, "data": raw}
    else:
        print("[run] No hay archivo crudo; ejecutando ingesta primero...")
        estado = ingesta_node(estado)
    return preparacion_node(estado)


def _run_analista(estado: dict, dataset_id: str) -> dict:
    df = load_clean_data(dataset_id)
    if df is not None:
        print(f"[run] Usando dataset limpio guardado: data/clean/{dataset_id}.csv")
        estado = {**estado, "data": df}
    else:
        print("[run] No hay CSV limpio; ejecutando ingesta y preparación primero...")
        estado = ingesta_node(estado)
        estado = preparacion_node(estado)
    return analista_node(estado)


def _run_one(mode: str, alias: str, dataset_id: str, app=None) -> None:
    print(f"\n=== [run] Procesando dataset '{alias}' ({dataset_id}) ===")
    estado_inicial = _build_estado_inicial(dataset_id)

    if mode == "ingesta":
        _run_ingesta(estado_inicial)
        return

    if mode == "preparacion":
        _run_preparacion(estado_inicial, dataset_id)
        print(f"[run] Sprint 2 completado para '{alias}'.")
        return

    if mode == "analista":
        resultado = _run_analista(estado_inicial, dataset_id)
        analysis = resultado.get("analysis") or {}
        print(f"[run] Sprint 3 completado para '{alias}'.")
        print(f"[run] Resumen de análisis: {analysis.get('summary', {})}")
        return

    app.invoke(estado_inicial)
    print(f"[run] Flujo completo (Sprints 1-3) terminado para '{alias}'.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner del sistema multiagente")
    parser.add_argument(
        "--mode",
        choices=["ingesta", "preparacion", "analista", "all"],
        default="ingesta",
        help=(
            "ingesta=Sprint1 | preparacion=Sprint2 | analista=Sprint3 | "
            "all=Sprints 1-3 en cadena (más nodos placeholder)"
        ),
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
