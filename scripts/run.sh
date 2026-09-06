#!/usr/bin/env bash
# Esclarificador - Pipeline completo (wrapper modular)
# Version: 2.0.0

set -e

# Cargar módulos
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/lib"

source "$LIB_DIR/colors.sh"
source "$LIB_DIR/utils.sh"
source "$LIB_DIR/test_runner.sh"
source "$LIB_DIR/pipeline.sh"

# Detectar modo CI
if [ -n "$CI" ]; then
    CI_MODE=true
else
    CI_MODE=false
fi

# Variables
SHOW_LOG=false
VERBOSE=false
TEST_RUNNER="auto"
BRIDGE_ARGS=()

# Mostrar ayuda
show_help() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}🚀 ESCLARIFICADOR - AYUDA${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}USO:${NC}"
    echo "  ./run.sh [OPCIONES] [COMANDO] [ARGUMENTOS]"
    echo ""
    echo -e "${YELLOW}OPCIONES:${NC}"
    echo "  --help, -h     Muestra esta ayuda"
    echo "  --show-log     Muestra el log completo"
    echo "  --no-log       No muestra el log"
    echo "  --verbose, -v  Modo verbose"
    echo "  --ci           Modo CI"
    echo "  --test-runner  Forzar runner de tests"
    echo ""
    echo -e "${YELLOW}COMANDOS:${NC}"
    echo "  run            Pipeline completo (default)"
    echo "  interpret      Solo interpretar"
    echo "  generate       Generar código (--lang)"
    echo "  compile        Compilar Rust"
    echo "  clean          Limpiar archivos"
    echo "  test           Ejecutar tests"
    echo ""
    echo -e "${YELLOW}EJEMPLOS:${NC}"
    echo "  ./run.sh                    # Pipeline normal"
    echo "  ./run.sh run --verbose      # Con verbose"
    echo "  ./run.sh test               # Tests (auto-detecta)"
    echo "  ./run.sh --ci run           # Modo CI"
    echo "  ./run.sh --help             # Ayuda"
    echo ""
    echo -e "${BLUE}========================================${NC}"
}

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            exit 0
            ;;
        --show-log)
            SHOW_LOG=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            BRIDGE_ARGS+=("--verbose")
            shift
            ;;
        --no-log)
            SHOW_LOG=false
            shift
            ;;
        --ci)
            CI_MODE=true
            shift
            ;;
        --test-runner)
            TEST_RUNNER="$2"
            shift 2
            ;;
        test)
            BRIDGE_ARGS+=("test")
            shift
            ;;
        *)
            BRIDGE_ARGS+=("$1")
            shift
            ;;
    esac
done

# Banner
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🚀 ESCLARIFICADOR - PIPELINE COMPLETO${NC}"
echo -e "${BLUE}========================================${NC}"

# Verificar bridge/main.py
if ! check_file "bridge/main.py"; then
    die "No se encuentra bridge/main.py"
fi

# Asegurar archivos de ejemplo
ensure_example_files

# Ejecutar comando
if [[ " ${BRIDGE_ARGS[@]} " =~ " test " ]]; then
    # Modo tests
    run_tests "$TEST_RUNNER"
    TEST_EXIT=$?
    
    if [ $TEST_EXIT -eq 0 ]; then
        echo -e "${GREEN}✅ ¡Todos los tests pasaron!${NC}"
    else
        echo -e "${RED}❌ Fallaron algunos tests${NC}"
        exit $TEST_EXIT
    fi
else
    # Pipeline normal
    if [ ${#BRIDGE_ARGS[@]} -eq 0 ]; then
        BRIDGE_ARGS=("run")
    fi
    
    run_pipeline "$VERBOSE"
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ ¡Pipeline completado exitosamente!${NC}"
        
        # Mostrar log
        if [ "$SHOW_LOG" = true ] && check_file "output/logs.txt"; then
            echo ""
            echo -e "${CYAN}📋 Log completo:${NC}"
            echo -e "${CYAN}----------------------------------------${NC}"
            cat output/logs.txt
            echo -e "${CYAN}----------------------------------------${NC}"
        elif check_file "output/logs.txt"; then
            echo ""
            echo -e "${YELLOW}📋 Últimas 10 líneas del log:${NC}"
            echo -e "${YELLOW}----------------------------------------${NC}"
            tail -10 output/logs.txt
            echo -e "${YELLOW}----------------------------------------${NC}"
            echo -e "${CYAN}💡 Para ver log completo: ./run.sh --show-log${NC}"
        fi
    else
        echo ""
        echo -e "${RED}❌ Error durante la ejecución${NC}"
        if check_file "output/logs.txt"; then
            echo -e "${YELLOW}📋 Verifica el log: output/logs.txt${NC}"
        fi
        exit $EXIT_CODE
    fi
fi
