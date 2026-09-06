#!/usr/bin/env bash
# Lógica del pipeline

# Verificar y crear archivos de ejemplo
ensure_example_files() {
    # Verificar src/idea.cpp
    if ! check_file "src/idea.cpp"; then
        warn "No se encuentra src/idea.cpp - Creando archivo de ejemplo..."
        mkdir -p src
        cat > src/idea.cpp << 'CPPEOF'
#include <iostream>
#include <chrono>
#include <vector>

class Tanger {
public:
    std::string problema = "renderizado_3d";
    void diagnosticar() { std::cout << "Problema identificado\n"; }
};

class Espejo {
public:
    void analizar(Tanger& t) { std::cout << "Analizando: " << t.problema << "\n"; }
};

class Modulus {
public:
    std::string traducir(const std::string& idea) {
        return "TRADUCIDO:" + idea;
    }
};

class Cayo {
public:
    std::vector<std::string> pasos;
    void planificar() { pasos.push_back("paso_1"); }
};

class Barca {
public:
    void ejecutar() { std::cout << "Ejecutando...\n"; }
};
CPPEOF
        success "src/idea.cpp creado"
    fi
    
    # Verificar config/mappings.json
    if ! check_file "config/mappings.json"; then
        warn "No se encuentra config/mappings.json - Creando archivo de configuración..."
        mkdir -p config
        cat > config/mappings.json << 'JSONEOF'
{
  "version": "1.0",
  "abstracciones": {
    "Tanger": {
      "descripcion": "Identificación del problema",
      "python": "Problem",
      "js": "Problem",
      "rust": "Problem"
    },
    "Espejo": {
      "descripcion": "Análisis y reflexión",
      "python": "Reflect",
      "js": "Reflect",
      "rust": "Reflect"
    },
    "Modulus": {
      "descripcion": "Puente entre idea y lógica",
      "python": "Bridge",
      "js": "Bridge",
      "rust": "Bridge"
    },
    "Cayo": {
      "descripcion": "Planificación",
      "python": "Plan",
      "js": "Plan",
      "rust": "Plan"
    },
    "Barca": {
      "descripcion": "Ejecución irreversible",
      "python": "Execute",
      "js": "Execute",
      "rust": "Execute"
    }
  },
  "std_namespaces": {
    "chrono": {"python": "datetime", "js": "Date", "rust": "std::time"},
    "vector": {"python": "list", "js": "Array", "rust": "std::vec::Vec"}
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
        success "config/mappings.json creado"
    fi
}

# Ejecutar pipeline
run_pipeline() {
    local verbose="${1:-false}"
    
    # Crear directorios
    ensure_dir "intermediate"
    ensure_dir "output/generated"
    
    # Verificar Python
    if ! check_command python3; then
        die "python3 no está instalado"
    fi
    
    # Mantener los argumentos como una lista para preservar el quoting y
    # permitir comandos distintos de run desde el wrapper.
    local args=("${BRIDGE_ARGS[@]}")
    if [ ${#args[@]} -eq 0 ]; then
        args=("run")
    fi
    local cmd_display="python3 bridge/main.py ${args[*]}"
    
    # Ejecutar
    echo ""
    echo "📋 Ejecutando pipeline..."
    echo "▶️ $cmd_display"
    echo ""
    
    python3 bridge/main.py "${args[@]}"
}
