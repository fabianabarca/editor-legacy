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

## Discusión: Bootstrap vs Primer

Más adelante en el desarrollo hay que decidir entre posibles *frameworks* de HTML, CSS y JavaScript. En el TCU tenemos experiencia con [Bootstrap](https://getbootstrap.com/) pero también existe la posibilidad de seguir el estilo de GitHub mismo con [Primer](https://primer.style/). Queda abierta la discusión.
