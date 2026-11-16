# UrbanIA Córdoba

Plataforma web para analizar el crecimiento urbano y la pérdida de espacios verdes de 24 ciudades de la
Provincia de Córdoba con imágenes satelitales **reales** (Sentinel-2) e Inteligencia Artificial (Gemini).
Trabajo Final Integrador – Aplicaciones Informáticas (Opción 4: UrbanIA).

## Ejecutar en local
```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # editar SECRET_KEY y GEMINI_API_KEY
python init_db.py                                     # crea tablas + datos de prueba (SQLite por defecto)
flask --app app run --debug                           # http://127.0.0.1:5000
```
> `rasterio` trae GDAL en su rueda para Windows/Linux/macOS con Python 3.9–3.12. Si falla la instalación, use Python 3.11.

## Novedades de la versión 2
- Resultados en **5 pestañas**: Antes y después · Cambios detectados · Estadísticas · Informe · Fuentes.
- **Cambios específicos**: zonas de nueva urbanización / pérdida / ganancia de vegetación con tamaño, dirección y distancia al centro, botón para ver un punto de referencia aproximado en el mapa, crecimiento por dirección y descarga CSV/PNG.
- **Mapa más fácil de leer**: guía de colores y años sobre el mapa, orientación sencilla (norte arriba), explicación de los filtros y superficies comparadas con canchas de fútbol.
- **Comparación y orientación**: separador deslizante para comparar ambos años, explicación del área comparable sin nubes ni sombras, guía rápida de uso y marcador que aclara que solo indica una ubicación aproximada (no un límite exacto).
- **Accesibilidad**: tamaño de texto, alto contraste, colores aptos para daltonismo, pestañas con teclado, tablas equivalentes a los gráficos, resumen en lenguaje simple y lectura en voz alta.
- **Resumen provincial** (`/resumen`): ranking de ciudades y totales por cluster.

> **Si ya había ejecutado la versión 1:** se agregó la columna `cambios_json`. Borre `instance/urbania.db` (o `urbania.db`) y
> ejecute de nuevo `python init_db.py`. En MySQL/PostgreSQL: `ALTER TABLE analisis_urbano ADD COLUMN cambios_json TEXT;`.
> También ejecute `pip install -r requirements.txt` (se agregó `scipy`).

## Usuarios de prueba (cambiar en producción con las variables *_PASSWORD)
| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | admin@urbania.local | Admin1234! |
| Planificador Urbano | planificador@urbania.local | Plan1234! |
| Consultor | consultor@urbania.local | Cons1234! |

## Estructura
```
app.py          rutas, autenticación, roles, CSRF, CRUD, API
models.py       8 tablas (SQLAlchemy)
analisis.py     núcleo numérico: índices, clasificación, comparación, zonas de cambio, PNG (sin red)
satelite.py     búsqueda STAC + lectura de Sentinel-2 (rasterio)
ia.py           informe con Gemini (multimodal) + plan B sin IA
init_db.py      crea tablas y carga datos
schema.sql      esquema MySQL equivalente
templates/ static/   frontend (HTML5, CSS3, JavaScript: visor.js, accesibilidad.js, resumen.js...)
```

## Despliegue (Render + base remota)
1. Subir a GitHub (sin `.env`).
2. Base de datos: MySQL en Aiven o PostgreSQL en Supabase. Copiar la URL de conexión.
3. Render → New Web Service → repositorio. Build: `pip install -r requirements.txt && python init_db.py`.
   Start: `gunicorn app:app --workers 1 --threads 4 --timeout 180`.
4. Variables de entorno: `SECRET_KEY`, `DATABASE_URL`, `GEMINI_API_KEY`, `COOKIE_SECURE=1`, y las `*_PASSWORD`.
5. Render asigna `https://<nombre>.onrender.com` (subdominio público). Opcional: dominio propio en *Settings → Custom Domains*.

## Aviso
Las superficies son **estimaciones** por teledetección (umbrales de índices espectrales), no mediciones confirmadas.
Los registros marcados "[PRUEBA]" son ilustrativos y no provienen de imágenes reales.
