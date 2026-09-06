# 🧠 Esclarificador

**"De C++ a Python, JavaScript y Rust, sin perder la cabeza."**

---

## 🤔 ¿Qué es esto?

Imagina que escribes un programa en C++ y quieres ver cómo se vería en Python, JavaScript o Rust. Normalmente tendrías que traducirlo a mano, línea por línea.

**Esclarificador** hace esa traducción por ti. No es perfecto, pero es un comienzo. Y lo mejor: **aprende mientras lo usas**.

---

## 🎯 ¿Qué hace exactamente?

1. **Lee** tu código C++ (por ahora, clases simples con métodos y atributos).
2. **Interpreta** ese código y lo convierte en una estructura intermedia (AST).
3. **Genera** código equivalente en:
   - 🐍 Python
   - 📜 JavaScript
   - 🦀 Rust
4. **Ejecuta** el código generado para que veas que funciona.

---

## 🧱 ¿Cómo está organizado?
esclarificador/
├── bridge/ # ✅ El cerebro del proyecto (ACTIVO)
│ ├── interpreter.py # Lee C++ y crea un AST
│ ├── generator.py # Convierte el AST en código
│ └── main.py # Punto de entrada unificado (NUEVO)
├── config/
│ └── mappings.json # Aquí defines cómo se traduce cada cosa
├── src/
│ └── idea.cpp # El código C++ que quieres traducir
├── output/
│ └── generated/ # Aquí aparecen los archivos generados
│ ├── idea.py
│ ├── idea.js
│ └── idea.rs
└── README.md # Esto que estás leyendo

**Nota:** `run.sh` y `commands.sh` ya no se usan. Todo se maneja desde `bridge/main.py`.

---

## 🚀 ¿Cómo lo uso?

### 1. Clona el repositorio



git clone https://github.com/tu-usuario/esclarificador.git
cd esclarificador
2. Asegúrate de tener lo necesario

    Python 3.8 o superior

    (Opcional) Node.js para ejecutar JavaScript

    (Opcional) Rust para compilar y ejecutar Rust

3. Ejecuta el pipeline completo

python3 bridge/main.py run

Este comando hace todo automáticamente:

    Lee src/idea.cpp

    Genera los archivos en output/generated/

    Ejecuta el código generado
    
4. Comandos disponibles

# Pipeline completo
python3 bridge/main.py run

# Solo interpretar (C++ → AST)
python3 bridge/main.py interpret

# Generar un lenguaje específico
python3 bridge/main.py generate --lang python
python3 bridge/main.py generate --lang js
python3 bridge/main.py generate --lang rust

# Compilar Rust
python3 bridge/main.py compile

# Limpiar archivos generados
python3 bridge/main.py clean

# Ver ayuda
python3 bridge/main.py --help

5. Explora los resultados

# Ver el código Python generado
cat output/generated/idea.py

# Ver el código JavaScript generado
cat output/generated/idea.js

# Ver el código Rust generado
cat output/generated/idea.rs

# Ejecutar Python
python3 output/generated/idea.py

# Ejecutar JavaScript
node output/generated/idea.js

# Compilar y ejecutar Rust
rustc output/generated/idea.rs -o output/generated/idea
./output/generated/idea

🧪 ¿Cómo personalizo la traducción?

El archivo config/mappings.json es el diccionario que usa Esclarificador para traducir.

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



Si quieres que una clase C++ se llame diferente en Python, solo cambias el valor de "python". Fácil.


📖 Ejemplo práctico
Entrada (src/idea.cpp)

class Tanger {
public:
    std::string problema = "renderizado_3d";
    void diagnosticar() { std::cout << "Problema identificado\n"; }
};

Salida (Python)


class Problem:
    def __init__(self):
        self.problema = ""
    def diagnosticar(self):
        print("🔍 Diagnosticando Tanger...")
        return True
        
        
Salida (JavaScript)


class Problem {
    constructor() {
        this.problema = "";
    }
    diagnosticar() {
        console.log("🔍 Diagnosticando Tanger...");
        return true;
    }
}



Salida (Rust)

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




📊 Logs

El pipeline registra cada paso en output/logs.txt:



[2026-09-06 05:56:59] [INFO] === NUEVA EJECUCIÓN ===
[2026-09-06 05:56:59] [STEP] 📖 PASO 1: Interpretando C++...
[2026-09-06 05:56:59] [OK] ✅ AST generado con 5 abstracciones
[2026-09-06 05:56:59] [STEP] 🔧 PASO 2: Generando código...
[2026-09-06 05:56:59] [OK] ✅ Código python generado
[2026-09-06 05:56:59] [STEP] 🦀 PASO 3: Compilando Rust...
[2026-09-06 05:57:00] [OK] ✅ Binario generado
[2026-09-06 05:57:00] [STEP] ▶️ PASO 4: Ejecutando ejemplos...
[2026-09-06 05:57:00] [OK] ✅ ¡Pipeline completado!




⚠️ ¿Qué NO puede hacer (todavía)?

    ❌ Leer C++ complejo con templates o herencia múltiple.

    ❌ Traducir código con punteros o referencias complejas.

    ❌ Entender #include más allá de los namespaces básicos.

    ❌ Generar código con la lógica exacta de los métodos originales.

Pero sí puede traducir la estructura de tus clases, y eso ya es un montón.




🧠 ¿Cómo aprendo más?

Este proyecto está diseñado para que puedas meterle mano sin miedo.

    Si quieres entender cómo se interpreta el código, abre bridge/interpreter.py.

    Si quieres modificar cómo se genera el código, abre bridge/generator.py.

    Si quieres agregar un nuevo lenguaje, mira cómo funciona generator.py y agrega tu propio método _generate_tu_lenguaje().
    
    
    
    
🤝 ¿Quieres contribuir?

¡Bienvenido! Esto es un proyecto abierto. Puedes:

    Hacer un fork

    Crear una rama (git checkout -b mi-mejora)

    Hacer tus cambios

    Hacer un pull request
    
    
    
    
📄 Licencia

MIT License. Puedes usarlo, modificarlo y compartirlo libremente.

Esclarificador — Un proyecto para aprender, experimentar y divertirse.
