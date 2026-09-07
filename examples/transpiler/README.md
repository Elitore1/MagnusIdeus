# Ejemplos para el transpiler: C++, Python, JavaScript y Rust

Este directorio contiene ejemplos mínimos que muestran cómo representar:
- Clase abstracta (molde)
- Instancia (objeto)
- Herencia
- Polimorfismo
- Sobrescritura (override)

Archivos:
- ejemplo.cpp  - Ejemplo en C++
- ejemplo.py   - Ejemplo en Python
- ejemplo.js   - Ejemplo en JavaScript (ES6)
- ejemplo.rs   - Ejemplo en Rust

Cómo ejecutar cada ejemplo:

C++ (requiere g++ o clang):

```bash
# Compilar
g++ -std=c++17 examples/transpiler/ejemplo.cpp -o ejemplo_cpp
# Ejecutar
./ejemplo_cpp
```

Python (requiere Python 3.8+):

```bash
python3 examples/transpiler/ejemplo.py
```

JavaScript (Node.js):

```bash
node examples/transpiler/ejemplo.js
```

Rust (requiere rustc o cargo):

Usando rustc:

```bash
rustc examples/transpiler/ejemplo.rs -o ejemplo_rs
./ejemplo_rs
```

Usando cargo (crear un proyecto si es necesario):

```bash
# dentro de un proyecto cargo, mover el archivo a src/main.rs o ajustar
cargo run
```

Propósito
--------
Estos ejemplos sirven como referencia para las transformaciones que tu transpiler debe realizar al convertir C++ a Python/JS/Rust, y muestran correspondencias de conceptos entre lenguajes (abstract classes, virtual methods, trait objects, etc.).
