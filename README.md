# UrbanIA Córdoba

Aplicación web Flask para estimar cambios en el crecimiento urbano y la cobertura vegetal de ciudades de Córdoba mediante imágenes Sentinel-2. Puede generar informes con Gemini si se configura una clave API; si no, utiliza un informe alternativo basado en reglas.

## Importante: GitHub y publicación web

UrbanIA **no es un sitio estático**: necesita Python/Flask, procesamiento geoespacial y una base de datos. GitHub sirve para guardar el código, pero **GitHub Pages no puede ejecutar esta aplicación**.

La configuración incluida permite publicar la aplicación en **Render** conectada a este repositorio. Render te asignará una dirección pública similar a `https://urbania.onrender.com` (el nombre exacto depende de la disponibilidad). También podrás conectar un dominio propio desde Render.

## 1. Subir el proyecto a GitHub

1. Descargá y descomprimí este ZIP.
2. En GitHub, creá un repositorio llamado `UrbanIA` (o el nombre que prefieras).
3. Subí el contenido de la carpeta `UrbanIA` al nivel principal del repositorio. La carpeta raíz debe contener `app.py`, `requirements.txt`, `render.yaml` y `README.md`.
4. Verificá que GitHub no haya recibido `.env`, bases `.db` ni carpetas `venv`. Están excluidas mediante `.gitignore`.

## 2. Crear la base de datos

UrbanIA necesita una base PostgreSQL persistente para producción. Creá una instancia PostgreSQL en un proveedor compatible (por ejemplo, Supabase o Neon) y copiá la URL de conexión que permita conexiones externas.

No uses la base SQLite local para producción: el disco de una instancia gratuita puede ser efímero y perder datos al reiniciarse.

## 3. Publicar en Render

1. Iniciá sesión en [Render](https://render.com/).
2. Elegí **New + → Blueprint** y conectá tu cuenta de GitHub.
3. Seleccioná el repositorio donde subiste UrbanIA. Render detectará `render.yaml`.
4. Completá las variables solicitadas:
   - `DATABASE_URL`: URL de PostgreSQL.
   - `ADMIN_PASSWORD`: contraseña nueva y segura para el administrador.
   - `PLANIFICADOR_PASSWORD`: contraseña nueva para el planificador.
   - `CONSULTOR_PASSWORD`: contraseña nueva para el consultor.
   - `GEMINI_API_KEY`: opcional. Si no la completás, los informes se generan sin Gemini.
5. Confirmá la creación. Render instalará las dependencias, inicializará las tablas y arrancará Gunicorn.
6. Cuando el servicio figure como **Live**, abrí la URL `onrender.com` que muestra Render. La ruta inicial `/` lleva al inicio de sesión.

**No publiques ni compartas contraseñas, claves API ni la URL privada de la base de datos.** Configuralas en el panel de Render, nunca dentro del código ni en GitHub.

## 4. Usuarios iniciales

La primera inicialización crea estos usuarios:

| Rol | Correo |
|---|---|
| Administrador | `admin@urbania.local` |
| Planificador Urbano | `planificador@urbania.local` |
| Consultor | `consultor@urbania.local` |

Las contraseñas son las que hayas definido en las variables de Render. Si ya existe el usuario en la base, cambiar una variable no modifica su contraseña existente; en ese caso debe cambiarse desde la administración de usuarios o actualizarse de forma controlada en la base.

## 5. Ejecutar localmente en Windows

Recomendado: Python 3.11.

```powershell
py -3.11 -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python init_db.py
flask --app app run --debug
```

Abrí `http://127.0.0.1:5000`. Para desarrollo local, `.env.example` contiene contraseñas de demostración: cambialas si el entorno no es privado.

## Comprobaciones y limitaciones

- La sintaxis de los módulos Python y JavaScript fue comprobada.
- La aplicación usa autenticación, roles y protección CSRF en formularios y operaciones POST.
- Los análisis satelitales necesitan acceso de red al catálogo Sentinel-2 y a los archivos GeoTIFF remotos; la disponibilidad depende de esos servicios.
- La instalación de `rasterio`/GDAL puede tardar y requiere una plataforma compatible.
- El plan gratuito de Render puede suspender el servicio por inactividad; la primera apertura posterior puede demorar.
- Las estadísticas son estimaciones de teledetección, no mediciones confirmadas en terreno.
- Los registros `[PRUEBA]` son datos ilustrativos, no resultados de imágenes satelitales reales.

## Estructura principal

- `app.py`: servidor Flask, autenticación, roles, rutas y API.
- `models.py`: modelos de base de datos.
- `analisis.py`: procesamiento y comparación de imágenes.
- `satelite.py`: consulta y lectura de escenas Sentinel-2.
- `ia.py`: informes con Gemini y alternativa basada en reglas.
- `init_db.py`: creación de tablas y datos iniciales.
- `templates/` y `static/`: interfaz web.
