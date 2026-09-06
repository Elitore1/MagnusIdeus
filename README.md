# 🧠 Esclarificador

**"De C++ a Python, JavaScript y Rust, sin perder la cabeza."**

[![CI](https://github.com/Elitore1/MagnusIdeus/actions/workflows/ci.yml/badge.svg)](https://github.com/Elitore1/MagnusIdeus/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Rust 1.70+](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)
[![Node.js 16+](https://img.shields.io/badge/node-16+-green.svg)](https://nodejs.org/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Online-brightgreen)](https://elitore1.github.io/MagnusIdeus/)
[![codecov](https://codecov.io/gh/Elitore1/MagnusIdeus/branch/main/graph/badge.svg)](https://codecov.io/gh/Elitore1/MagnusIdeus)

---

Esclarificador soporta un **subconjunto de C++ simple**, principalmente clases con atributos, métodos e includes básicos, y genera código equivalente en otros lenguajes. No es un compilador completo: es un transpilador experimental para aprender y experimentar.

---
# Esclarificador

De C++ a Python, JavaScript y Rust, sin perder la cabeza.

[![CI](https://github.com/Elitore1/MagnusIdeus/actions/workflows/ci.yml/badge.svg)](https://github.com/Elitore1/MagnusIdeus/actions/workflows/ci.yml)

---

## 🎥 Demo del Pipeline

![Pipeline en acción](docs/Peek%202026-09-06%2009-20.gif)
![Pipeline en acción X2](docs/Peek%202026-09-06%2009-24.gif)




## 📋 Tabla de Contenidos

- [Qué hace](#qué-hace)
- [Cómo está organizado](#cómo-está-organizado)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Wrapper `run.sh`](#wrapper-run.sh)
- [Comandos Disponibles](#comandos-disponibles)
- [Tests](#tests)
- [Personalizar la Traducción](#personalizar-la-traducción)
- [Ejemplo](#ejemplo)
- [Logs](#logs)
- [Alcance y Limitaciones](#alcance-y-limitaciones)
- [Dónde Meterle Mano](#dónde-meterle-mano)
- [Contribuir](#contribuir)
- [Historial de cambios](#historial-de-cambios)
- [Licencia](#licencia)

---

## 🎯 Qué hace

1. **Lee** tu código C++ (clases con métodos y atributos).
2. **Interpreta** ese código y lo convierte en un AST.
3. **Genera** código equivalente en Python, JavaScript y Rust.
4. **Ejecuta** lo generado para comprobar que corre.

---

## 🧱 Cómo está organizado

```text
esclarificador/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD con GitHub Actions
├── bridge/                         # 🧠 Cerebro del proyecto
│   ├── interpreter.py              # Lee C++ y crea un AST
│   ├── generator.py                # Convierte el AST en código
│   ├── main.py                     # Punto de entrada del pipeline
│   └── tokenizer.py                # Extrae tokens de C++
├── scripts/                        # 🛠️ Scripts modulares
│   ├── run.sh                      # Wrapper principal
│   └── lib/
│       ├── colors.sh               # Colores de salida
│       ├── utils.sh                # Utilidades generales
│       ├── test_runner.sh          # Lógica de tests
│       └── pipeline.sh             # Lógica del pipeline
├── tests/                          # 🧪 Tests automatizados
│   ├── test_interpreter.py
│   ├── test_generator.py
│   ├── test_pipeline.py
│   └── run_tests.py
├── config/
│   └── mappings.json               # Reglas de traducción
├── src/
│   └── idea.cpp                    # Código C++ de entrada
├── output/
│   └── generated/                  # Código generado
│       ├── idea.py
│       ├── idea.js
│       ├── idea.rs
│       └── .gitkeep
├── docs/                           # GitHub Pages y demos
│   ├── _config.yml
│   ├── index.html
│   └── *.gif
├── CHANGELOG.md                    # Historial de versiones
├── CONTRIBUTING.md                 # Guía para contribuir
├── run.sh                          # Enlace a scripts/run.sh
├── LICENSE
└── README.md
```


El punto de entrada es `./run.sh`, que ejecuta el pipeline completo.

---

## 🔧 Requisitos

- Python 3.8 o superior
- Node.js (opcional, para ejecutar JavaScript)
- Rust / `rustc` (opcional, para compilar y ejecutar Rust)

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Elitore1/MagnusIdeus.git
cd MagnusIdeus

# Dar permisos de ejecución al wrapper
chmod +x run.sh

# Ejecutar el pipeline completo
./run.sh
```

## 🚀 Uso Rápido

```bash

# Pipeline completo (interpreta, genera, compila y ejecuta)
./run.sh

# Pipeline con salida detallada
./run.sh --verbose

# Pipeline en modo CI (sin colores)
./run.sh --ci run

# Ver el log completo al finalizar
./run.sh --show-log
```

## 🛠️ Wrapper `run.sh`

El wrapper raíz delega en scripts/run.sh y ofrece una forma cómoda de ejecutar el pipeline y sus verificaciones.
### Opciones del wrapper

| Opción | Qué hace |
|---|---|
| `--help`, `-h` | Muestra ayuda y ejemplos |
| `--show-log` | Muestra el log completo al finalizar |
| `--no-log` | No muestra el log al finalizar |
| `--verbose`, `-v` | Modo detallado |
| `--ci` | Modo CI sin colores |
| `--test-runner` | Fuerza `pytest`, `unittest` o `custom` |

### Ejemplos

```bash

./run.sh                  # Pipeline completo
./run.sh --verbose        # Pipeline con salida detallada
./run.sh --show-log       # Muestra el log completo al finalizar
./run.sh --ci test        # Ejecuta los tests en modo CI
./run.sh --test-runner unittest test
./run.sh --help           # Muestra ayuda
```

--test-runner acepta `auto`, `pytest`, `unittest` o `custom`. En modo `auto`
se elige el runner disponible según los archivos del proyecto.

## 📋 Comandos Disponibles

| Comando | Qué hace |
|---|---|
| `./run.sh` | Pipeline completo |
| `./run.sh interpret` | C++ → AST |
| `./run.sh generate --lang python` | Genera Python |
| `./run.sh generate --lang js` | Genera JavaScript |
| `./run.sh generate --lang rust` | Genera Rust |
| `./run.sh compile` | Compila el Rust generado |
| `./run.sh clean` | Limpia generados y el log |
| `./run.sh test` | Ejecuta tests |
| `./run.sh --help` | Ayuda |

### Ejecutar resultados

```bash

python3 output/generated/idea.py       # Ejecutar Python
node output/generated/idea.js          # Ejecutar JavaScript
rustc output/generated/idea.rs -o output/generated/idea  # Compilar Rust
./output/generated/idea                # Ejecutar Rust
```

## 🧪 Tests

El proyecto incluye una suite de tests automatizados que validan:

    Carga de mappings

    Lectura de código C++

    Extracción de tokens

    Generación del AST

    Generación de código en Python, JavaScript y Rust

    Ejecución del código generado

### Ejecutar tests

```bash

# Auto-detección del runner
./run.sh test

# Forzar pytest
./run.sh test --test-runner pytest

# Forzar unittest
./run.sh test --test-runner unittest

# Modo CI
./run.sh --ci test
```

### Cobertura actual

| Test | Estado |
|---|---|
| Carga de mappings | ✅ |
| Lectura de C++ | ✅ |
| Extracción de tokens | ✅ |
| Generación de AST | ✅ |
| Generación Python | ✅ |
| Generación JavaScript | ✅ |
| Generación Rust | ✅ |
| Ejecución Python | ✅ |

La ejecución de JavaScript y la compilación/ejecución de Rust se validan en el
pipeline completo y en CI cuando las herramientas están disponibles.

## 🧪 Personalizar la Traducción

config/mappings.json es el diccionario de traducción. Si una clase C++ debe llamarse distinto en Python, cambia el valor de `"python"`:

```json

{
  "abstracciones": {
    "Tanger": {
      "descripcion": "Identificación del problema",
      "python": "Problem",
      "js": "Problem",
      "rust": "Problem"
    }
  },
  "std_namespaces": {
    "vector": {
      "python": "list",
      "js": "Array",
      "rust": "std::vec::Vec"
    }
  }
}
```

## 📖 Ejemplo

Entrada (`src/idea.cpp`):

```cpp

class Tanger {
public:
    std::string problema = "renderizado_3d";
    void diagnosticar() { std::cout << "Problema identificado\n"; }
};
```

Salida Python:

```python

class Problem:
    def __init__(self):
        self.problema = ""
    def diagnosticar(self):
        print("🔍 Diagnosticando Tanger...")
        return True
```

Salida JavaScript:

```javascript

class Problem {
    constructor() {
        this.problema = "";
    }
    ```
    diagnosticar() {
        console.log("🔍 Diagnosticando Tanger...");
        return true;
    }
}

Salida Rust:

```rust

struct Problem {
    problema: String,
}
impl Problem {
    fn new() -> Self {
        Self {
            problema: String::from(""),
        }
    }
    fn diagnosticar(&self) {
        println!("🔍 Diagnosticando Problem...");
    }
}
```

## 📊 Logs

Cada corrida del pipeline queda en `output/logs.txt`:

```text

[2026-09-06 05:56:59] [INFO] === NUEVA EJECUCIÓN ===
[2026-09-06 05:56:59] [STEP] PASO 1: Interpretando C++...
[2026-09-06 05:56:59] [OK] AST generado con 5 abstracciones
[2026-09-06 05:56:59] [STEP] PASO 2: Generando código...
[2026-09-06 05:56:59] [OK] Código python generado
[2026-09-06 05:56:59] [STEP] PASO 3: Compilando Rust...
[2026-09-06 05:57:00] [OK] Binario generado
[2026-09-06 05:57:00] [STEP] PASO 4: Ejecutando ejemplos...
[2026-09-06 05:57:00] [OK] Pipeline completado
```

⚠️ Alcance y Limitaciones

El proyecto soporta un subconjunto de C++ simple. Está pensado para ejemplos educativos y prototipos, no para traducir proyectos C++ completos.

NO soporta:

    ❌ Templates o herencia múltiple

    ❌ Punteros o referencias complejas

    ❌ #include más allá de namespaces básicos

    ❌ Lógica exacta de los métodos originales

SÍ soporta:

    ✅ Estructura de clases (nombres, atributos, métodos)

    ✅ Mapeos configurables

    ✅ Generación en 3 lenguajes

🧠 Dónde Meterle Mano

    Interpretación: bridge/interpreter.py

    Generación: bridge/generator.py

    Nuevo lenguaje: copiá el patrón de _generate_python / _generate_javascript / _generate_rust

    Wrapper: scripts/run.sh y scripts/lib/

    Tests: tests/

🤝 Contribuir

1. Hacé fork del repositorio y creá una rama (`git checkout -b mi-mejora`).
2. Ejecutá `./run.sh --ci test` antes de enviar cambios.
3. Documentá los cambios relevantes y abrí un pull request.

Para nuevas funcionalidades del parser o generador, añadí tests que cubran el
caso normal y sus entradas límite.

## Licencia

El proyecto se distribuye bajo la licencia MIT. Consultá `LICENSE` para conocer
los permisos y condiciones completos.

Consultá `CHANGELOG.md` para conocer la evolución del proyecto.

## Historial de cambios

El historial completo de versiones y cambios está disponible en
[`CHANGELOG.md`](CHANGELOG.md).

Para contribuir al proyecto, consultá también
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## 🔒 Auditoría y Seguridad

El proyecto utiliza **CI/CD con auditoría de dependencias y detección de
secretos**. Las acciones del workflow principal están fijadas a versiones
concretas y la acción de Rust está fijada a un SHA inmutable para reducir el
riesgo de supply chain.

| Herramienta | Propósito | Estado |
|---|---|---|
| GitHub Actions | CI/CD | ✅ Versiones fijadas; Rust fijado a SHA |
| Dependabot | Actualizaciones de Actions | ✅ Configurado semanalmente |
| CodeQL | Análisis de seguridad | ⚙️ Activar en **Settings → Code security** |
| Secret scanning | Detección de secretos | ✅ Activo con push protection |
| Auditoría CI | Patrones de secretos y dependencias | ✅ Ejecutada en cada workflow |

### Buenas prácticas implementadas

- ✅ No se detectaron secretos en los archivos rastreados.
- ✅ `.gitignore` excluye archivos sensibles, binarios y temporales.
- ✅ Los scripts no contienen credenciales.
- ✅ El workflow usa `contents: read` y no solicita permisos de escritura.
- ✅ Los logs y artefactos publicados se limitan a `output/logs.txt`.
- ✅ Las dependencias se auditan con `pip-audit`, `npm audit` o `cargo audit`
  cuando existen manifiestos para el ecosistema correspondiente.

Secret Scanning y push protection están activos en el repositorio. CodeQL es una
función de seguridad de GitHub que todavía debe habilitarse desde la
configuración del repositorio.

📄 Licencia

MIT License. Podés usarlo, modificarlo y compartirlo libremente.

Esclarificador — un proyecto para aprender, experimentar y divertirse. 🚀
