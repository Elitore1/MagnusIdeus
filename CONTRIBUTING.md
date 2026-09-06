# Contribuir a Esclarificador

Gracias por tu interés en mejorar Esclarificador. El proyecto es un
transpilador experimental que soporta un subconjunto de C++ simple.

## Flujo de trabajo

1. Creá un fork y una rama descriptiva para tu cambio.
2. Mantené los cambios enfocados y documentá cualquier modificación de
   comportamiento.
3. Ejecutá la suite antes de abrir el pull request:

   ```bash
   ./run.sh --ci test
   ```

4. Añadí o actualizá tests cuando cambies el intérprete, el AST, los
   generadores o el pipeline.
5. Abrí un pull request explicando qué cambió y cómo se validó.

## Criterios para los pull requests

- No incluir secretos, binarios ni archivos generados.
- Mantener compatibilidad con el wrapper `./run.sh`.
- Usar mensajes de error y documentación coherentes con el proyecto.
- Confirmar que los checks de CI pasan antes de solicitar la revisión.

Para cambios grandes en el parser o nuevos lenguajes de salida, explicá primero
el alcance y añadí un ejemplo reproducible.
