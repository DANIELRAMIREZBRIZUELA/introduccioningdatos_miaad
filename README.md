# OpenWeather + Airbyte Cloud + MotherDuck + dbt

This project implements a layered dbt pipeline for OpenWeather data loaded by Airbyte into MotherDuck.

## Implemented architecture

1. Airbyte Cloud ingests OpenWeather into MotherDuck.
2. dbt transforms the raw table into staging, intermediate, and mart layers.

## Current project structure

- `models/staging/_sources.yml`: source definitions
- `models/staging/openweather/stg_openweather__weather.sql`: daily weather staging
- `models/staging/openweather/stg_openweather__current.sql`: current weather staging
- `models/intermediate/openweather/int_openweather__daily_summary.sql`: intermediate aggregation
- `models/marts/weather/fct_openweather_daily_weather.sql`: final mart table

## Current MotherDuck source mapping

- schema: `main`
- table: `onecall`

Configured via dbt vars in `dbt_project.yml`:

- `openweather_raw_schema`
- `openweather_raw_table`

## Run locally

1. Set `MOTHERDUCK_TOKEN` in your shell.
2. Run `dbt build`.

## Assignment coverage status

1. dbt project initialized and configured: done.
2. At least 2 staging models: done.
3. At least 1 intermediate model: done.
4. At least 1 mart model: done.
5. `_sources.yml` configured: done.
6. DAG screenshot from dbt docs: done (`Clase5_DAG.png`).

## DAG evidence

The lineage screenshot for class 5 deliverable is included at `Clase5_DAG.png`.

## Scope by class (for grading)

Class 5 ends in commit `c2618a5` on `main` with these deliverables:

1. `dbt_project.yml` configured.
2. At least 2 staging models.
3. At least 1 intermediate model.
4. At least 1 mart model.
5. `models/staging/_sources.yml` configured.
6. DAG screenshot included as `Clase5_DAG.png`.

Class 6 starts after Class 5 and is completed in commit `0964bda` on `main` with these deliverables:

1. `dbt-expectations` installed (`packages.yml` + `package-lock.yml`).
2. 5+ generic tests in model schema YAML files.
3. 3 dbt-expectations tests in schema YAML files.
4. 2 singular tests in `tests/assert_no_future_observation_dates.sql` and `tests/assert_temperature_band_consistency.sql`.
5. Documentation expanded in model/column descriptions.
6. DAG screenshot included as `Clase6_DAG.png`.

Class 5 and Class 6 are intentionally separated by commit history and by dedicated DAG evidence files (`Clase5_DAG.png` and `Clase6_DAG.png`).

## DAG screenshot workaround

Your machine policy blocks loading the MotherDuck DuckDB extension for `dbt-core docs generate` (Windows App Control), while `dbt-fusion` runs successfully.

Recommended workaround for the deliverable screenshot:

1. Capture the lineage/DAG view from the dbt VS Code extension (same project and dependencies).
2. Include the capture in the repository as evidence.

If policy is relaxed later, run:

1. `python -m dbt.cli.main docs generate`
2. `python -m dbt.cli.main docs serve`
