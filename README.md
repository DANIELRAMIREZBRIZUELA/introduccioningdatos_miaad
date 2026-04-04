# OpenWeather + Airbyte Cloud + MotherDuck + dbt

Este proyecto implementa una canalización dbt por capas para datos de OpenWeather cargados por Airbyte en MotherDuck.

## Arquitectura implementada

1. Airbyte Cloud ingiere OpenWeather en MotherDuck.
2. dbt transforma la tabla cruda en capas staging, intermediate y mart.

## Estructura actual del proyecto

- `models/staging/_sources.yml`: definición de fuentes
- `models/staging/openweather/stg_openweather__weather.sql`: staging de clima diario
- `models/staging/openweather/stg_openweather__current.sql`: staging de clima actual
- `models/intermediate/openweather/int_openweather__daily_summary.sql`: agregación intermedia
- `models/marts/weather/fct_openweather_daily_weather.sql`: tabla mart final

## Mapeo actual de la fuente en MotherDuck

- esquema: `main`
- tabla: `onecall`

Configurado mediante variables de dbt en `dbt_project.yml`:

- `openweather_raw_schema`
- `openweather_raw_table`

## Ejecución local

1. Definir `MOTHERDUCK_TOKEN` en la terminal.
2. Ejecutar `dbt build`.

## Estado de cobertura de la tarea

1. Proyecto dbt inicializado y configurado: completo.
2. Al menos 2 modelos staging: completo.
3. Al menos 1 modelo intermediate: completo.
4. Al menos 1 modelo mart: completo.
5. `_sources.yml` configurado: completo.
6. Captura del DAG desde dbt docs: completo (`Clase5_DAG.png`).

## Evidencia del DAG

La captura del linaje correspondiente al entregable de la clase 5 está incluida en `Clase5_DAG.png`.

## Alcance por clase para la evaluación

La clase 5 termina en el commit `c2618a5` en `main` con estos entregables:

1. `dbt_project.yml` configurado.
2. Al menos 2 modelos staging.
3. Al menos 1 modelo intermediate.
4. Al menos 1 modelo mart.
5. `models/staging/_sources.yml` configurado.
6. Captura del DAG incluida como `Clase5_DAG.png`.

La clase 6 comienza después de la clase 5 y queda completada en el commit `0964bda` en `main` con estos entregables:

1. `dbt-expectations` instalado (`packages.yml` + `package-lock.yml`).
2. 5 o más tests genéricos en archivos YAML de modelos.
3. 3 tests de `dbt-expectations` en archivos YAML de modelos.
4. 2 tests singulares en `tests/assert_no_future_observation_dates.sql` y `tests/assert_temperature_band_consistency.sql`.
5. Documentación ampliada en descripciones de modelos y columnas.
6. Captura del DAG incluida como `Clase6_DAG.png`.

La clase 5 y la clase 6 están separadas por el historial de commits y por archivos de evidencia distintos (`Clase5_DAG.png` y `Clase6_DAG.png`).

## Alternativa para generar el DAG

La política de tu equipo bloquea la carga de la extensión DuckDB de MotherDuck cuando se usa `dbt-core docs generate` (App Control de Windows), mientras que `dbt-fusion` sí funciona correctamente.

Alternativa recomendada para obtener la captura requerida:

1. Abrir la vista de linaje/DAG desde la extensión de dbt en VS Code, usando el mismo proyecto y dependencias.
2. Guardar la captura en el repositorio como evidencia.

Si más adelante la política se relaja, puedes ejecutar:

1. `python -m dbt.cli.main docs generate`
2. `python -m dbt.cli.main docs serve`
