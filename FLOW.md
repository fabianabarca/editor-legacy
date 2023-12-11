# Pasos para la creación de un nuevo *feed*

Un *feed* consiste en un archivo `.zip` que contiene varios archivos `.txt` en formato CSV (valores separados por coma). Es necesario construir este *feed* a partir de las tablas de la base de datos, que fueron creadas por los modelos ORM según la [referencia](https://gtfs.org/schedule/reference/) GTFS Schedule v2.0.

Aunque es posible importar un *feed* `.zip` ya creado, la labor principal dentro del editor, dado que en Costa Rica casi nadie tiene GTFS, será crear un *feed* nuevo.

Aquí están descritos los pasos que hay que seguir y el orden establecido, y por tanto es una referencia para crear todas las tablas y secciones del editor propiamente.

## Compañías y *feeds*

Premisas para la edición de los *feeds* con los modelos `Company` y `Feed` para almacenar *feeds* históricos y plantillas.

- `class Company` es un modelo creado para la administración del sitio, y es la entidad que crea los *feed*.
  - Una compañía puede crear uno o más *feeds*. Un ejemplo puede ser CTP (Consejo de Transporte Público) que haga todas las rutas del país o en el caso de que **cada empresa autobusera** hiciera su propio *feed*.
- `class Feed` es un modelo para guardar o referenciar un *feed*, ya que pueden existir varios (diferentes compañías o diferentes versiones de un mismo *feed*)
  - Los *feed* tienen, al menos: una versión vigente, una versión en edición, y un histórico de *feeds*.
    - Esto implica la existencia de un campo llamado algo así como `feed_status` (tipo *enum*: `EDITION`, `CURRENT`, `RECORD`)
    - Para conservar el histórico, la propuesta es tener un campo llamado algo así como `feed_file` que guarda el archivo `.zip` del histórico y del vigente (del que está en edición no, porque no se ha creado todavía, y la creación del archivo `.zip` tiene varios pasos de validación).
    - Propuesta de conservación de registros en las tablas: mantener únicamente los registros que pertenecen al *feed* actual y al que está en edición, y mantener el histórico como archivos `.zip`. Si en algún momento es necesario restaurar una versión antigua (*alla* Git) entonces tendría que "jalar" ese `.zip` y restaurarlo en el "espacio de trabajo" (las tablas de GTFS).
- Cada dato de las tablas está asociado a una combinación única de `company_id` y `feed_id`, entonces, cuando cargamos en el editor un *feed* para edición, hay que hacer el *query* con base en esos dos identificadores.
- El servicio de buses es estacional, en teoría (meses de mayor y menor demanda). Por tanto, es necesario tener algo así como "plantillas" para editar el servicio según la época (referencia: MBTA en Día de Acción de Gracias). ¿En Costa Rica hay "temporadas"? ¿El servicio de buses de, por ejemplo, Jacó cambia su frecuencia según la época del año?
  - De alguna forma, debemos habilitar la existencia de estas "plantillas". Una opción es crear *feeds "plantilla"* o simplemente cargar para edición un *feed* "viejo" (ejemplo: del diciembre anterior). 

## Tipos de usuarios

- Administradores (del sitio): nosotros los desarrolladores (CRUD)
- Operadores: empresas autobuseras (CRU)
- Gestores: CTP (CRUD)
- Planificadores: MOPT (R)
- Reguladores: ARESEP (R)
- Observadores: prensa, investigadores, etc. (R)

## Páginas del sitio

#### Páginas misceláneas

Django app: `website`

- `editor.com/`
Página de bienvenida con información general, una lista de "compañías" a las que tiene acceso el usuario, la opción de crear una nueva, etc.

- `editor.com/<company_id>/`
Página de información de la compañía elegida, datos generales, algunas acciones por definir. Posible confusión: compañía =/= empresa autobusera (necesariamente).

- `editor.com/perfil/`
Página de perfil del usuario registrado.

- `editor.com/sobre`
Página de información general sobre el sitio, sobre GTFS, etc.

- Páginas administrativas
  - Edición de usuarios
  - Edición de compañías

#### Páginas de edición de GTFS

Django app: `gtfs`

- `editor.com/<company_id>/gtfs/`
Una lista de los *feeds* existentes, incluyendo el histórico, el vigente y uno en edición (se crea automáticamente cuando se genera un *feed*).
  - Aquí debe estar también la opción de **importar** un *feed* externo (elegir archivo `.zip`, descomprimir, validar, registrar, guardar)

- `editor.com/<company_id>/gtfs/<feed_id>`
Un sitio de edición del *feed* seleccionado, al estilo del [sitio de horas de Tropicalización](https://tropicalizacion.eie.ucr.ac.cr/) con un menú lateral con una página para cada tabla (opcional). También es una página resumen del *feed*, con estadísticas, mapas, información global.
  - Nota: esta es la sección de "reporte" o "vista" o informe de un *feed* en general, y quizá también se puede habilitar un tipo de búsqueda dentro del *feed*. Esto sería de interés, sobre todo, para los usuarios observadores, como prensa e investigadores.
  - Nota: en el caso de un `.zip` histórico, habría que descomprimir el archivo y, por ejemplo, cargar las tablas en `DataFrame` de Pandas para hacer la manipulación "local" y obtener estísticas y otra información. Esto no debería ser tan demandante ni en tiempo ni en memoria y es el "precio" a pagar por no almacenar estos datos en la base de datos, sino guardados en un baúl.
  - Nota: el `<feed_id>` del *feed* en edición posiblemente sea único y podría llamarse algo así como `edicion`.
  - Nota: ¿aplica que una compañía tiene únicamente un *feed*? (Posiblemente sí, ejemplo: MBTA o Metro).

- `editor.com/<company_id>/gtfs/<feed_id>/<table_name>/` (por ejemplo: `editor.com/<company_id>/gtfs/<feed_id>/agencia/`)
Un sitio para la edición de todos los campos de cada una de las tablas. Cuando es necesario editar registros de una misma tabla, hay dos opciones (discusión pendiente):
  - Abrir una ventana emergente tipo [modal](https://getbootstrap.com/docs/5.3/components/modal/) para editar el registro particular (así lo hace AddTransit)
  - Ir a una página nueva, tipo `editor.com/<company_id>/gtfs/<feed_id>/paradas/<stop_id>`, donde se hace la misma edición para el registro particular

- `editor.com/<company_id>/gtfs/<feed_id>/exportar/`
La página donde se hace la validación del *feed* en edición actualmente y donde se puede **exportar**.

### Componentes de cada página de edición de una tabla

Página de edición de una tabla: `editor.com/<company_id>/gtfs/<feed_id>/<table_name>/`

Público meta: personal administrativo que crea y actualiza los datos del servicio.

- Explicación exhaustiva de lo que hace esa tabla
- Definición rigurosa de los campos que hay que llenar, incluyendo formatos
- Ejemplos de registros
- Convenciones adoptadas para la edición de GTFS

## Orden en el que debe crearse un nuevo *feed*

- Es necesario editar una lista de las tablas de GTFS Schedule
- También es necesario editar tres tablas que son creadas para nuestro editor (no son parte de GTFS Schedule), llamadas **tablas auxiliares**.

El orden en el que se realiza es, específicamente:

1. `agency` (no tiene dependencias)
2. `routes` (una única dependencia de `agency`)
3. `stops` (no tiene dependencias): esta posiblemente sea una tabla "universal" de referencia creada por una autoridad competente (como el CTP) porque las paradas no se pueden "inventar", sino que son predefinidas y autorizadas. Aun así, posiblemente en nuestro editor tengamos que habilitar su creación, si no existe esa tabla "universal".
  - Nota: en la tabla "universal" no se pueden definir los `zone_id` porque son propios de cada ruta
  - Nota: cuando se genera la tabla `stops` para un *feed* particular, deben considerarse los `zone_id` de la tabla auxiliar `route_stops`.
4. `calendar` (no tiene dependencias)
5. `calendar_dates` (una única dependencia de `calendar`)
6. `geoshapes` [**tabla auxiliar**] (no tiene dependencias): **con un mapa** se edita la línea o trayectoria que recorre cada `shape`.
7. `shapes` (no tiene dependencias): se genera automáticamente de la tabla `geoshapes`.
8. `route_stops` [**tabla auxiliar**] (tiene varias dependencias): representa la secuencia de paradas (`stop_id`) que sigue una ruta (`route_id`) en una dirección (`direction_id`) en una trayectoria (`shape_id`), bajo la premisa de que siempre es la misma (algo que asumimos que aplica en Costa Rica).
9. `trips`: es la tabla "central" a partir de la cual se construye el *feed*. Referencia de [Partridge](https://github.com/remix/partridge): "En el núcleo de Partridge hay un gráfico de dependencia con raíz en `trips.txt`. Los datos desconectados se descartan de acuerdo con este gráfico al leer el contenido de un *feed*." O también: "lo que no está vinculado a un viaje, no existe".
10. `trip_times` [**tabla auxiliar**]: tiene la indicación explícita de la **hora de salida del viaje** en la parada inicial y, opcionalmente, en otras paradas donde el tiempo de salida es exacto (es decir: `timepoint` = 1) lo cual es heredado ("jalado") de la tabla `route_stops`. Esto es una emulación de la forma habitual de dar los horarios en Costa Rica, es decir: dar la hora de salida y nada más, no hay información sobre cuáles son las siguientes paradas y a qué hora pasan por ahí.
  - Nota: en el caso del método **A** de estimación de tiempos de paradas (ver siguiente) es necesario también un registro adicional con el tiempo de llegada a la última parada de la ruta (que está en `route_stops`). Es decir, hay que indicar la hora de salida y la hora estimada de llegada.
  - Sobre si es necesario el tiempo de llegada del viaje para utilizar el método **A**, el sistema debe determinarlo consultando la tabla de funciones de aproximación para tiempos de llegada basados en mediciones, `stop_times_estimations` (funciones polinomiales). Si no existe un estimador para esta combinación de ruta/dirección, entonces sí es necesario pedir la estimación "manual" aproximada del tiempo de llegada del viaje para hacer los cálculos intermedios con el método **A**.
11. `stop_times_measurements` [**tabla auxiliar**]: una tabla donde se hace registros de tiempos de llegada a las paradas de todos los buses y de donde se van a construir las funciones polinomiales de aproximación en el método **B** del estimador.
12. `stop_times_estimations` [**tabla auxiliar**]: funciones polinomiales calculadas a partir de los datos de la tabla `stop_times_measurements` utilizadas para estimar tiempos de llegada con el método **B**.
13. `stop_times`: es una tabla *generada automáticamente* con ayuda del paquete `stop_times_estimator` y con base en dos métodos:
    - **A**: conociendo el tiempo de salida y de llegada del viaje completo (o de un segmento) y haciendo una estimación de forma proporcional a la distancia entre paradas
    - **B**: conociendo el tiempo de salida y las funciones polinomiales de estimación de tiempos de llegada a cada parada, generadas a partir de mediciones reales de los viajes de la ruta
14. `fare_attributes`: los precios de las tarifas
15. `fare_rules`: el "de dónde a dónde" aplican las tarifas según zonas de las paradas (temazo este de las zonas, quizá implique una tabla auxiliar adicional, o una columna nueva `zone_id` en la tabla `route_stops`, que parece lo más probable)
16. `feed_info`: pura información de contacto y otra generada automáticamente

## Sobre la disposición (*layout*) del editor

Preliminarmente, Fabián prefiere un editor con columna lateral donde estén las tablas (en edición).

Adrián hará un Figma.
