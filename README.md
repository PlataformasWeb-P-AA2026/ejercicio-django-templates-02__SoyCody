# Despliegue de Django en Render (Free) con PostgreSQL  
*(sin acceso a Shell)*

Este proyecto muestra cómo desplegar una aplicación **Django** en **Render (plan Free)** utilizando **PostgreSQL**, incluyendo la creación automática de un **superusuario**, incluso cuando **no existe acceso a consola interactiva**.

Es un flujo utilizado en entornos con **CI/CD** y servicios gestionados.

---

## Estructura del proyecto


<img width="1346" height="499" alt="image" src="https://github.com/user-attachments/assets/50cd6c47-c291-496f-a624-812b09863f41" />

### Uso de template

* https://templatemo.com/tm-562-space-dynamic#google_vignette 

```text
├── administrativo/
├── proyectoUno/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── build.sh
├── requirements.txt
└── README.md
```

El proyecto principal de Django es: **`proyectoUno`**

---

## Requisitos

- Python 3.10+
- Django
- Cuenta en Render
- Repositorio en GitHub

---

## Dependencias necesarias

En `requirements.txt` deben existir, como mínimo:

```text
Django
gunicorn
whitenoise
dj-database-url
psycopg2-binary
```

---

## Configuración en Django

### `ALLOWED_HOSTS`

En `proyectoUno/settings.py`:

```python
ALLOWED_HOSTS = ["*"]
```

---

### Archivos estáticos (WhiteNoise)

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Middleware:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```

---

### Base de datos (PostgreSQL vía variable de entorno)

```python
import os
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
        conn_max_age=600,
    )
}
```

Esto permite:
- PostgreSQL en Render
- SQLite en desarrollo local

---

## Creación de PostgreSQL en Render

1. Render → **New → PostgreSQL**
2. Plan: **Free**
3. Copiar **Internal Database URL**
4. En el Web Service agregar variable:

```text
DATABASE_URL=postgres://...
```

---

## Script de construcción (`build.sh`)

Archivo ubicado en la raíz del repositorio:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser --noinput || true
```

📌 El uso de `|| true` evita que el despliegue falle si el usuario ya existe.

---

## Creación automática del superusuario (Render Free)

Como Render Free **no tiene Shell**, el superusuario se crea usando **variables de entorno**, leídas automáticamente por Django.

### Variables requeridas

En Render → Web Service → Environment:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@ejemplo.com
DJANGO_SUPERUSER_PASSWORD=Admin123*
```

Durante el deploy, Django ejecuta internamente:

```bash
python manage.py createsuperuser --noinput
```

Y toma estos valores desde el entorno.

---

## Configuración del Web Service en Render

| Campo | Valor |
|-----|------|
| Runtime | Python 3 |
| Build Command | `./build.sh` |
| Start Command | `gunicorn proyectoUno.wsgi:application` |
| Plan | Free |

---

## Acceso al panel de administración

Una vez desplegado:

```
https://<su-app>.onrender.com/admin
```

Ingrese con el usuario y contraseña definidos en las variables de entorno.

---

## Consideraciones importantes

- El método automático de superusuario **es solo para demos o clases**
- En producción real:
  - se recomienda plan con Shell
  - o creación manual del usuario
- PostgreSQL Free en Render:
  - tiene límites
  - puede expirar tras 30 días

---

Proyecto académico – Despliegue de Django en la nube - René Elizalde
