[← Volver al índice](indice.md)

## 3. Conceptos generales

### 3.1 Módulo/Grupo

En CCxI, cada módulo o grupo se almacena en un archivo `.sqlite` independiente dentro del directorio `data/`. Esto significa que:

- Puedes tener tantos módulos como necesites, cada uno con sus propios estudiantes, resultados, actividades y calificaciones.
- No necesitas un servidor de bases de datos; cada módulo es un simple archivo.
- Para duplicar o hacer una copia de seguridad de un módulo, basta copiar su archivo `.sqlite`.

Te recomiendo que uses nombres estandarizados para tus módulos/grupos. Por ejemplo:

- **1DAW-PROG**, para el grupo de programación de primero de DAW.
- **2DAM-DINT**, para el grupo de Diseño de Interfaces de segundo de DAM.
- **C2627-2DAW-DWES**. También puedes indicar el curso.

### 3.2 Resultado de Aprendizaje

Los **Resultados de Aprendizaje (RA)** son los que se indican en tu programación. Generalmente serán los establecidos en el decreto que define el ciclo más alguno que tú quieras añadir. Cada RA tien un **código identificativo** (ej. RA01, RA02…), un **nombre** (normalmente el que tiene en el decreto) y un **peso** que indica su importancia relativa respecto al total del módulo.

La calificación final del módulo se calcula como la media ponderada de las calificación de todos los RA según su peso.

### 3.3 Indicador de Logro

Un **Indicador de Logro (IL)** es un criterio medible y concreto que permite determinar si un estudiante ha alcanzado un resultado de aprendizaje. Son definidos por cada profesor (aunque algunos utilizamos los Criterios de Evaluación del decreto como guía para definirlos). Cada IL:

- Tiene un **código** (ej. IL1.a, IL2.c.3...) y un **nombre** descriptivo.
- Puede estar asociado a **uno o varios RA**, con un peso específico en cada relación.
- Cada IL se puede calificar en varias "Actividades Evaluables".

La nota de un RA se calcula como la media ponderada de las notas de los indicadores que le pertenecen.

### 3.4 Actividad Evaluable

Una **Actividad Evaluable (AE)** es cualquier instrumento de evaluación: examen, trabajo práctico, ejercicio de clase, proyecto, etc. Cada actividad:

- Tiene **código** (ej. AE1.2, AE3.a.2...), **nombre** y **fecha** de realización.
- Se asocia a **uno o varios indicadores de logro**.
- Para cada indicador asociado se define un **tipo de calificación** (ponderada, máxima o mínima) y opcionalmente un **peso** ([ver calificación](10_calificaciones.md)).

Cuando se califica a un estudiante en una actividad, se registra el nivel de logro alcanzado en cada indicador asociado.

### 3.5 Calificación

La calificación de cada Indicador de Logro en cada Actividad Evaluable que realiza cada Estudiante tiene dos opciones:

a) Puedes poner un **nivel de logro** numérico entre 0 y 10.
b) Puedes poner un **incremento** positivo o negativo (valor decimal) que se sumará a la calificación actual del IL.

Al calificar una AE, no solo puedes calificar los IL asociados a la AE, también puedes añadir nuevos IL para poner incrementos al estudiante que estás calificando. Por ejemplo: si al calificar la AE3 de Ana ves que ha mejorado su competencia en el IL2.b, puedes ponerle un incremento positivo en ese IL aunque no esté asociado a la AE3. Ese incremento será solo para Ana. 

Al calificar verás que el sistema te muestra la "calificación actual" del estudiante en el indicador que estás calificando. Esto te facilita decidir qué tipo de calificación quieres darle (nivel de logro o incremento). Por ejemplo: si al calificar a Blas en el IL2.b ves que tiene un 8 por actividades anteriores, pero esta vez le ha salido mal, igual prefieres ponerle un punto negativo en lugar de calificarle con un 3.

### 3.7 Informes de Estudiante

Los informes de estudiante se pueden generar en formato pdf para su envío posterior. De esta forma se puede cumplir con el requerimiento de información actualizada sobre el proceso de evaluación.

Hay dos tipos de informes:

- **Informe de Estudiante** que le indica la calificación obtenida en cada RA en función de las calificaciones obtenidas en cada IL.
- **Informe de Actividades por Resultados** que le permite al estudiante revisar el cálculo de la calificación del informe de estudiante.

Puede ser conveniente que, además de enviar estos informes a cada estudiante, les envíes el "Informe de Grupo" para que comparen su situación con el resto de la clase.


### 3.7 Informes de Grupo

Los **informes de grupo** muestran cuartiles en lugar de notas individuales. Los cuartiles dividen el conjunto de notas del grupo en cuatro partes iguales:

- **Q1 (primer cuartil)**: el 25 % de los estudiantes tiene una nota inferior o igual a este valor.
- **Q2 (mediana)**: el 50 % de los estudiantes tiene una nota inferior o igual a este valor. Es el valor central.
- **Q3 (tercer cuartil)**: el 75 % de los estudiantes tiene una nota inferior o igual a este valor.

Estas tres medidas permiten hacerse una idea rápida de la distribución de las calificaciones del grupo: si hay mucha diferencia entre Q1 y Q3 la dispersión es alta; si están próximos, el grupo es homogéneo.

El "Informe de Grupo" permite conocer la situación general del grupo y la situación de un estudiante concreto dentro de él.

El "Informe de Actividades por Resultados (Grupo)" está destinado al profesor, para que puedas conocer qué actividades están siendo más eficaces en el proceso de enseñanza/aprendizaje. Una AE que haya tenido un Q3 muy bajo, puede indicar que ha sido demasiado difícil para el grupo o que otros factores han impedido que la preparen bien.
