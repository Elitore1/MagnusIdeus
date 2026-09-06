#!/usr/bin/env bash
# Utilidades generales

# Verificar si un archivo existe
check_file() {
    if [ -f "$1" ]; then
        return 0
    else
        return 1
    fi
}

# Verificar si un directorio existe
check_dir() {
    if [ -d "$1" ]; then
        return 0
    else
        return 1
    fi
}

# Verificar si un comando existe
check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Crear directorio si no existe
ensure_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo "✅ Directorio creado: $1"
    fi
}

# Mostrar mensaje con color (si está disponible)
print_msg() {
    local color="$1"
    local msg="$2"
    echo -e "${!color}${msg}${NC}"
}

# Mostrar error y salir
die() {
    print_msg RED "❌ Error: $1"
    exit 1
}

# Mostrar advertencia
warn() {
    print_msg YELLOW "⚠️  $1"
}

# Mostrar éxito
success() {
    print_msg GREEN "✅ $1"
}
