from __future__ import annotations

import json

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

from backend.agents.state import AgentState
from backend.agents.tools.insights_validation import validate_insights_report
from backend.core.config import settings
from backend.core.storage import save_insights_data
from backend.prompts.system_prompts import INSIGHTS_PROMPT, INSIGHTS_RETRY_PROMPT


def _analysis_is_actionable(analysis: dict) -> bool:
    if not analysis or analysis.get("dataset_type") in (None, "unknown"):
        return False
    summary = analysis.get("summary") or {}
    if not summary:
        return False
    if summary.get("n", summary.get("total_registros", 0)) == 0:
        return False
    return True


def _invoke_llm(llm: ChatOllama, prompt_text: str) -> str:
    response = llm.invoke(prompt_text)
    return getattr(response, "content", str(response)).strip()


def insights_node(state: AgentState) -> AgentState:
    analysis = state.get("analysis")

    if not _analysis_is_actionable(analysis):
        msg = (
            "No hay datos suficientes para generar un informe ejecutivo. "
            f"Tipo de dataset: {analysis.get('dataset_type') if analysis else 'sin análisis'}."
        )
        print(f"[Agente de Insights] {msg}")
        return {**state, "insights": [msg]}

    print("[Agente de Insights] Generando reporte en lenguaje natural con Ollama...")

    try:
        llm = ChatOllama(model="llama3", temperature=0.1)
        prompt = PromptTemplate.from_template(INSIGHTS_PROMPT)
        analysis_str = json.dumps(analysis, ensure_ascii=False, indent=2)
        response_text = _invoke_llm(llm, prompt.format(analysis_data=analysis_str))

        if not response_text:
            print("[Agente de Insights] Advertencia: el LLM devolvió una respuesta vacía.")
            return state

        is_valid, errors = validate_insights_report(analysis, response_text)

        if not is_valid:
            print("[Agente de Insights] Validación fallida; reintentando con prompt estricto...")
            for err in errors:
                print(f"  - {err}")

            retry_prompt = PromptTemplate.from_template(INSIGHTS_RETRY_PROMPT)
            detalle = "\n".join(
                f"- {u}" for u in analysis.get("anomalies_detalle", []) if u
            ) or "(sin anomalías)"
            summary_keys = ", ".join(
                f"{k}={v}" for k, v in (analysis.get("summary") or {}).items()
            )
            retry_text = retry_prompt.format(
                anomalies_detalle=detalle,
                summary_keys=summary_keys,
                validation_errors="\n".join(f"- {e}" for e in errors),
                analysis_data=analysis_str,
            )
            response_text = _invoke_llm(llm, retry_text)
            is_valid, errors = validate_insights_report(analysis, response_text)

            if not is_valid:
                print("[Agente de Insights] Advertencia: el informe sigue con inconsistencias.")
                for err in errors:
                    print(f"  - {err}")
                response_text += (
                    "\n\n---\n[Validación automática] El informe puede contener "
                    "inconsistencias con el JSON de análisis. Revisar anomalies_detalle."
                )
            else:
                print("[Agente de Insights] Informe corregido tras reintento.")

        preview = response_text[:300] + ("..." if len(response_text) > 300 else "")
        print(f"[Agente de Insights] Fragmento del informe:\n{preview}")

        dataset_id = state.get("dataset_id") or settings.default_dataset_id
        try:
            path = save_insights_data(dataset_id, response_text)
            print(f"[Agente de Insights] Informe guardado en: {path}")
        except Exception as exc:
            print(f"[Agente de Insights] Advertencia: no se pudo guardar el informe: {exc}")

        return {**state, "insights": [response_text]}

    except Exception as exc:
        print(f"[Agente de Insights] Error al invocar Ollama: {exc}")
        print(
            "[Agente de Insights] Verifica que Ollama esté en ejecución "
            "y que el modelo 'llama3' esté instalado (ollama pull llama3)."
        )
        return state
