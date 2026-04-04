# Clase 7 - Orquestacion y Visualizacion

Este archivo define el plan y el alcance de la Clase 7, manteniendo congelados los entregables de Clase 5 y Clase 6.

## Estado congelado previo

- Rama base congelada: `main`
- Tag de cierre: `clase6-final`
- Rama de trabajo Clase 7: `clase7-orquestacion-visualizacion`

Regla de trabajo: no modificar los artefactos de clases anteriores salvo correcciones tecnicas estrictamente necesarias.

## Entregables base (segun PDF Clase 7)

1. Airbyte: connection MySQL -> MotherDuck funcionando.
2. dbt: modelos en `main_staging` y `main_marts` ejecutandose.
3. Prefect: pipeline completo con `.env` configurado.
4. Metabase: dashboard con al menos 5 visualizaciones y 2 filtros.
5. Capturas: Prefect UI con ejecucion exitosa + dashboard.

## Evidencias a versionar

- Captura de ejecucion exitosa en Prefect.
- Captura de dashboard en Metabase.
- Configuracion reproducible del pipeline (codigo Prefect + ejemplo de variables).
- Modelos dbt de ecommerce y su ejecucion.

## Checklist de trabajo

- [ ] Configurar fuente y conexion en Airbyte.
- [ ] Crear modelos dbt de ecommerce (staging y marts).
- [ ] Implementar flujo Prefect (extract/load -> transform -> test -> docs opcional).
- [ ] Levantar Metabase con Docker.
- [ ] Construir dashboard (>= 5 visualizaciones y >= 2 filtros).
- [ ] Guardar capturas finales en el repositorio.
- [ ] Actualizar README principal con referencia a Clase 7 (sin alterar historial de Clase 5/6).

## Notas de seguridad

- No versionar credenciales reales.
- Versionar solo archivo de ejemplo para variables (`.env.example`).
- Mantener `MOTHERDUCK_TOKEN` y claves de Airbyte fuera del repositorio.
