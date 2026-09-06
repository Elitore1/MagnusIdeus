# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### ✨ Próximas características

- [ ] Soporte para más tipos de datos (estructuras, uniones y enumeraciones).
- [ ] Mejorar el parser de C++ con un AST completo (templates y herencia).
- [ ] Más tests de integración con casos reales.
- [ ] Dashboard visual con métricas de traducción.

### 🔧 Mejoras planificadas

- [ ] Optimización de la generación de código.
- [ ] Soporte para herencia en C++.
- [ ] Interfaz web para pruebas interactivas.
- [ ] Exportación a otros lenguajes (Go, C# y Java).

### 🔒 Seguridad

- [ ] Auditar dependencias con `safety`.
- [ ] Implementar hooks de `pre-commit`.
- [ ] Configurar `codecov` con un umbral de cobertura.
- [ ] Activar CodeQL desde la configuración del repositorio.
- [x] Activar Secret Scanning y push protection en el repositorio.

---

## [2.0.0] - 2026-09-06

### ✨ Nuevas características

- **Pipeline modular**: reorganización completa en `scripts/lib/` con módulos
  reutilizables:
  - `colors.sh`: gestión de colores para la salida.
  - `utils.sh`: funciones de utilidad (`check_file`, `check_dir`, etc.).
  - `test_runner.sh`: lógica de ejecución de tests.
  - `pipeline.sh`: lógica del pipeline principal.
- **Wrapper `run.sh`**: CLI unificado con opciones avanzadas:
  - `--verbose` / `-v`: salida detallada.
  - `--show-log`: muestra el log completo al finalizar.
  - `--no-log`: oculta el log.
  - `--ci`: modo CI sin colores y con salida minimalista.
  - `--test-runner`: fuerza el runner de tests (`pytest`, `unittest` o `custom`).
  - `--help`: muestra la ayuda interactiva.
- **Soporte para un subconjunto de C++ simple**:
  - Clases con atributos y métodos.
  - Namespaces `std` básicos (`vector`, `chrono`, `map` y `thread`).
  - Tipos fundamentales (`string`, `int`, `float` y `bool`).
- **Tests automatizados**: suite de 14 tests para interpretación, generación y
  pipeline, compatible con `pytest`, `unittest` y el runner personalizado.
- **CI/CD con GitHub Actions**:
  - Jobs separados para build, tests y auditoría.
  - Python, Node.js y Rust configurados para validar el pipeline.
  - Cache de herramientas y carga de logs con retención limitada.
  - Acciones fijadas a SHA inmutables.
  - Badge de estado en el README.
- **GitHub Pages**: documentación visual en `docs/index.html`.
- **Dependabot**: configuración semanal para actualizaciones de GitHub Actions.

### 🔧 Mejoras

- **Modularización completa**: scripts separados por responsabilidad.
- **Logging mejorado**: timestamps y niveles (`STEP`, `OK`, `INFO`, `WARNING`,
  `ERROR`).
- **Generación de código**: Python, JavaScript y Rust con sintaxis correcta.
- **Mapeos mejorados**: `config/mappings.json` más completo y flexible.
- **Manejo de errores**: mensajes más explícitos y códigos de salida apropiados.
- **CI más eficiente**: triggers limitados a `main` y pull requests, con
  cancelación de ejecuciones redundantes.

### 🐛 Correcciones

- `print_summary` movido dentro de la clase `Interpreter`.
- Tests actualizados para generar los archivos antes de ejecutarlos.
- El wrapper raíz encuentra correctamente `scripts/run.sh`.
- Eliminado el uso de `eval` en scripts para ejecutar comandos de forma segura.

### 📚 Documentación

- README renovado con badges, ejemplos, limitaciones y guía de contribución.
- Sección «Auditoría y Seguridad» detallada.
- Guía de uso del wrapper `run.sh`.
- Ejemplos prácticos de generación de código.
- Demos visuales del pipeline en `docs/`.
- CHANGELOG con historial de versiones.

### 🗑️ Eliminado

- Scripts de depuración y archivos duplicados que ya no forman parte del
  pipeline público.
- Binarios generados de Rust del repositorio; ahora se ignoran mediante
  `.gitignore`.

---

## [1.0.0] - 2026-09-05

### ✨ Características iniciales

- Interpretación de C++ a AST.
- Generación de Python, JavaScript y Rust.
- Sistema de mapeos básico (`config/mappings.json`).
- Pipeline con `bridge/interpreter.py` y `bridge/generator.py`.
- Logging básico en `output/logs.txt`.

### 🔧 Estructura inicial

- `bridge/`: módulos principales.
- `config/`: configuración y mapeos.
- `src/`: código fuente de ejemplo.
- `output/generated/`: código generado.

### 🐛 Limitaciones conocidas

- Parser basado en regex, limitado a un subconjunto de C++ simple.
- No soporta templates ni herencia múltiple.
- Los atributos complejos no se extraen correctamente.

---

[Unreleased]: https://github.com/Elitore1/MagnusIdeus/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Elitore1/MagnusIdeus/releases/tag/v2.0.0
[1.0.0]: https://github.com/Elitore1/MagnusIdeus/releases/tag/v1.0.0
