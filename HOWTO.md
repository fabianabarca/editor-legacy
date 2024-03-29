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

## Migrar a GeoDjango

[GeoDjango](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/) será utilizado con PostgreSQL y PostGIS.

- Instalar PostgreSQL.
- Instalar PostGIS.
- Crear base de datos `editor` con `$ createdb editor`.
- Ingresar con `$ psql editor`.
- [Habilitar PostGIS](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/postgis/) para la base de datos `ferias` con `# CREATE EXTENSION postgis;`.
- Modificar `settings.py` con (asumiendo que la DB no tiene password):
```python
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
    },
}
```
y con:
```python
INSTALLED_APPS = [
    (...)
    "django.contrib.gis",
]
```
- Agregar a `.env` (asumiendo que el usuario de PostgreSQL es `postgres`, y si no lo sabe puede hacer en psql: `# SELECT current_user;`):
```
DB_NAME=editor
DB_USER=postgres
```
- (Opcional) En algunos sistemas operativos, es necesario adjuntar a `settings.py`:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
    },
}

GDAL_LIBRARY_PATH = config('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = config('GEOS_LIBRARY_PATH')
```
y en `.env`:
```
GDAL_LIBRARY_PATH=/opt/homebrew/opt/gdal/lib/libgdal.dylib
GEOS_LIBRARY_PATH=/opt/homebrew/opt/geos/lib/libgeos_c.dylib
```
o lo que corresponda.
- Hacer todas las migraciones con `$ python manage.py makemigrations gtfs` y así para cada app.
- Migrar con `$ python manage.py migrate` para crear las tablas.
- Hacer `$ python manage.py loaddata auth` para cargar los datos de usuarios de prueba del fixture (peligroso).
- Para ver mapas de OpenStreetMap en el panel de administración, hay que editar `gtfs/admin.py` para cualquier modelo que utilice datos geoespaciales con:
```python
from django.contrib.gis import admin
(...)
admin.site.register(GeoShape, admin.GISModelAdmin)
```

Con esto debería funcionar la aplicación pero ahora con PostgreSQL y PostGIS activado para usar GeoDjango, que permite guardar ubicaciones y regiones en el mapa y hacer búsquedas geoespaciales.

## Aplicaciones del sitio

Django utiliza "apps" para manejar el sitio. Por experiencia, sabemos que son divisiones útiles para la organización del sitio, aunque realmente desde una sola app se podrían realizar todas las funciones. Por orden, sin embargo, es mejor hacer una separación funcional. En ese sentido, y con base en la funcionalidad esperada del sitio, se han creado los siguientes apps:

<dl>
    <dt>gtfs</dt>
    <dd>Administra la base de datos de GTFS Schedule.</dd>
    <dt>viewing</dt>
    <dd>Despliega los datos de GTFS con visualizaciones apropiadas, como mapas, gráficas, etc.</dd>
    <dt>editing</dt>
    <dd>Facilita la edición de los datos de GTFS con interfaces apropiadas, como mapas, formularios, etc.</dd>
    <dt>reporting</dt>
    <dd>Crea y muestra reportes a partir de los datos GTFS, como gráficas, análisis estadísticos, etc.</dd>
    <dt>exporting</dt>
    <dd>Crea los archivos .zip de exportación de GTFS, que es la utilidad central del editor.</dd>
    <dt>importing</dt>
    <dd>Lee y valida los archivos .zip para la importación de datos GTFS y los incorpora en la base de datos.</dd>
    <dt>website</dt>
    <dd>Despliega algunas páginas generales del sitio.</dd>
    <dt>users</dt>
    <dd>Administra los distintos tipos de usuarios del sistema.</dd>
</dl>

Aunque `gtfs` y `edit` podrían ser una misma app, están separadas para poder utilizar `gtfs` casi *as is* en otros proyectos (como en el de pantallas de información GTFS).

## Páginas del sitio

Con base en la funcionalidad descrita, es posible crear un primer esbozo de las páginas que tendrá el sitio (arquitectura de información), clasificadas según el app que las gestiona:

- ***website***
    - `/`: página de bienvenida, incluyendo la lista de feeds disponibles
    - `/gtfs`: información sobre GTFS y su implementación
    - `/acerca`, `/contacto`, etc.: información sobre el sitio web
- ***viewing***
    - `/datos`: página de meta información sobre los datos que contiene la página
    - `/datos/<código-de-agencia>`: información básica de la agencia y sus rutas
    - `/datos/<código-de-ruta>`: información básica de la ruta, sin posibilidades de edición
    - `/datos/buscar?param=valor`: resultados de la búsqueda de datos
- ***editing***
    - `/edicion/<código-de-agencia>`: editor de datos de la agencia elegida
    - `/edicion/<código-de-ruta>`: editor de datos de la ruta elegida
- ***reporting***
    - `/reportes`: página para la visualización de datos y creación de reportes
    - `/reportes/<tabla-gtfs>`: información global (de todas las agencias y todas las rutas) de cualquiera de las tablas GTFS, como *stops*, *calendar*, *trips*, etc. Debe estar al menos la explicación de su contenido y quizá algunas estadísticas o gráficas (especialmente cuando no se puede mostrar todo el contenido). Puede incluir opciones de filtrado.
- ***exporting***
    - `/exportacion`: exportador de datos seleccionados como un archivo comprimido .zip
    - `/exportacion/<código-de-agencia>`: exportador de datos de la agencia elegida como un archivo comprimido .zip
    - `/exportacion/<código-de-ruta>`: exportador de datos de la ruta elegida como un archivo comprimido .zip
- ***importing***
    - `/importacion`: página para la importación y revisión de nuevos *feeds* GTFS
- ***users***
    - `/perfil`: página de información de la persona usuaria


**Nota 1**: se asume la existencia de un código único para cada agencia y cada ruta. No hay una asignación del tipo `/<código-de-agencia>/<código-de-ruta>`
porque las rutas pueden cambiar de agencia (empresa concesionaria), de forma que la agencia es solo un "atributo" de cada ruta y tiene precedencia.

**Nota 2**: este sitio en general no es un visualizador de datos GTFS de la forma en que será desplegada al público. Por ejemplo, el público podría estar interesado en visualizar una o varias rutas en una misma tabla de horarios o una o varias trayectorias de bus en un mismo mapa, pero aquí no es el objetivo pues las visualizaciones sería únicamente por cada ruta individual. Los reportes sí pueden hacer visualizaciones más complejas.

## Discusión: Bootstrap vs Primer

Más adelante en el desarrollo hay que decidir entre posibles *frameworks* de HTML, CSS y JavaScript. En el TCU tenemos experiencia con [Bootstrap](https://getbootstrap.com/) pero también existe la posibilidad de seguir el estilo de GitHub mismo con [Primer](https://primer.style/). Queda abierta la discusión.
