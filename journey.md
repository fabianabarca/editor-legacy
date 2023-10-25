# Cómo hacer un feed desde cero

**TP**: *transporte público*

Actores del TP en Costa Rica:

- operadores (empresas autobuseras concesionarias) - CRU
- gestor (CTP) - CRUD
- planificador (MOPT) - R
- regulador (ARESEP) - R
- observador (prensa, investigadores, CNE, etc.) - R

Para cada uno de estos actores habrá un tipo de usuario con distintos permisos.

Asumiendo ser CTP (CRUD): tarea: crear un feed desde cero

Un feed puede ser para 
- una sola agencia (empresa autobusera) y sus rutas
- una sola ruta
- todas las agencias y todas las rutas del país (o región)

1. Crear un "feed": registro en el modelo `Feed` 
