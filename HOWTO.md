# Instrucciones para desarrollo

## Clave secreta de Django

La clave secreta de Django y otras configuraciones están en variables ambientales y es manipulado por el paquete `python-decouple` ([documentación](https://pypi.org/project/python-decouple/)).

Para iniciar:

```bash
pip install python-decouple
```

Luego, en `editor/settings.py`:

```python
from decouple import config
```

(Seguir instrucciones de la documentación).

> El equipo de desarrolladores compartirá el documento `.env`.

## Aplicaciones del sitio

Django utiliza "apps" para manejar el sitio. Por experiencia, sabemos que son divisiones útiles para la organización del sitio, aunque realmente desde una sola app se podrían realizar todas las funciones. Por orden, sin embargo, es mejor hacer una separación funcional. En ese sentido, y con base en la funcionalidad esperada del sitio, se han creado los siguientes apps:

<dl>
    <dt>gtfs</dt>
    <dd>Administra la base de datos de GTFS Schedule.</dd>
    <dt>viewing</dt>
    <dd>Despliega los datos de GTFS con visualizaciones apropiadas, como mapas, gráficas, etc.</dd>
    <dt>editing</dt>
    <dd>Facilita la edición de los datos de GTFS con interfaces apropiadas, como mapas, formularios, etc.</dd>
    <dt>exporting</dt>
    <dd>Crea los archivos .zip de exportación de GTFS, que es la utilidad central del editor, y además gestiona la importación de nuevos feeds GTFS.</dd>
    <dt>reporting</dt>
    <dd>Crea y muestra reportes a partir de los datos GTFS, como gráficas, análisis estadísticos, etc.</dd>
    <dt>users</dt>
    <dd>Administra los distintos tipos de usuarios del sistema.</dd>
</dl>

Aunque `gtfs` y `edit` podrían ser una misma app, están separadas para poder utilizar `gtfs` casi *as is* en otros proyectos (como en el de pantallas de información GTFS).

## Páginas del sitio

Con base en la funcionalidad descrita y las apps existentes, es posible crear un primer esbozo de las páginas que tendrá el sitio (arquitectura de información):

> Es necesario determinar si la información será desplegada por **ruta** o por **agencia**. Posiblemente por ruta o conjunto de rutas.

- `/`: página de bienvenida, incluyendo la lista de feeds disponibles y búsquedas de datos.
- `/<código-de-agencia>`: información básica de la agencia y sus rutas
- `/<código-de-ruta>`: información básica de la ruta, sin posibilidades de edición
    - `/<código-de-ruta>/edicion`: editor de datos de la ruta elegida
    - `/<código-de-ruta>/exportacion`: exportador de datos de la ruta elegida como un archivo comprimido .zip
- `/datos`: página para la creación de reportes y visualización de datos
- `/importacion`: página para la importación y revisión de nuevos *feeds* GTFS
- `/perfil`: página de información de la persona usuaria

**Nota 1**: se asume la existencia de un código único para cada agencia y cada ruta. No hay una asignación del tipo `/<código-de-agencia>/<código-de-ruta>`
porque las rutas pueden cambiar de agencia (empresa concesionaria), de forma que la agencia es solo un "atributo" de cada ruta y tiene precedencia.

**Nota 2**: este sitio en general no es un visualizador de datos GTFS de la forma en que será desplegada al público. Por ejemplo, el público podría estar interesado en visualizar una o varias rutas en una misma tabla de horarios o una o varias trayectorias de bus en un mismo mapa, pero aquí no es el objetivo pues las visualizaciones sería únicamente por cada ruta individual. Los reportes sí pueden hacer visualizaciones más complejas.

## Discusión: Bootstrap vs Primer

Más adelante en el desarrollo hay que decidir entre posibles *frameworks* de HTML, CSS y JavaScript. En el TCU tenemos experiencia con [Bootstrap](https://getbootstrap.com/) pero también existe la posibilidad de seguir el estilo de GitHub mismo con [Primer](https://primer.style/). Queda abierta la discusión.
