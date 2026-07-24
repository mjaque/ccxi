[← Volver al índice](indice.md)

# Copias de Seguridad — ccxi

## 12.1 Qué se guarda

Cada módulo de CCxI es un único archivo **SQLite independiente** almacenado en `data/<nombre>.sqlite`. No hay una base de datos central ni archivos de configuración externos: todo el contenido de un módulo (estudiantes, resultados, indicadores, actividades, calificaciones) está dentro de ese archivo.

Por tanto, para hacer una copia de seguridad completa de un módulo basta con copiar su archivo `.sqlite`.

## 12.2 Cómo hacer una copia de seguridad

1. **Detén la aplicación** (cierra el servidor o espera a que nadie la esté usando)
2. Copia el archivo `data/<nombre>.sqlite` a la ubicación deseada:
   - Puedes usar el directorio `backups/` incluido en la aplicación
   - O cualquier otra ubicación (nube, disco externo, etc.)
3. Opcionalmente, renómbralo para identificar la fecha de la copia, por ejemplo:
   - `DAW1-PROG-2026-07-24.sqlite`

Puedes copiar todo el directorio `data/` si quieres respaldar todos los módulos a la vez.

## 12.3 Cómo restaurar una copia

1. **Detén la aplicación**
2. Copia el archivo `.sqlite` desde la copia de seguridad a `data/`
3. Si ya existe un módulo con el mismo nombre, la aplicación lo rechazará al crearlo; puedes sobrescribir el archivo existente o eliminar el viejo antes de copiar
4. Arranca la aplicación
5. El módulo restaurado aparecerá en el desplegable del panel superior

Si el archivo no es válido (no pertenece a CCxI o está dañado), la aplicación no lo mostrará en el listado de módulos.

## 12.4 Directorio `backups/`

La aplicación incluye un directorio `backups/` preparado para almacenar las copias de seguridad. Este directorio está excluido del control de versiones, por lo que los archivos que guardes ahí no se subirán accidentalmente a un repositorio.

## 12.5 Verificación de integridad

Al listar los módulos, la aplicación comprueba automáticamente que cada archivo `.sqlite` en `data/` tenga la estructura correcta (las 8 tablas necesarias y la marca de identificación de CCxI). Si un archivo no pasa esta verificación, se ignora y no aparece en el desplegable.

Esto significa que si restauras un archivo dañado o incompatible, lo sabrás inmediatamente porque el módulo no estará disponible.

## 12.6 Consejos prácticos

- Incluye la **fecha** en el nombre del archivo de la copia para identificar cuándo se hizo
- No uses la aplicación mientras realizas la copia para evitar corrupción de datos
- Después de restaurar, comprueba que el módulo aparece en el desplegable y que los datos son correctos
- Mantén copias en **ubicaciones separadas** (nube, disco externo, otro ordenador) para protegerte ante fallos del disco principal
- Programa recordatorios periódicos para hacer copias (inicio/fin de evaluación, semanalmente, etc.)

## 12.7 Limitaciones

- No hay **interfaz gráfica** para hacer o restaurar copias: el proceso es completamente manual
- No hay **copias automáticas** programadas
- No hay **compresión** ni **cifrado** de las copias
- No hay **historial de versiones**: cada copia sobrescribe el archivo anterior si usas el mismo nombre
