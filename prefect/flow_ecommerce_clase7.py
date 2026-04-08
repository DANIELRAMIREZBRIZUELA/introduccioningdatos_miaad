"""
Flujo Prefect para orquestación Clase 7: MySQL -> MotherDuck -> dbt

Ejecuta:
1. Validación de conexión MySQL (Aiven)
2. Validación de sincronización en MotherDuck
3. Ejecución de dbt build para modelos ecommerce
4. Reporte de resultados

Uso:
    # Opción 1: Ejecutar una sola vez
    python flow_ecommerce_clase7.py

    # Opción 2: Modo serve con schedule (diario a las 6am)
    # Descomentar en main y ejecutar
"""

import os
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import mysql.connector
from dotenv import load_dotenv
from prefect import flow, task, get_run_logger
from prefect_dbt.cli.commands import DbtCoreOperation

# Cargar variables de entorno
load_dotenv()


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
def ecommerce_pipeline_clase7(run_validate: bool = True, run_build: bool = True):
    """
    Orquestación principal: MySQL -> MotherDuck -> dbt
    
    Args:
        run_validate: Si ejecutar validación de conexiones
        run_build: Si ejecutar dbt build
    """
    logger = get_run_logger()
    
    logger.info("=" * 80)
    logger.info("Iniciando flujo Clase 7: Ecommerce ETL + Transformación")
    logger.info("=" * 80)
    
    results = {}
    
    # Tarea 1: Validar MySQL
    if run_validate:
        logger.info("\n[1/3] Validando conexión MySQL...")
        mysql_result = validate_mysql_connection()
        results["mysql"] = mysql_result
        logger.info(mysql_result["message"])
        
        # Tarea 2: Validar MotherDuck
        logger.info("\n[2/3] Validando sincronización MotherDuck...")
        md_result = validate_motherduck_data()
        results["motherduck"] = md_result
        logger.info(md_result["message"])
    
    # Tarea 3: Ejecutar dbt
    if run_build:
        logger.info("\n[3/3] Ejecutando dbt build...")
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
    ecommerce_pipeline_clase7(run_validate=True, run_build=True)
    
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
    #     }
    # )
    
    print("\n✓ Flujo completado")
