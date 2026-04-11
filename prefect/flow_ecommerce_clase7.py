"""
Flujo Prefect para orquestación Clase 7: Airbyte Cloud -> MySQL -> MotherDuck -> dbt

Ejecuta:
1. Sincronización de Airbyte Cloud
2. Validación de conexión MySQL (Aiven)
3. Validación de sincronización en MotherDuck
4. Ejecución de dbt build para modelos ecommerce
5. Reporte de resultados

Uso:
    # Opción 1: Ejecutar una sola vez
    python flow_ecommerce_clase7.py

    # Opción 2: Modo serve con schedule (diario a las 6am)
    # Descomentar en main y ejecutar
"""

import os
import time
from pathlib import Path
from typing import Any, Dict

import httpx
import mysql.connector
from dotenv import load_dotenv
from prefect import flow, task, get_run_logger
from prefect_dbt.cli.commands import DbtCoreOperation

# Cargar variables de entorno
load_dotenv()


def _get_airbyte_settings() -> Dict[str, str]:
    """Lee la configuración de Airbyte Cloud desde variables de entorno."""
    api_base_url = os.getenv("AIRBYTE_API_BASE_URL", "https://api.airbyte.com/v1").rstrip("/")
    connection_id = os.getenv("AIRBYTE_CONNECTION_ID")
    access_token = os.getenv("AIRBYTE_ACCESS_TOKEN")
    client_id = os.getenv("AIRBYTE_CLIENT_ID")
    client_secret = os.getenv("AIRBYTE_CLIENT_SECRET")
    token_url = os.getenv("AIRBYTE_TOKEN_URL", f"{api_base_url}/applications/token").rstrip("/")

    if not connection_id:
        raise ValueError("AIRBYTE_CONNECTION_ID no configurado")

    if not access_token and (not client_id or not client_secret):
        raise ValueError(
            "Configura AIRBYTE_ACCESS_TOKEN o bien AIRBYTE_CLIENT_ID y AIRBYTE_CLIENT_SECRET"
        )

    return {
        "api_base_url": api_base_url,
        "connection_id": connection_id,
        "access_token": access_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "token_url": token_url,
    }


def _get_airbyte_access_token(settings: Dict[str, str]) -> str:
    """Obtiene el token de Airbyte Cloud a partir de credenciales de aplicación o token directo."""
    if settings.get("access_token"):
        return settings["access_token"]

    client_id = settings.get("client_id")
    client_secret = settings.get("client_secret")
    if not client_id or not client_secret:
        raise ValueError("No hay credenciales suficientes para autenticar Airbyte Cloud")

    token_url = settings["token_url"]
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    with httpx.Client(timeout=60) as client:
        response = client.post(token_url, json=payload)
        if response.status_code >= 400:
            response = client.post(token_url, data=payload)

        response.raise_for_status()
        token_payload = response.json()

    token = token_payload.get("access_token") or token_payload.get("token")
    if not token:
        raise ValueError(f"No se pudo obtener access_token desde Airbyte: {token_payload}")

    return str(token)


def _extract_job_id(payload: Dict[str, Any]) -> str:
    """Extrae el job_id desde la respuesta de Airbyte con tolerancia a distintos formatos."""
    job = payload.get("job")
    if isinstance(job, dict) and job.get("id"):
        return str(job["id"])

    if payload.get("jobId"):
        return str(payload["jobId"])

    if payload.get("id"):
        return str(payload["id"])

    raise ValueError(f"No se pudo obtener job_id desde la respuesta de Airbyte: {payload}")


def _extract_job_status(payload: Dict[str, Any]) -> str:
    """Obtiene el status del job desde la respuesta de Airbyte."""
    job = payload.get("job")
    if isinstance(job, dict) and job.get("status"):
        return str(job["status"]).lower()

    if payload.get("status"):
        return str(payload["status"]).lower()

    if payload.get("jobStatus"):
        return str(payload["jobStatus"]).lower()

    raise ValueError(f"No se pudo obtener status desde la respuesta de Airbyte: {payload}")


@task(name="trigger_airbyte_sync", retries=3, retry_delay_seconds=30)
def trigger_airbyte_sync() -> Dict[str, str]:
    """Dispara un sync de Airbyte Cloud y hace polling hasta finalizar."""
    logger = get_run_logger()

    settings = _get_airbyte_settings()
    access_token = _get_airbyte_access_token(settings)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    sync_url = f"{settings['api_base_url']}/connections/sync"
    poll_url = f"{settings['api_base_url']}/jobs/get"

    logger.info("Disparando sync de Airbyte Cloud...")

    with httpx.Client(timeout=60, headers=headers) as client:
        response = client.post(sync_url, json={"connectionId": settings["connection_id"]})

        if response.status_code == 409:
            logger.warning("Airbyte reportó un sync en curso (409). Se reintentará automáticamente.")
            time.sleep(30)
            raise RuntimeError("Sync de Airbyte ya en curso; reintento programado por Prefect")

        response.raise_for_status()
        payload = response.json()
        job_id = _extract_job_id(payload)
        logger.info(f"Airbyte sync iniciado. job_id={job_id}")

        max_attempts = 60
        poll_seconds = 10

        for attempt in range(1, max_attempts + 1):
            poll_response = client.post(poll_url, json={"id": job_id})
            poll_response.raise_for_status()
            poll_payload = poll_response.json()
            status = _extract_job_status(poll_payload)

            logger.info(f"Airbyte job {job_id} intento {attempt}/{max_attempts}: status={status}")

            if status in {"succeeded", "success"}:
                logger.info("Airbyte sync completado exitosamente.")
                return {
                    "status": "success",
                    "message": f"Airbyte sync completado. job_id={job_id}",
                }

            if status in {"failed", "cancelled"}:
                raise RuntimeError(f"Airbyte sync falló con status={status}. job_id={job_id}")

            time.sleep(poll_seconds)

        raise TimeoutError(f"Airbyte sync no terminó dentro del tiempo esperado. job_id={job_id}")


@task(name="validate_mysql_connection", retries=2, retry_delay_seconds=5)
def validate_mysql_connection() -> Dict[str, str]:
    """Valida conexión a MySQL en Aiven."""
    logger = get_run_logger()
    
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "mysql-3486cffb-danielramirezconsultor.k.aivencloud.com"),
            port=int(os.getenv("MYSQL_PORT", 14473)),
            user=os.getenv("MYSQL_USER", "avnadmin"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE", "ecommerce")
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) as test_count FROM website_sessions;")
        result = cursor.fetchone()
        
        connection.close()
        
        logger.info(f"✓ MySQL connected. Test count: {result[0]}")
        return {
            "status": "success",
            "message": f"MySQL Aiven conexión exitosa. Filas en website_sessions: {result[0]}"
        }
    except Exception as e:
        logger.error(f"✗ MySQL connection failed: {str(e)}")
        return {
            "status": "failed",
            "message": f"Error: {str(e)}"
        }


@task(name="validate_motherduck_data", retries=2, retry_delay_seconds=5)
def validate_motherduck_data() -> Dict[str, str]:
    """Valida sincronización de datos en MotherDuck."""
    logger = get_run_logger()
    
    try:
        import duckdb
        
        # Conectar a MotherDuck usando token
        token = os.getenv("MOTHERDUCK_TOKEN")
        if not token:
            raise ValueError("MOTHERDUCK_TOKEN no configurado")

        conn = duckdb.connect(f"md:?motherduck_token={token}")

        # Validar que las tablas estén presentes en schema main
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main'
          AND (
              table_name LIKE 'website_%'
              OR table_name LIKE 'order%'
              OR table_name = 'products'
          )
        """

        result = conn.execute(query).fetchall()
        
        logger.info(f"✓ MotherDuck: {len(result)} tablas encontradas")
        
        return {
            "status": "success",
            "message": f"MotherDuck validado. {len(result)} tablas de ecommerce presentes."
        }
    except Exception as e:
        logger.error(f"✗ MotherDuck validation failed: {str(e)}")
        return {
            "status": "failed",
            "message": f"Error: {str(e)}"
        }


@task(name="execute_dbt_build")
def execute_dbt_build() -> Dict:
    """Ejecuta dbt build para modelos ecommerce usando DbtCoreOperation."""
    logger = get_run_logger()
    
    dbt_project_dir = Path(os.getenv(
        "DBT_PROJECT_DIR", 
        "/mnt/c/Users/impactales/Documents/GitHub/Integraciondatos/mi_proyeco_dbt"
    ))
    
    dbt_profiles_dir = Path(os.getenv(
        "DBT_PROFILES_DIR",
        dbt_project_dir
    ))
    
    logger.info(f"Ejecutando dbt build desde: {dbt_project_dir}")
    
    try:
        result = DbtCoreOperation(
            commands=[
                "dbt deps",
                "dbt build --select path:models/staging/ecommerce path:models/intermediate/ecommerce path:models/marts/ecommerce"
            ],
            project_dir=str(dbt_project_dir),
            profiles_dir=str(dbt_profiles_dir),
        ).run()
        
        logger.info("dbt build completado exitosamente")
        return {
            "status": "success",
            "message": "dbt build ejecutado"
        }
    except Exception as e:
        logger.error(f"dbt build error: {str(e)}")
        return {
            "status": "failed",
            "message": f"Error: {str(e)}"
        }


@flow(name="Clase7_Ecommerce_Pipeline")
def ecommerce_pipeline_clase7(run_validate: bool = True, run_build: bool = True, run_airbyte: bool = False):
    """
    Orquestación principal: Airbyte Cloud -> MySQL -> MotherDuck -> dbt
    
    Args:
        run_validate: Si ejecutar validación de conexiones
        run_build: Si ejecutar dbt build
        run_airbyte: Si disparar sincronización de Airbyte Cloud
    """
    logger = get_run_logger()
    
    logger.info("=" * 80)
    logger.info("Iniciando flujo Clase 7: Ecommerce ETL + Transformación")
    logger.info("=" * 80)
    
    results = {}

    # Tarea 1: Disparar sincronización de Airbyte (opcional)
    if run_airbyte:
        logger.info("\n[1/4] Disparando sincronización Airbyte Cloud...")
        try:
            airbyte_result = trigger_airbyte_sync()
            results["airbyte"] = airbyte_result
            logger.info(airbyte_result["message"])
        except Exception as exc:
            logger.warning(f"Airbyte Cloud no se ejecutó correctamente: {exc}")
            results["airbyte"] = {
                "status": "failed",
                "message": f"Airbyte Cloud no se ejecutó correctamente: {exc}",
            }
    else:
        logger.info("\n[1/4] Airbyte Cloud omitido (run_airbyte=False)")
        results["airbyte"] = {
            "status": "skipped",
            "message": "Airbyte Cloud omitido por configuración",
        }
    
    # Tarea 2: Validar MySQL
    if run_validate:
        logger.info("\n[2/4] Validando conexión MySQL...")
        mysql_result = validate_mysql_connection()
        results["mysql"] = mysql_result
        logger.info(mysql_result["message"])
        
        # Tarea 3: Validar MotherDuck
        logger.info("\n[3/4] Validando sincronización MotherDuck...")
        md_result = validate_motherduck_data()
        results["motherduck"] = md_result
        logger.info(md_result["message"])
    
    # Tarea 4: Ejecutar dbt
    if run_build:
        logger.info("\n[4/4] Ejecutando dbt build...")
        dbt_result = execute_dbt_build()
        results["dbt"] = dbt_result
        logger.info(dbt_result["message"])
    
    # Reporte final
    logger.info("\n" + "=" * 80)
    logger.info("REPORTE FINAL")
    logger.info("=" * 80)
    for key, result in results.items():
        logger.info(f"{key:15} : {result['status']}")
    logger.info("=" * 80 + "\n")
    
    return results


if __name__ == "__main__":
    # ===========================================================================
    # OPCIÓN 1: Ejecutar flujo una sola vez
    # ===========================================================================
    ecommerce_pipeline_clase7(run_validate=True, run_build=True, run_airbyte=False)
    
    # ===========================================================================
    # OPCIÓN 2: Ejecutar flujo con scheduler (diario a las 6am)
    # Descomentar las siguientes líneas para activar
    # ===========================================================================
    # ecommerce_pipeline_clase7.serve(
    #     name="clase7-ecommerce-daily",
    #     cron="0 6 * * *",  # Diario a las 6am
    #     parameters={
    #         "run_validate": True,
    #         "run_build": True,
    #         "run_airbyte": False,
    #     }
    # )
    
    print("\n✓ Flujo completado")
