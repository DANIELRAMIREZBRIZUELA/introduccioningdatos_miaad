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

## Trabajo realizado

### dbt

- Se construyeron y validaron los modelos de ecommerce para staging, intermediate y marts.
- El `dbt build` quedó ejecutado correctamente para el caso de Clase 7.

### Prefect

- Se implementó el flujo `prefect/flow_ecommerce_clase7.py` para orquestar la pipeline.
- El flujo completo quedó validado con estado `Completed`.
- La ejecución estable por defecto usa `run_airbyte=False`.

### Metabase

- Se levantó la instancia local de Metabase para la entrega de Clase 7.
- Se construyó el dashboard final con 5 visualizaciones y 2 filtros.
- Se generaron las capturas nuevas de evidencia incluidas en esta entrega.

### Airbyte

- La conexión MySQL -> MotherDuck quedó documentada para la clase.
- La validación end-to-end por API quedó pendiente por los errores ya observados en pruebas.

### Lectura rapida de la estructura

- Staging: normaliza las fuentes de ecommerce.
- Intermediate: combina y prepara las entidades principales.
- Marts: expone las tablas finales para analisis y visualizacion.

### Evidencias

- `evidencias/clase7/Captura_Prefect_Flows.png`
- `evidencias/clase7/Captura_Prefect_Flows_Clase7_Ecommerce_Pipeline.png`
- `evidencias/clase7/Captura_Prefect_Dashboard.png`
- `evidencias/clase7/Captura_Prefect_Runs.png`
- `evidencias/clase7/Captura_Mysql_MotherDuck_Settings.png`
- `evidencias/clase7/Captura_Mysql_MotherDuck_Schema.png`
- `evidencias/clase7/captura_Metabase_datos_consultas_tablas.png`
- `evidencias/clase7/Captura_Metabase_Dashboard_5_visualizaciones.png`
- `evidencias/clase7/Captura_Metabase_Dashboard_5_visualizaciones_filtro_canales_activo.png`
- `evidencias/clase7/Captura_Metabase_Dashboard_5_visualizaciones_filtro_fechas_activo.png`
- `evidencias/clase7/dbt_ecommerce_build_pass36.txt`
- `evidencias/clase7/prefect_clase7_flow_output_v3.txt`

## Checklist de cumplimiento

- [x] Airbyte configurado (modo manual/documentado).
- [x] dbt ecommerce ejecutado.
- [x] Prefect ejecutado.
- [x] Metabase levantado y dashboard construido.
- [x] Capturas de Prefect y Metabase guardadas.

## Notas de seguridad

- No se incluyen claves ni archivos `.env` reales en el repositorio.
- Si se documenta configuracion, usar unicamente `.env.example` y descripciones genericas.
