import sys
from pathlib import Path

# Agregar el directorio raíz al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.web.app import app, serve

if __name__ == "__main__":
    print("Iniciando Dashboard Titanic...")
    print("Abre tu navegador en: http://localhost:5001")
    serve(port=5001)
