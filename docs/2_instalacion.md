[Volver al índice](1_objetivo.md)

## 2. Instalación y puesta en marcha

### Requisitos

- Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

### Instalación

- Descarga o clona el repositorio:

   ```bash
   git clone https://github.com/mjaque/ccxi
   cd ccxi
   ```

- No requiere instalar librerías externas — todo el stack usa la biblioteca estándar de Python.

### Arranque

En Windows:

```bash
	start-windows.bat
```

En Linux:

```bash
	sh start-linux.sh
```

El servidor se iniciará en `http://127.0.0.1:8000`. Abre esa dirección en el navegador para acceder a la aplicación.

### Notas

- La primera vez que accedas solo estará el módulo "prueba" que te puede servir de ejemplo. Tiene varios estudiantes, algunos resultados de aprendizaje, indicadores de logro, actividades evaluables y calificaciones.
- Una vez revisado el contenido del módulo "prueba", el primer paso será crear un módulo desde la interfaz (ver [Gestión de Módulos](3_conceptos.md)).
- Los datos se almacenan en archivos `.sqlite` dentro del directorio `data/`. Se creará un archivo `.sqlite` para cada módulo o grupo que quieras gestionar. Para hacer una copia de seguridad, basta copiar ese directorio.
