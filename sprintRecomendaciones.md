RECOMENDACIÓN TÉCNICA Y PLAN DE SPRINTS
Proyecto: Uso de APIs de Datos Abiertos en Salud mediante Agentes de IA

------------------------------------------------------------
1. VISIÓN DEL PROYECTO
------------------------------------------------------------

El objetivo del proyecto es desarrollar un sistema basado en agentes de inteligencia artificial capaz de consumir datos abiertos del sector salud (datos.gov.co), analizarlos automáticamente y generar insights relevantes, como tendencias, cambios significativos y alertas.

El valor diferencial del sistema radica en que no solo consulta datos, sino que los interpreta de forma autónoma mediante agentes especializados.

------------------------------------------------------------
2. ENFOQUE DE AGENTES DE IA
------------------------------------------------------------

El sistema estará compuesto por múltiples agentes con roles definidos:

- Agente de Ingesta: consulta datos desde la API.
- Agente de Preparación: limpia y estructura los datos.
- Agente Analista: detecta tendencias y anomalías.
- Agente de Insights: genera explicaciones en lenguaje natural.
- Agente de Alertas: decide si se debe generar una alerta.

Esto permite un flujo autónomo de análisis sin intervención manual.

------------------------------------------------------------
3. TECNOLOGÍAS RECOMENDADAS
------------------------------------------------------------

Lenguaje:
- Python

Framework de agentes:
- LangGraph (principal)
- LangChain (tools)

Modelo de IA:
- Ollama

Datos:
- Pandas
- NumPy

API:
- Socrata (datos.gov.co)

Backend:
- FastAPI

Visualización:
- Streamlit

Base de datos:
- PostgreSQL

Pruebas:
- Pytest

Infraestructura:
- Docker

------------------------------------------------------------
4. PLAN DE SPRINTS
------------------------------------------------------------

------------------------------------------------------------
SPRINT 1 — Agente de Ingesta y Arquitectura
------------------------------------------------------------

Objetivo:
Diseñar la arquitectura multiagente e implementar el agente de ingesta.

Tareas:
- Definir arquitectura basada en agentes
- Seleccionar datasets en datos.gov.co
- Implementar conexión con API Socrata
- Crear agente de ingesta
- Definir formato de datos entre agentes
- Estructurar repositorio
- Documentar roles de agentes

Entregables:
- Diagrama de arquitectura
- Agente de ingesta funcional
- Script de consumo de API

Criterios de aceptación:
- El agente consulta datos reales
- Devuelve datos estructurados
- Arquitectura documentada

------------------------------------------------------------
SPRINT 2 — Agente de Preparación de Datos
------------------------------------------------------------

Objetivo:
Limpiar y preparar los datos para análisis.

Tareas:
- Implementar agente de preparación
- Limpiar datos (nulos, duplicados)
- Normalizar columnas
- Convertir tipos de datos
- Filtrar por periodos
- Diseñar tools de limpieza
- Conectar con agente de ingesta

Entregables:
- Agente de preparación funcional
- Dataset limpio

Criterios de aceptación:
- Datos consistentes
- Flujo entre agentes funcionando

------------------------------------------------------------
SPRINT 3 — Agente Analista
------------------------------------------------------------

Objetivo:
Detectar patrones, tendencias y anomalías.

Tareas:
- Implementar agente analista
- Calcular variaciones porcentuales
- Comparar periodos
- Detectar anomalías
- Identificar tendencias
- Diseñar tools analíticas

Entregables:
- Motor de análisis automático
- Resultados estructurados

Criterios de aceptación:
- Detecta cambios relevantes
- Resultados interpretables

------------------------------------------------------------
SPRINT 4 — Agente Generador de Insights
------------------------------------------------------------

Objetivo:
Convertir resultados técnicos en lenguaje natural.

Tareas:
- Integrar Ollama
- Diseñar prompts
- Implementar agente de insights
- Generar explicaciones claras
- Validar coherencia de resultados

Entregables:
- Insights en lenguaje natural
- Reportes automáticos

Criterios de aceptación:
- Explicaciones claras
- No inventa datos
- Coherencia con resultados

------------------------------------------------------------
SPRINT 5 — Agente de Alertas y Sistema Final
------------------------------------------------------------

Objetivo:
Automatizar el sistema completo y generar alertas.

Tareas:
- Implementar agente de alertas
- Definir reglas de severidad
- Generar alertas automáticas
- Integrar flujo con LangGraph
- Crear dashboard en Streamlit
- Realizar pruebas finales
- Documentar sistema

Entregables:
- Sistema multiagente completo
- Dashboard funcional
- Documentación final

Criterios de aceptación:
- Flujo completo automatizado
- Agentes funcionando en cadena
- Generación de alertas


------------------------------------------------------------
5. VALOR DIFERENCIAL
------------------------------------------------------------

El sistema no solo consulta datos de salud, sino que automatiza su análisis, detecta cambios relevantes y genera explicaciones en lenguaje natural, permitiendo monitoreo continuo del sistema de salud.

------------------------------------------------------------
6. RECOMENDACIONES FINALES
------------------------------------------------------------

- No iniciar con IA, primero estructurar los datos
- Implementar agentes por etapas
- Validar cada agente antes de integrarlo
- No sobrecomplicar la autonomía
- Documentar cada proceso
- Usar LangGraph para orquestación clara

