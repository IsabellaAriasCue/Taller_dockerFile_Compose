## Proyecto: API de Venta de Videojuegos con FastAPI, Docker y PostgreSQL

### Descripción

Este proyecto es una API REST desarrollada en **FastAPI** que permite gestionar videojuegos (crear, listar, obtener, eliminar y aplicar descuentos).
La aplicación está conectada a una base de datos **PostgreSQL** y se ejecuta completamente en contenedores usando **Docker y Docker Compose**.
Incluye pruebas unitarias ejecutadas dentro del contenedor.


## Tecnologías utilizadas

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker
* Docker Compose
* Pytest


## Endpoints principales

### Home

```
GET /
```

### Crear videojuego

```
POST /videojuegos
```

### Listar videojuegos

```
GET /videojuegos
```

### Obtener videojuego por ID

```
GET /videojuegos/{id}
```

### Eliminar videojuego

```
DELETE /videojuegos/{id}
```

### Aplicar descuento

```
PUT /videojuegos/{id}/descuento?porcentaje=10
```



## Requisitos previos

* Docker Desktop instalado
* Docker Compose habilitado


## Ejecución del proyecto

### 1. Construir y levantar los contenedores

```
docker compose up -d --build
```

### 2. Verificar contenedores activos

```
docker compose ps
```


## Ejecución de pruebas

### Ejecutar pruebas dentro del contenedor

```
docker compose exec app pytest
```

### Ejecutar pruebas con contenedor temporal

```
docker compose run --rm app pytest
```

---

## Reconstrucción del servicio de la aplicación

```
docker compose up -d --build app
```

---

## Notas importantes

* La base de datos PostgreSQL se ejecuta en un contenedor separado.
* Los datos se almacenan en un volumen persistente.
* Las pruebas se ejecutan dentro del contenedor sin necesidad de instalar dependencias en la máquina local.

---

## Autor

Proyecto académico – Taller Docker, FastAPI y pruebas en contenedores.

