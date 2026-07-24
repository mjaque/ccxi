# Manual de Usuario — CCxI

## 1. Objetivo de CCxI

**CCxI (Calificador de Competencias por Indicadores)** es una aplicación web diseñada para facilitar la calificación por competencias en ciclos de Formación Profesional.

### Aviso Importante

Esta aplicación **solo gestiona la calificación**, que es una parte del proceso de evaluación. No cubre otras actividades asociadas al proceso de evaluación (como la comunicación con los estudiantes, retroalimentación, evaluación inicial, seguimiento...) 

Su propósito principal es permitir al docente:

- Definir los **resultados de aprendizaje** (RA) de un módulo y asignarles un peso relativo.
- Descomponer cada RA en **indicadores de logro** medibles y asociarlos a uno o varios resultados.
- Crear **actividades evaluables** (exámenes, trabajos, prácticas…) y vincularlas a los indicadores que evalúan.
- **Calificar** a cada estudiante en cada actividad introduciendo el nivel de logro alcanzado por indicador.
- Obtener **informes individuales y de grupo** que reflejan el progreso, incluyendo el cálculo automático de la calificación actual de cada indicador y el análisis por cuartiles del grupo.

CCxI almacena cada módulo en un archivo independiente, lo que permite tener cursos separados sin necesidad de un servidor de bases de datos. No requiere autenticación instalación más allá de Python 3.8+ y un navegador web ([ver instalación](2_instalacion.md)).

### Otro Aviso Importante

La información no se guarda encriptada. Debes asegurarte de que los datos registrados no son accedidos por personas sin autorización. Esto puedes conseguirlo de dos formas:

1. Instala la aplicación en un pendrive y guárdalo bien.

2. Evita introducir datos personales. Por ejemplo, puedes usar números, códigos o nombres de pila para los estudiantes, por lo que resultará difícil identificarlos personalmente si la información cae en manos inadecuadas. 
