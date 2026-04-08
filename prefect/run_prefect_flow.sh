#!/bin/bash
# Script para ejecutar el flujo Prefect de Clase 7
# Uso: bash run_prefect_flow.sh

set -e

PROJECT_DIR="/mnt/c/Users/impactales/Documents/GitHub/Integraciondatos/mi_proyeco_dbt"
PREFECT_DIR="$PROJECT_DIR/prefect"
VENV_DIR="$PROJECT_DIR/.venv-wsl"

echo "=========================================="
echo "Clase 7: Ejecutando flujo Prefect"
echo "=========================================="
echo ""

# Activar venv
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo "✓ Virtual environment activado"
else
    echo "✗ Virtual environment no encontrado en $VENV_DIR"
    exit 1
fi

# Instalar/verificar dependencias del flujo
echo ""
echo "Instalando dependencias de Prefect..."
pip install -r "$PREFECT_DIR/requirements.txt"

# Cargar .env
echo ""
echo "Cargando variables de entorno..."
if [ -f "$PREFECT_DIR/.env" ]; then
    export $(cat "$PREFECT_DIR/.env" | grep -v '^#' | xargs)
    echo "✓ .env cargado"
else
    echo "⚠ .env no encontrado en $PREFECT_DIR"
    echo "  Usar .env.example como referencia"
fi

# Ejecutar el flujo
echo ""
echo "=========================================="
echo "Iniciando flujo Prefect..."
echo "=========================================="
echo ""

cd "$PREFECT_DIR"

python flow_ecommerce_clase7.py 2>&1 | tee flow_output_$(date +%Y%m%d_%H%M%S).txt

echo ""
echo "=========================================="
echo "✓ Flujo completado"
echo "=========================================="
