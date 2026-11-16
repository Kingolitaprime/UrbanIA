import os
from dotenv import load_dotenv

load_dotenv()


def _normalizar_url(url):
    """Normaliza los esquemas de conexión entregados por proveedores."""
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("mysql://"):
        url = url.replace("mysql://", "mysql+pymysql://", 1)
    return url


EN_RENDER = os.getenv("RENDER", "").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Evita arrancar en producción con una clave pública/insegura o una SQLite efímera.
if EN_RENDER and not SECRET_KEY:
    raise RuntimeError("Falta configurar SECRET_KEY en el entorno de producción.")
if EN_RENDER and not DATABASE_URL:
    raise RuntimeError("Falta configurar DATABASE_URL con una base PostgreSQL persistente.")


class Config:
    SECRET_KEY = SECRET_KEY or "dev-inseguro-cambiar-en-produccion"
    SQLALCHEMY_DATABASE_URI = _normalizar_url(DATABASE_URL or "sqlite:///urbania.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "0") == "1"
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
