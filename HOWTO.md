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
    <dt>users</dt>
    <dd>Administra los distintos tipos de usuarios del sistema.</dd>
    <dt>exporting</dt>
    <dd>Crea los archivos .zip de exportación de GTFS, que es la utilidad central del editor, y además gestiona la importación de nuevos feeds GTFS.</dd>
    <dt>reporting</dt>
    <dd>Crea y muestra reportes a partir de los datos GTFS, como gráficas, análisis estadísticos, etc.</dd>
    <dt>editing</dt>
    <dd>Despliega los datos de GTFS y facilita su edición con interfaces apropiadas para el fin, como mapas, formularios, etc.</dd>
</dl>

Aunque `gtfs` y `edit` podrían ser una misma app, están separadas para poder utilizar `gtfs` casi *as is* en otros proyectos (como en el de pantallas de información GTFS).

## Discusión: Bootstrap vs Primer

Más adelante en el desarrollo hay que decidir entre posibles *frameworks* de HTML, CSS y JavaScript. En el TCU tenemos experiencia con [Bootstrap](https://getbootstrap.com/) pero también existe la posibilidad de seguir el estilo de GitHub mismo con [Primer](https://primer.style/). Queda abierta la discusión.
