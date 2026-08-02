# Dockloader

Este es un proyecto Full-Stack desarrollado con **Angular** para el Frontend y **Django + Django Rest Framework (DRF)** para el Backend.

Todo el entorno de desarrollo ha sido **dockerizado**, lo que significa que no necesitas instalar Node.js, Python o bases de datos directamente en tu máquina local para hacerlo funcionar.

## 📋 Requisitos Previos

* [Docker](https://www.docker.com/get-started) instalado.
* Docker Compose (incluido en las versiones modernas de Docker Desktop).

## 🚀 Instalación y Uso

**1. Clonar el repositorio**
Descarga este proyecto en tu máquina local.

**2. Configurar las IPs del Frontend**
Antes de levantar los contenedores, es necesario que el frontend sepa a qué IP o dominio apuntar para consumir la API de Django.
Debes cambiar la IP por la de tu entorno local (ej. la IP de tu red local) en la carpeta de variables de entorno de Angular (`environment.ts`).

**3. Construir y levantar los contenedores**
Abre una terminal en la raíz del proyecto (donde se encuentra el archivo `docker-compose.yml`) y ejecuta los siguientes comandos:

```bash
# Construir las imágenes de Docker
docker compose build

# Levantar los contenedores
docker compose up

```

*(Si deseas correrlo en segundo plano, puedes usar `docker compose up -d`)*.

Una vez finalizado, el frontend en Angular y la API en Django estarán funcionando en los puertos definidos en el `docker-compose.yml`.

---

## ⚠️ Advertencias y Consideraciones Importantes

Al estar utilizando una arquitectura separada (Angular y Django Rest Framework) dockerizada, ten en cuenta los siguientes puntos:

### 1. Política de CORS (¡Importante!)

Actualmente, las restricciones de **CORS están "bajadas"** (totalmente permisivas) en el backend de Django para facilitar el desarrollo. Esto significa que la API aceptará peticiones desde cualquier origen (`*`).

* **Para producción:** Es un riesgo de seguridad grave. Antes de desplegar, debes ir a la configuración de Django (`settings.py`) y modificar la librería `django-cors-headers` para permitir únicamente la URL de tu frontend en Angular usando la variable `CORS_ALLOWED_ORIGINS`.

### 2. Entorno de Desarrollo vs Producción

* **Django (`DEBUG=True`):** Revisa tu archivo de variables de entorno de Django (`.env`). Seguramente el modo Debug está activo. Nunca despliegues el proyecto a un servidor público con el Debug encendido, ya que expone variables sensibles y código fuente al mostrar errores.
* **Angular (`ng serve`):** En Docker, el frontend suele levantarse usando el servidor de desarrollo interno de Angular, apuntando a `0.0.0.0`. Esto está bien para programar, pero para producción debes hacer un build (`ng build`) y servir los archivos estáticos usando un servidor web como **Nginx** o Apache.

### 3. Migraciones de Base de Datos (NO APLICA)

Si es la primera vez que clonas y levantas el proyecto, recuerda que la base de datos de Django estará vacía. Es posible que necesites aplicar las migraciones para crear las tablas y crear un superusuario. Abre una nueva terminal mientras los contenedores están corriendo y ejecuta:

```bash
# Aplicar migraciones
docker compose exec backend python manage.py migrate

# (Opcional) Crear superusuario para entrar al panel de Admin
docker compose exec backend python manage.py createsuperuser

```

*(Nota: Cambia la palabra `backend` por el nombre exacto del servicio de Django que tengas en tu archivo docker-compose.yml).*

### 4. Hot Reload en Windows (WSL2) / Mac

Si estás utilizando Docker Desktop en Windows o Mac, es posible que el *Hot Reload* (recarga automática) de Angular no funcione inmediatamente al guardar un archivo. Si esto ocurre, habilita el "polling" en la configuración de arranque de Angular dentro del `package.json` (`ng serve --poll 2000`).