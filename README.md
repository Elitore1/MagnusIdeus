# Esclarificador

De C++ a Python, JavaScript y Rust, sin perder la cabeza.

Esclarificador soporta un **subconjunto de C++ simple**, principalmente clases con atributos, métodos e includes básicos, y genera código equivalente en otros lenguajes. No es un compilador completo: es un transpilador experimental para aprender y experimentar.

## Qué hace

1. **Lee** tu código C++ (clases con métodos y atributos).
2. **Interpreta** ese código y lo convierte en un AST.
3. **Genera** código equivalente en Python, JavaScript y Rust.
4. **Ejecuta** lo generado para comprobar que corre.

## Cómo está organizado

```
esclarificador/
├── bridge/                 ←  cerebro del proyecto (activo)
│   ├── interpreter.py      ←  lee C++ y crea un AST
│   ├── generator.py        ←  convierte el AST en código
│   └── main.py             ←  punto de entrada unificado
├── config/
│   └── mappings.json       ←  cómo se traduce cada cosa
├── src/
│   └── idea.cpp            ←  el C++ que quieres traducir
├── output/
│   └── generated/          ←  archivos generados
│       ├── idea.py
│       ├── idea.js
│       └── idea.rs
└── README.md               ←  esto que estás leyendo
```

El punto de entrada es `./run.sh`, que ejecuta el pipeline completo.

## Cómo usarlo

### Requisitos

- Python 3.8 o superior
- Node.js (opcional, para ejecutar JavaScript)
- Rust / `rustc` (opcional, para compilar y ejecutar Rust)

### Pipeline completo

Desde la raíz del repositorio:


git clone https://github.com/Elitore1/MagnusIdeus.git
cd esclarificador
2. Asegúrate de tener lo necesario

    Python 3.8 o superior

    (Opcional) Node.js para ejecutar JavaScript

    (Opcional) Rust para compilar y ejecutar Rust

3. Ejecuta el pipeline completo


./run.sh
```

Eso lee `src/idea.cpp`, genera archivos en `output/generated/` y los ejecuta.

### Wrapper `run.sh`

El wrapper raíz delega en `scripts/run.sh` y ofrece una forma cómoda de ejecutar
el pipeline y sus verificaciones:

```bash
./run.sh                  # Pipeline completo
./run.sh --verbose        # Pipeline con salida detallada
./run.sh --show-log       # Muestra el log completo al finalizar
./run.sh --ci test        # Ejecuta los tests en modo CI
./run.sh --test-runner unittest test
```

`--test-runner` acepta `auto`, `pytest`, `unittest` o `custom`. En modo `auto`
se elige el runner disponible según los archivos del proyecto. El workflow de
GitHub Actions ejecuta `./run.sh --ci test` en cada push y pull request.

### Comandos

| Comando | Qué hace |
|---|---|
| `./run.sh` | Pipeline completo |
| `./run.sh interpret` | C++ → AST |
| `./run.sh generate --lang python` | Genera Python |
| `./run.sh generate --lang js` | Genera JavaScript |
| `./run.sh generate --lang rust` | Genera Rust |
| `./run.sh compile` | Compila el Rust generado |
| `./run.sh clean` | Limpia generados y el log |
| `./run.sh --help` | Ayuda |

### Resultados

```bash
python3 output/generated/idea.py
node output/generated/idea.js
rustc output/generated/idea.rs -o output/generated/idea
./output/generated/idea
```

## Personalizar la traducción

`config/mappings.json` es el diccionario de traducción. Si una clase C++ debe llamarse distinto en Python, cambia el valor de `"python"`:

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

## Ejemplo

**Entrada** (`src/idea.cpp`):

```cpp
class Tanger {
public:
    std::string problema = "renderizado_3d";
    void diagnosticar() { std::cout << "Problema identificado\n"; }
};
```

**Salida Python:**

```python
class Problem:
    def __init__(self):
        self.problema = ""
    def diagnosticar(self):
        print("🔍 Diagnosticando Tanger...")
        return True
```

**Salida JavaScript:**

```javascript
class Problem {
    constructor() {
        this.problema = "";
    }
    diagnosticar() {
        console.log("🔍 Diagnosticando Tanger...");
        return true;
    }
}
```

**Salida Rust:**

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

## Logs

Cada corrida del pipeline queda en `output/logs.txt`:

```
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

## Alcance y limitaciones

El proyecto soporta un **subconjunto de C++ simple**. Está pensado para ejemplos
educativos y prototipos, no para traducir proyectos C++ completos.

- Leer C++ complejo con templates o herencia múltiple
- Traducir punteros o referencias complejas
- Entender `#include` más allá de los namespaces básicos
- Regenerar la lógica exacta de los métodos originales

Sí traduce la **estructura** de las clases (nombres, atributos, métodos y mapeos).

## Dónde meterle mano

- Interpretación: `bridge/interpreter.py`
- Generación: `bridge/generator.py`
- Un lenguaje nuevo: copiá el patrón de `_generate_python` / `_generate_javascript` / `_generate_rust`

## Contribuir

Fork, rama (`git checkout -b mi-mejora`), cambios y pull request.

## Licencia

MIT. Podés usarlo, modificarlo y compartirlo.

Esclarificador — un proyecto para aprender, experimentar y divertirse.
