# Clase 7 - Ecommerce, Orquestacion y Visualizacion

Este archivo resume solo lo necesario para entregar la Clase 7. Los entregables de Clase 5 y Clase 6 permanecen congelados y no se modifican.

## Alcance de la clase

La clase 7 trabaja con el caso de uso de ecommerce y cubre el flujo completo:

Airbyte -> MotherDuck -> dbt -> Prefect -> Metabase

La consigna del profesor en la transcripcion fue usar dos fuentes de datos no triviales, ejecutar el proyecto localmente, orquestar con Prefect y cerrar con un dashboard en Metabase.

## Entregables requeridos

1. Airbyte: connection MySQL -> MotherDuck funcionando.
2. dbt: modelos de ecommerce ejecutandose.
3. Prefect: pipeline completo con variables de entorno configuradas.
4. Metabase: dashboard con al menos 5 visualizaciones y 2 filtros.
5. Evidencias: captura de Prefect UI y captura del dashboard.

## Alcance de la orquestacion implementada

- La orquestacion de Clase 7 se implementa con Prefect en `prefect/flow_ecommerce_clase7.py`.
- El flujo actual puede disparar Airbyte Cloud de forma opcional (`run_airbyte`).
- Para preservar una ejecucion estable de entrega, el modo por defecto usa `run_airbyte=False`; en ese modo el pipeline base sigue ejecutando validación MySQL, validación MotherDuck y `dbt build` para ecommerce.
- Las variables necesarias para Airbyte Cloud se documentan en `prefect/.env.example`.

## Estado actual validado

- Se ejecutó el flujo completo con estado final `Completed` en Prefect.
- Resultado validado: `airbyte=skipped`, `mysql=success`, `motherduck=success`, `dbt=success`.
- Integración API de Airbyte Cloud: implementada en código, pero pendiente de validación end-to-end por errores de autenticación/endpoint observados en pruebas de API.

## Estructura a subir

### dbt

- `models/staging/ecommerce/` - capa staging de ecommerce, con las tablas limpias de entrada.
- `models/intermediate/ecommerce/` - capa intermedia de ecommerce, con transformaciones y enriquecimiento.
- `models/marts/ecommerce/` - capa marts de ecommerce, con las tablas finales para analisis y dashboard.

### Prefect

- `prefect/flow_ecommerce_clase7.py`
- `prefect/requirements.txt`
- `prefect/run_prefect_flow.sh`
- `prefect/.env.example`

No versionar `prefect/.env` ni credenciales reales.

### Metabase

- `metabase/docker-compose.clase7.yml`
- `metabase/dashboard_queries_clase7.sql`
- `metabase/metabase_connection_clase7.txt`

### Lectura rapida de la estructura

- Staging: normaliza las fuentes de ecommerce.
- Intermediate: combina y prepara las entidades principales.
- Marts: expone las tablas finales para analisis y visualizacion.

### No se incluyen en la entrega

- `fuzzy-mid-course-prjt.sql` es material de apoyo/practica y no forma parte de la entrega final de Clase 7.
- `prefect/.env` contiene credenciales reales y no debe versionarse.

### Evidencias

- `evidencias/clase7/Captura_Prefect_Flows.png`
- `evidencias/clase7/Captura_Prefect_Flows_Clase7_Ecommerce_Pipeline.png`
- `evidencias/clase7/Captura_Prefect_Dashboard.png`
- `evidencias/clase7/Captura_Prefect_Runs.png`
- `evidencias/clase7/Captura_Mysql_MotherDuck_Settings.png`
- `evidencias/clase7/Captura_Mysql_MotherDuck_Schema.png`
- `evidencias/clase7/captura_UI_Metabase (1).png`
- `evidencias/clase7/captura_UI_Metabase (2).png`
- `evidencias/clase7/captura_UI_Metabase (3).png`
- `evidencias/clase7/captura_UI_Metabase (4)_filters.png`
- `evidencias/clase7/dbt_ecommerce_build_pass36.txt`
- `evidencias/clase7/prefect_clase7_flow_output_v3.txt`

## Checklist de cumplimiento

- [x] Airbyte configurado (modo manual/documentado).
- [x] dbt ecommerce ejecutado.
- [x] Prefect ejecutado.
- [x] Metabase levantado y dashboard construido.
- [x] Capturas de Prefect y Metabase guardadas.
- [ ] Trigger de Airbyte Cloud por API validado de extremo a extremo.

## Notas de seguridad

- No se incluyen claves ni archivos `.env` reales en el repositorio.
- Si se documenta configuracion, usar unicamente `.env.example` y descripciones genericas.
