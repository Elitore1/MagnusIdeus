#!/usr/bin/env bash
# Esclarificador - Pipeline completo (wrapper para bridge/main.py)
# Version: 2.1.0
# Compatible con: Linux, macOS, WSL

set -e  # Salir ante cualquier error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Detectar si estamos en CI (GitHub Actions, GitLab CI, etc.)
if [ -n "$CI" ]; then
    CI_MODE=true
else
    CI_MODE=false
fi

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}🚀 ESCLARIFICADOR - AYUDA${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}USO:${NC}"
    echo "  ./run.sh [OPCIONES] [COMANDO] [ARGUMENTOS]"
    echo ""
    echo -e "${YELLOW}OPCIONES DE ESTE WRAPPER:${NC}"
    echo "  --help, -h     Muestra esta ayuda"
    echo "  --show-log     Muestra el log completo al finalizar"
    echo "  --no-log       No muestra el log al finalizar"
    echo "  --verbose, -v  Pasa --verbose a bridge/main.py y muestra log completo"
    echo "  --ci           Modo CI (sin colores, output minimalista)"
    echo "  --test-runner  Especifica el runner de tests (pytest|unittest|custom)"
    echo ""
    echo -e "${YELLOW}COMANDOS DISPONIBLES (para bridge/main.py):${NC}"
    echo "  run            Ejecuta el pipeline completo (default)"
    echo "  interpret      Solo interpretar C++ → AST"
    echo "  generate       Generar código (requiere --lang)"
    echo "  compile        Compilar Rust"
    echo "  clean          Limpiar archivos generados"
    echo "  test           Ejecutar tests (detección automática)"
    echo ""
    echo -e "${YELLOW}EJEMPLOS:${NC}"
    echo "  ./run.sh                              # Ejecución normal (run)"
    echo "  ./run.sh run --verbose                # Pipeline con verbose"
    echo "  ./run.sh test                         # Tests (auto-detecta pytest/unittest)"
    echo "  ./run.sh test --test-runner pytest    # Forzar pytest"
    echo "  ./run.sh test --test-runner unittest  # Forzar unittest"
    echo "  ./run.sh --ci run                     # Modo CI (para GitHub Actions)"
    echo "  ./run.sh --help                       # Muestra ayuda"
    echo ""
    echo -e "${BLUE}========================================${NC}"
}

# Variables
SHOW_LOG=false
CI_MODE=false
TEST_RUNNER="auto"
WRAPPER_ARGS=()
BRIDGE_ARGS=()

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            exit 0
            ;;
        --show-log)
            SHOW_LOG=true
            WRAPPER_ARGS+=("$1")
            shift
            ;;
        --verbose|-v)
            SHOW_LOG=true
            BRIDGE_ARGS+=("--verbose")
            WRAPPER_ARGS+=("$1")
            shift
            ;;
        --no-log)
            SHOW_LOG=false
            WRAPPER_ARGS+=("$1")
            shift
            ;;
        --ci)
            CI_MODE=true
            WRAPPER_ARGS+=("$1")
            shift
            ;;
        --test-runner)
            TEST_RUNNER="$2"
            shift 2
            ;;
        test)
            # Comando especial: test
            BRIDGE_ARGS+=("test")
            shift
            ;;
        *)
            BRIDGE_ARGS+=("$1")
            shift
            ;;
    esac
done

# Si estamos en CI, desactivar colores
if [ "$CI_MODE" = true ]; then
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    MAGENTA=''
    NC=''
fi

# Banner
if [ "$CI_MODE" = false ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}🚀 ESCLARIFICADOR - PIPELINE COMPLETO${NC}"
    echo -e "${BLUE}========================================${NC}"
else
    echo "========================================"
    echo "🚀 ESCLARIFICADOR - PIPELINE COMPLETO (CI MODE)"
    echo "========================================"
fi

# Verificar que existan los archivos necesarios
if [ ! -f "bridge/main.py" ]; then
    if [ "$CI_MODE" = false ]; then
        echo -e "${RED}❌ Error: No se encuentra bridge/main.py${NC}"
    else
        echo "❌ Error: No se encuentra bridge/main.py"
    fi
    echo "💡 El punto de entrada principal es bridge/main.py"
    echo "📂 Ruta esperada: $(pwd)/bridge/main.py"
    exit 1
fi

# Verificar que existe src/idea.cpp
if [ ! -f "src/idea.cpp" ]; then
    if [ "$CI_MODE" = false ]; then
        echo -e "${YELLOW}⚠️  Advertencia: No se encuentra src/idea.cpp${NC}"
    else
        echo "⚠️  Advertencia: No se encuentra src/idea.cpp"
    fi
    echo "   Creando archivo de ejemplo..."
    mkdir -p src
    cat > src/idea.cpp << 'CPPEOF'
#include <iostream>
#include <chrono>
#include <vector>

// Abstracción: Tanger (Problema)
class Tanger {
public:
    std::string problema = "renderizado_3d";
    void diagnosticar() { std::cout << "Problema identificado\n"; }
};

// Abstracción: Espejo (Análisis)
class Espejo {
public:
    void analizar(Tanger& t) { std::cout << "Analizando: " << t.problema << "\n"; }
};

// Abstracción: Modulus (Puente)
class Modulus {
public:
    std::string traducir(const std::string& idea) {
        return "TRADUCIDO:" + idea;
    }
};

// Abstracción: Cayo (Planificación)
class Cayo {
public:
    std::vector<std::string> pasos;
    void planificar() { pasos.push_back("paso_1"); }
};

// Abstracción: Barca (Ejecución)
class Barca {
public:
    void ejecutar() { std::cout << "Ejecutando...\n"; }
};
CPPEOF
    if [ "$CI_MODE" = false ]; then
        echo -e "${GREEN}✅ src/idea.cpp creado${NC}"
    else
        echo "✅ src/idea.cpp creado"
    fi
fi

# Verificar que existe config/mappings.json
if [ ! -f "config/mappings.json" ]; then
    if [ "$CI_MODE" = false ]; then
        echo -e "${YELLOW}⚠️  Advertencia: No se encuentra config/mappings.json${NC}"
    else
        echo "⚠️  Advertencia: No se encuentra config/mappings.json"
    fi
    echo "   Creando archivo de configuración por defecto..."
    mkdir -p config
    cat > config/mappings.json << 'JSONEOF'
{
  "version": "1.0",
  "abstracciones": {
    "Tanger": {
      "descripcion": "Identificación del problema",
      "python": "Problem",
      "js": "Problem",
      "rust": "Problem",
      "atributos": ["problema", "severidad", "contexto"],
      "metodos": ["diagnosticar", "identificar"]
    },
    "Espejo": {
      "descripcion": "Análisis y reflexión",
      "python": "Reflect",
      "js": "Reflect",
      "rust": "Reflect",
      "atributos": ["analisis", "contexto"],
      "metodos": ["analizar", "razonar"]
    },
    "Modulus": {
      "descripcion": "Puente entre idea y lógica",
      "python": "Bridge",
      "js": "Bridge",
      "rust": "Bridge",
      "atributos": ["origen", "destino"],
      "metodos": ["traducir", "mapear"]
    },
    "Cayo": {
      "descripcion": "Planificación",
      "python": "Plan",
      "js": "Plan",
      "rust": "Plan",
      "atributos": ["pasos", "estrategia"],
      "metodos": ["planificar", "diseñar"]
    },
    "Barca": {
      "descripcion": "Ejecución irreversible",
      "python": "Execute",
      "js": "Execute",
      "rust": "Execute",
      "atributos": ["estado", "resultado"],
      "metodos": ["ejecutar", "run"]
    }
  },
  "std_namespaces": {
    "chrono": {
      "descripcion": "Manejo de tiempo",
      "python": "datetime",
      "js": "Date",
      "rust": "std::time"
    },
    "vector": {
      "descripcion": "Contenedor dinámico",
      "python": "list",
      "js": "Array",
      "rust": "std::vec::Vec"
    }
  },
  "tipos_datos": {
    "string": {"python": "str", "js": "string", "rust": "String"},
    "int": {"python": "int", "js": "number", "rust": "i32"},
    "float": {"python": "float", "js": "number", "rust": "f64"},
    "bool": {"python": "bool", "js": "boolean", "rust": "bool"},
    "vector": {"python": "list", "js": "Array", "rust": "Vec<String>"}
  }
}
JSONEOF
    if [ "$CI_MODE" = false ]; then
        echo -e "${GREEN}✅ config/mappings.json creado${NC}"
    else
        echo "✅ config/mappings.json creado"
    fi
fi

# Crear directorios necesarios
mkdir -p intermediate
mkdir -p output/generated

# Verificar Python
if ! command -v python3 &> /dev/null; then
    if [ "$CI_MODE" = false ]; then
        echo -e "${RED}❌ Error: python3 no está instalado${NC}"
    else
        echo "❌ Error: python3 no está instalado"
    fi
    echo "💡 Instala Python 3.8 o superior"
    exit 1
fi

# === COMANDO TEST ===
# Si el comando es "test", ejecutar tests
if [[ " ${BRIDGE_ARGS[@]} " =~ " test " ]]; then
    echo ""
    if [ "$CI_MODE" = false ]; then
        echo -e "${MAGENTA}🧪 EJECUTANDO TESTS${NC}"
        echo -e "${MAGENTA}========================================${NC}"
    else
        echo "🧪 EJECUTANDO TESTS"
        echo "========================================"
    fi
    
    # Determinar qué runner usar
    RUNNER=""
    
    # Si se especificó --test-runner, usarlo
    if [ "$TEST_RUNNER" != "auto" ]; then
        RUNNER="$TEST_RUNNER"
        if [ "$CI_MODE" = false ]; then
            echo -e "${CYAN}🔧 Usando runner forzado: $RUNNER${NC}"
        else
            echo "🔧 Usando runner forzado: $RUNNER"
        fi
    else
        # Auto-detección
        if command -v pytest &> /dev/null && [ -f "pytest.ini" -o -d "tests" ]; then
            RUNNER="pytest"
        elif [ -f "tests/run_tests.py" ]; then
            RUNNER="custom"
        elif [ -d "tests" ] && find tests -name "test_*.py" | grep -q .; then
            # Si hay tests con unittest
            RUNNER="unittest"
        elif command -v pytest &> /dev/null; then
            RUNNER="pytest"
        elif [ -f "tests/run_tests.py" ]; then
            RUNNER="custom"
        else
            RUNNER="unittest"  # Fallback a unittest
        fi
        
        if [ "$CI_MODE" = false ]; then
            echo -e "${CYAN}🔍 Runner detectado: $RUNNER${NC}"
        else
            echo "🔍 Runner detectado: $RUNNER"
        fi
    fi
    
    # Ejecutar según el runner
    case $RUNNER in
        pytest)
            echo "🔍 Usando pytest..."
            if [ -f "pytest.ini" ]; then
                echo "📋 Usando configuración: pytest.ini"
            fi
            pytest tests/ -v --tb=short --color=yes 2>&1
            TEST_EXIT=$?
            ;;
        unittest)
            echo "🔍 Usando unittest (framework estándar de Python)..."
            # Buscar tests en tests/ o en el directorio actual
            if [ -d "tests" ]; then
                python3 -m unittest discover -s tests -p "test_*.py" -v
            else
                python3 -m unittest discover -p "test_*.py" -v
            fi
            TEST_EXIT=$?
            ;;
        custom)
            echo "🔍 Usando script de tests personalizado..."
            python3 tests/run_tests.py
            TEST_EXIT=$?
            ;;
        *)
            echo "⚠️ Runner desconocido: $RUNNER"
            echo "💡 Opciones válidas: pytest, unittest, custom"
            TEST_EXIT=1
            ;;
    esac
    
    # Mostrar resultado
    if [ $TEST_EXIT -eq 0 ]; then
        if [ "$CI_MODE" = false ]; then
            echo -e "${GREEN}✅ ¡Todos los tests pasaron!${NC}"
        else
            echo "✅ ¡Todos los tests pasaron!"
        fi
    else
        if [ "$CI_MODE" = false ]; then
            echo -e "${RED}❌ Fallaron algunos tests${NC}"
        else
            echo "❌ Fallaron algunos tests"
        fi
        exit $TEST_EXIT
    fi
    exit 0
fi

# === PIPELINE NORMAL ===
# Si no hay argumentos para bridge/main.py, usar "run" por defecto
if [ ${#BRIDGE_ARGS[@]} -eq 0 ]; then
    BRIDGE_ARGS=("run")
fi

# Construir comando para bridge/main.py
CMD="python3 bridge/main.py ${BRIDGE_ARGS[@]}"

if [ "$CI_MODE" = false ]; then
    echo ""
    echo -e "${BLUE}📋 Ejecutando pipeline...${NC}"
    echo ""
    echo -e "${CYAN}▶️ Ejecutando: $CMD${NC}"
    echo ""
else
    echo ""
    echo "📋 Ejecutando pipeline..."
    echo ""
    echo "▶️ Ejecutando: $CMD"
    echo ""
fi

# Ejecutar y capturar salida
set +e  # Desactivar exit on error para capturar el código
eval $CMD
EXIT_CODE=$?
set -e  # Reactivar exit on error

# Verificar resultado
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    if [ "$CI_MODE" = false ]; then
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}✅ ¡Pipeline completado exitosamente!${NC}"
        echo -e "${GREEN}========================================${NC}"
    else
        echo "========================================"
        echo "✅ ¡Pipeline completado exitosamente!"
        echo "========================================"
    fi
    
    echo ""
    if [ "$CI_MODE" = false ]; then
        echo -e "${YELLOW}📁 Archivos generados:${NC}"
    else
        echo "📁 Archivos generados:"
    fi
    ls -la output/generated/ 2>/dev/null || echo "  (No se encontraron archivos)"
    echo ""
    
    # Mostrar log según opciones
    if [ "$SHOW_LOG" = true ]; then
        if [ -f "output/logs.txt" ]; then
            if [ "$CI_MODE" = false ]; then
                echo -e "${CYAN}📋 Log completo:${NC}"
                echo -e "${CYAN}----------------------------------------${NC}"
            else
                echo "📋 Log completo:"
                echo "----------------------------------------"
            fi
            cat output/logs.txt
            if [ "$CI_MODE" = false ]; then
                echo -e "${CYAN}----------------------------------------${NC}"
                echo -e "${CYAN}📄 Total de líneas: $(wc -l < output/logs.txt)${NC}"
            else
                echo "----------------------------------------"
                echo "📄 Total de líneas: $(wc -l < output/logs.txt)"
            fi
        else
            if [ "$CI_MODE" = false ]; then
                echo -e "${YELLOW}⚠️  No se encontró output/logs.txt${NC}"
            else
                echo "⚠️  No se encontró output/logs.txt"
            fi
        fi
    else
        if [ -f "output/logs.txt" ]; then
            if [ "$CI_MODE" = false ]; then
                echo -e "${YELLOW}📋 Últimas 10 líneas del log:${NC}"
                echo -e "${YELLOW}----------------------------------------${NC}"
            else
                echo "📋 Últimas 10 líneas del log:"
                echo "----------------------------------------"
            fi
            tail -10 output/logs.txt
            if [ "$CI_MODE" = false ]; then
                echo -e "${YELLOW}----------------------------------------${NC}"
                echo -e "${CYAN}💡 Para ver el log completo usa: ./run.sh --show-log${NC}"
                echo -e "${CYAN}💡 Para pasar --verbose a main.py: ./run.sh run --verbose${NC}"
            else
                echo "----------------------------------------"
                echo "💡 Para ver el log completo usa: ./run.sh --show-log"
                echo "💡 Para pasar --verbose a main.py: ./run.sh run --verbose"
            fi
        else
            echo "  (No se encontró output/logs.txt)"
        fi
    fi
else
    echo ""
    if [ "$CI_MODE" = false ]; then
        echo -e "${RED}========================================${NC}"
        echo -e "${RED}❌ Error durante la ejecución del pipeline${NC}"
        echo -e "${RED}========================================${NC}"
    else
        echo "========================================"
        echo "❌ Error durante la ejecución del pipeline"
        echo "========================================"
    fi
    echo ""
    if [ "$CI_MODE" = false ]; then
        echo -e "${YELLOW}📋 Comando fallido:${NC}"
        echo -e "  ${CYAN}$CMD${NC}"
        echo ""
        echo -e "${YELLOW}📋 Código de error: ${EXIT_CODE}${NC}"
        echo ""
        echo -e "${YELLOW}📋 Verifica el log para más detalles:${NC}"
    else
        echo "📋 Comando fallido:"
        echo "  $CMD"
        echo ""
        echo "📋 Código de error: $EXIT_CODE"
        echo ""
        echo "📋 Verifica el log para más detalles:"
    fi
    if [ -f "output/logs.txt" ]; then
        if [ "$CI_MODE" = false ]; then
            echo -e "${YELLOW}----------------------------------------${NC}"
        else
            echo "----------------------------------------"
        fi
        tail -30 output/logs.txt
        if [ "$CI_MODE" = false ]; then
            echo -e "${YELLOW}----------------------------------------${NC}"
            echo -e "${CYAN}💡 Log completo en: output/logs.txt${NC}"
        else
            echo "----------------------------------------"
            echo "💡 Log completo en: output/logs.txt"
        fi
    else
        echo "  (No se encontró output/logs.txt)"
        echo "  💡 Ejecuta el comando manualmente para ver el error:"
        echo "  ${CYAN}$CMD${NC}"
    fi
    exit $EXIT_CODE
fi
