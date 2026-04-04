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

Nota: en `models/staging/_sources.yml` se definen `raw_weather` y `raw_weather_current` con el mismo `identifier` (`onecall`) porque ambos modelos extraen secciones distintas del mismo JSON crudo cargado por Airbyte.

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
4. 2 tests singulares en `tests/assert_sky_condition_consistency.sql` y `tests/assert_temperature_band_consistency.sql`.
5. Documentación ampliada en descripciones de modelos y columnas.
6. Captura del DAG incluida como `Clase6_DAG.png`.

La clase 5 y la clase 6 están separadas por el historial de commits y por archivos de evidencia distintos (`Clase5_DAG.png` y `Clase6_DAG.png`).

## Checklist de cumplimiento

### Clase 5

1. Proyecto dbt inicializado: sí.
2. Al menos 2 modelos staging: sí.
3. Al menos 1 modelo intermediate: sí.
4. Al menos 1 modelo mart: sí.
5. `_sources.yml` configurado: sí.
6. DAG de clase 5 publicado: sí (`Clase5_DAG.png`).

### Clase 6

1. `dbt-expectations` instalado: sí.
2. Al menos 5 tests genéricos: sí.
3. Al menos 3 tests de `dbt-expectations`: sí.
4. Al menos 2 tests singulares: sí.
5. Documentación de modelos y columnas clave: sí.
6. `dbt build` con tests en verde: sí.
7. DAG de clase 6 publicado: sí (`Clase6_DAG.png`).

## Evidencia de ejecución de tests

Última validación completa ejecutada localmente con `dbt build --profiles-dir .`:

- Resultado: `PASS=42 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=42`.

## Alternativa para generar el DAG

La política de tu equipo bloquea la carga de la extensión DuckDB de MotherDuck cuando se usa `dbt-core docs generate` (App Control de Windows), mientras que `dbt-fusion` sí funciona correctamente.

Alternativa recomendada para obtener la captura requerida:

1. Abrir la vista de linaje/DAG desde la extensión de dbt en VS Code, usando el mismo proyecto y dependencias.
2. Guardar la captura en el repositorio como evidencia.

Si más adelante la política se relaja, puedes ejecutar:

1. `python -m dbt.cli.main docs generate`
2. `python -m dbt.cli.main docs serve`
