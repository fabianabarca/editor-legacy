# Pasos para la creación de un nuevo *feed*

Un *feed* consiste en un archivo `.zip` que contiene varios archivos `.txt` en formato CSV (valores separados por coma). Es necesario construir este *feed* a partir de las tablas de la base de datos, que fueron creadas por los modelos ORM según la [referencia](https://gtfs.org/schedule/reference/) GTFS Schedule v2.0.

Aunque es posible importar un *feed* `.zip` ya creado, la labor principal dentro del editor, dado que en Costa Rica casi nadie tiene GTFS, será crear un *feed* nuevo.

Aquí están descritos los pasos que hay que seguir y el orden establecido, y por tanto es una referencia para crear todas las tablas y secciones del editor propiamente.

Premisas para la edición:

- `class Company` es un modelo creado para la administración del sitio, y es la entidad que crea los *feed*.
- Los *feed* tienen, al menos: una versión vigente, una versión en edición, y un histórico de *feeds*.
- Para conservar el histórico, la propuesta es tener un modelo `class Feed` que guarda el archivo `.zip` del histórico, del vigente y del que está en edición
- Cada dato de las tablas está asociado a una combinación única de `company_id` y `feed_id`, entonces, cuando cargamos en el editor un *feed* para edición, hay que hacer el _query_ con base en esos dos identificadores.

## Páginas del sitio

- `editor.com/<company_id>/gtfs/`
Una lista de los *feeds* existentes, incluyendo el histórico, el vigente y uno en edición (se crea automáticamente cuando se genera un *feed*)

- `editor.com/<company_id>/gtfs/<feed_id>`
Un sitio de edición del *feed* seleccionado, al estilo del [sitio de horas de Tropicalización](https://tropicalizacion.eie.ucr.ac.cr/) con un menú lateral con una página para cada tabla

- `editor.com/<company_id>/gtfs/<feed_id>/<table_name>/` (por ejemplo: `editor.com/<company_id>/gtfs/<feed_id>/agencia/`)
Un sitio para la edición de todos los campos de cada una de las tablas. Cuando es necesario editar registros de una misma tabla, hay dos opciones (discusión pendiente):
  - Abrir una ventana emergente tipo [modal](https://getbootstrap.com/docs/5.3/components/modal/) para editar el registro particular (así lo hace AddTransit)
  - Ir a una página nueva, tipo `editor.com/<company_id>/gtfs/<feed_id>/paradas/<stop_id>`, donde se hace la misma edición para el registro particular

### Componentes de cada página de edición de una tabla

- Explicación exhaustiva de lo que hace esa tabla
- Definición rigurosa de los campos que hay que llenar, incluyendo formatos
- Ejemplos de registros
- Convenciones adoptadas para la edición de GTFS

## Orden en el que debe crearse un nuevo *feed*

- Es necesario editar una lista de las tablas de GTFS Schedule:
- También es necesario editar tres tablas que son creadas para nuestro editor (no son parte de GTFS Schedule)

El orden en el que se realiza es, específicamente:

1. `agency`
1. `routes`
1. `stops`: esta posiblemente sea una tabla "universal" de referencia creada por una autoridad competente (como el CTP) porque las paradas no se pueden "inventar", sino que son predefinidas. Aun así, posiblemente en nuestro editor tengamos que habilitar la creación si no existe esa tabla "universal"
  - Nota: cuando se genera la tabla `stops` para un feed particular, deben considerarse los `zone_id` de la tabla auxiliar `route_stops`.
1. `calendar`
1. `calendar_dates`
1. `geoshapes` (**tabla auxiliar**): **con un mapa** se edita la línea o trayectoria que recorre cada `shape`.
1. `shapes`: se genera automáticamente de la tabla `geoshapes`.
1. `route_stops` (**tabla auxiliar**): representa la secuencia de paradas que sigue una ruta (`route_id`) en una dirección (`direction_id`), bajo la premisa de que siempre es la misma (algo que asumimos que aplica en Costa Rica)
1. `trips`: es la tabla "central" del *feed* a partir de la cual se construye. Referencia de [Partridge](https://github.com/remix/partridge): "En el núcleo de Partridge hay un gráfico de dependencia con raíz en `trips.txt`. Los datos desconectados se descartan de acuerdo con este gráfico al leer el contenido de un *feed*." O también: "lo que no está vinculado a un viaje, no existe" (F. Abarca, 2023)
10. `trip_times` (**tabla auxiliar**): tiene la indicación explícita de la hora de salida del viaje en la parada inicial y, opcionalmente, en otras paradas donde el tiempo de salida es exacto (es decir: `timepoint` = 1) lo cual es heredado ("jalado") de la tabla `route_stops`. Esto es una emulación de la forma habitual de dar los horarios en Costa Rica, es decir: dar la hora de salida y nada más, no hay información sobre cuáles son las siguientes paradas y a qué hora pasan por ahí.
  - Nota: en el caso del método **A** de estimación de tiempos de paradas (ver siguiente) es necesario también un registro adicional con el tiempo de llegada a la última parada de la ruta (que está en `route_stops`).
  - Sobre si es necesario el tiempo de llegada del viaje para utilizar el método A, el sistema debe determinarlo consultando la tabla de funciones de aproximación para tiempos de llegada basados en mediciones, `stop_times_estimations` (funciones polinomiales). Si no existe un estimador para esta combinación de ruta/dirección, entonces sí es necesario pedir la estimación "manual" aproximada del tiempo de llegada del viaje para hacer los cálculos intermedios con el método A.
1. `stop_times_measurements` (**tabla auxiliar**): una tabla donde se hace registros de tiempos de llegada a las paradas de todos los buses y de donde se van a construir las funciones polinomiales de aproximación en el método B del estimador.
1. `stop_times_estimations` (**tabla auxiliar**): funciones polinomiales calculados a partir de los datos de la tabla `stop_times_measurements` utilizados para estimar tiempos de llegada con el método B.
1. `stop_times`: es una tabla *generada automáticamente* con ayuda del paquete `estimador` y con base en dos métodos:
    - A: conociendo el tiempo de salida y de llegada del viaje completo (o de un segmento) estimación de forma proporcional a la distancia entre paradas
    - B: conociendo el tiempo de salida y funciones polinomiales de estimación de tiempos de llegada a cada parada, generadas a partir de mediciones reales de los viajes de la ruta
11. `fare_attributes`: los precios de las tarifas
12. `fare_rules`: el "de dónde a dónde" aplican las tarifas según zonas de las paradas (temazo este de las zonas, quizá implique una tabla auxiliar adicional, o una columna nueva `zone_id` en la tabla `route_stops`, que parece lo más probable)
13. `feed_info`: pura información de contacto y otra generada automáticamente
