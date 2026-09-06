# Changelog

## [v2.0.0] - 2026-09-06

Primera versión pública del transpilador experimental.

### Añadido

- Pipeline C++ → AST → Python, JavaScript y Rust.
- Mappings configurables para abstracciones, namespaces y tipos.
- Wrapper `./run.sh` con modos de ejecución, CI y tests.
- Suite automatizada para intérprete, generador y pipeline.
- Workflow de GitHub Actions para validar cada push y pull request.
- Documentación del proyecto y demos visuales del pipeline.

### Alcance

Esta versión representa la transición desde el prototipo conceptual hacia un
transpilador experimental reproducible. Soporta un subconjunto de C++ simple;
no pretende traducir proyectos C++ completos.
