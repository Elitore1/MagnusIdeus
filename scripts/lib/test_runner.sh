#!/usr/bin/env bash
# Lógica de ejecución de tests

# Detectar y ejecutar tests
run_tests() {
    local test_runner="${1:-auto}"
    
    echo ""
    if [ "$CI_MODE" = false ]; then
        echo -e "${MAGENTA}🧪 EJECUTANDO TESTS${NC}"
        echo -e "${MAGENTA}========================================${NC}"
    else
        echo "🧪 EJECUTANDO TESTS"
        echo "========================================"
    fi
    
    local runner=""
    local test_exit=0
    
    # Determinar runner
    case "$test_runner" in
        pytest)
            runner="pytest"
            ;;
        unittest)
            runner="unittest"
            ;;
        custom)
            runner="custom"
            ;;
        auto|*)
            runner=$(detect_test_runner)
            ;;
    esac
    
    echo "🔍 Usando runner: $runner"
    
    # Ejecutar según el runner
    case $runner in
        pytest)
            run_pytest
            test_exit=$?
            ;;
        unittest)
            run_unittest
            test_exit=$?
            ;;
        custom)
            run_custom
            test_exit=$?
            ;;
        *)
            echo "⚠️ Runner desconocido: $runner"
            test_exit=1
            ;;
    esac
    
    return $test_exit
}

# Detectar el mejor runner disponible
detect_test_runner() {
    if check_command pytest && { check_file "pytest.ini" || check_dir "tests"; }; then
        echo "pytest"
    elif check_file "tests/run_tests.py"; then
        echo "custom"
    elif check_dir "tests" && find tests -name "test_*.py" | grep -q .; then
        echo "unittest"
    else
        echo "unittest"
    fi
}

# Ejecutar tests con pytest
run_pytest() {
    if [ -f "pytest.ini" ]; then
        echo "📋 Usando configuración: pytest.ini"
    fi
    pytest tests/ -v --tb=short --color=yes
    return $?
}

# Ejecutar tests con unittest
run_unittest() {
    if check_dir "tests"; then
        python3 -m unittest discover -s tests -p "test_*.py" -v
    else
        python3 -m unittest discover -p "test_*.py" -v
    fi
    return $?
}

# Ejecutar tests personalizados
run_custom() {
    python3 tests/run_tests.py
    return $?
}
