[← Volver al índice](indice.md)

# Generación de Informes — ccxi

## 11.1 Acceso

Ve a la pestaña **Informes**. Se muestran cuatro bloques, cada uno con su propio formulario y botón para generar el informe correspondiente.

Todos los informes se abren en una **pestaña nueva** del navegador. Si no se abre, permite las ventanas emergentes para esta aplicación.

## 11.2 Fecha de corte (opcional)

Los cuatro informes aceptan una **fecha** opcional. Si se indica, solo se tendrán en cuenta las actividades realizadas hasta esa fecha. Esto permite generar informes parciales (por ejemplo, hasta la primera evaluación).

Si se deja vacía, se incluyen todas las actividades del módulo.

## 11.3 Informe de Estudiante

Muestra la calificación detallada de un estudiante en cada resultado de aprendizaje, con el desglose por indicadores de logro.

1. Selecciona un **estudiante**
2. Opcionalmente, elige una **fecha de corte**
3. Pulsa **Generar informe**

El informe incluye:
- **Calificación del módulo**: nota final del estudiante
- Por cada **resultado de aprendizaje**: código, nombre, peso y nota
- Dentro de cada RA, los **indicadores** asociados con su código, nombre, peso y nota

## 11.4 Informe de Actividades por Resultados

Misma información que el informe de estudiante, pero desglosada por actividades dentro de cada resultado de aprendizaje. Es útil para que el estudiante entienda cómo se ha calculado su calificación.

1. Selecciona un **estudiante**
2. Opcionalmente, elige una **fecha de corte**
3. Pulsa **Generar informe**

El informe incluye, para cada RA, el listado de actividades con:
- Código, nombre y fecha de la actividad
- Tipo de calificación y peso
- Calificación obtenida en esa actividad

## 11.5 Informe de Grupo

Muestra los cuartiles (Q1, Q2, Q3) de las calificaciones del grupo en cada resultado de aprendizaje e indicador de logro. No requiere seleccionar un estudiante: abarca a todos.

1. Opcionalmente, elige una **fecha de corte**
2. Pulsa **Generar informe de grupo**

El informe incluye:
- **Número de estudiantes** del grupo
- **Calificación del módulo** expresada en cuartiles
- Por cada RA, los cuartiles de la nota del grupo
- Dentro de cada RA, los cuartiles de cada indicador

Los cuartiles se interpretan así:
- **Q1 (primer cuartil)**: el 25 % de los estudiantes tiene una nota inferior o igual a este valor
- **Q2 (mediana)**: el 50 % de los estudiantes tiene una nota inferior o igual a este valor
- **Q3 (tercer cuartil)**: el 75 % de los estudiantes tiene una nota inferior o igual a este valor

Si la diferencia entre Q1 y Q3 es grande, la dispersión del grupo es alta; si están próximos, el grupo es homogéneo. ([más información sobre cuartiles](3_conceptos.md#37-cuartiles-q1-q2-q3))

## 11.6 Informe de Actividades por Resultados (Grupo)

Muestra los cuartiles por actividad, agrupados por resultado de aprendizaje, para todo el grupo. Está orientado al profesor para evaluar qué actividades están siendo más eficaces.

1. Opcionalmente, elige una **fecha de corte**
2. Pulsa **Generar informe**

El informe incluye, para cada RA, el listado de actividades con:
- Código, nombre y fecha de la actividad
- Tipo de calificación y peso
- Cuartiles (Q1, Q2, Q3) de la calificación del grupo en esa actividad

Una actividad con un Q3 muy bajo puede indicar que ha resultado demasiado difícil o que no se ha preparado adecuadamente.

## 11.7 Código de colores

Las notas en los informes se muestran con un código de colores para facilitar la lectura:

| Color | Rango |
|-------|-------|
| Rojo | Nota menor que 4 |
| Amarillo | Nota entre 4 y 5 (excluido) |
| Verde | Nota entre 5 y 8 (excluido) |
| Azul | Nota igual o superior a 8 |
| Gris | Sin calificar |

## 11.8 Cambio de módulo

Al seleccionar otro módulo en el panel superior, los selectores de estudiante se recargan automáticamente. También se actualizan al crear, editar o eliminar estudiantes.

## 11.9 Observaciones

- Los informes están diseñados para **imprimirse** directamente desde el navegador (incluyen estilos específicos para impresión)
- El sistema de calificación utilizado en los informes se explica en detalle en el [Sistema de Calificación](10_calificaciones.md)
- Para informes parciales por evaluaciones, usa la **fecha de corte**

## 11.10 Listado de Indicadores de Logro

El último bloque de la vista de informes genera un listado de indicadores agrupado por resultado de aprendizaje. No requiere seleccionar estudiante ni indicar una fecha.

El informe muestra el nombre del módulo y, para cada resultado:

- Código, nombre y peso del resultado de aprendizaje
- Código, nombre y peso de cada indicador asociado en ese resultado
