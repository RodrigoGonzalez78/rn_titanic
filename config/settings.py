"""
Configuración central del proyecto Titanic ML
"""
import os
from pathlib import Path

# Directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent

# Directorios de datos
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_PROCESSED = DATA_DIR / "processed"

# Directorios de modelos
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_TRAINED = MODELS_DIR / "trained"
MODELS_ARTIFACTS = MODELS_DIR / "artifacts"

# Directorios de reportes
REPORTS_DIR = PROJECT_ROOT / "reports"

# URL del dataset
DATASET_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Parámetros por defecto del modelo
DEFAULT_MODEL_PARAMS = {
    "hidden_layer_sizes": (10,), 
    "activation": "relu", 
    "solver": "adam",
    "alpha": 0.0001,
    "learning_rate_init": 0.001, 
    "max_iter": 3000, 
    "random_state": 42
}

# Crear directorios si no existen
def ensure_dirs():
    """Crea todos los directorios necesarios"""
    for dir_path in [DATA_RAW, DATA_PROCESSED, MODELS_TRAINED, MODELS_ARTIFACTS, REPORTS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

# Paths a archivos específicos
def get_scaler_path():
    return MODELS_ARTIFACTS / "scaler.joblib"

def get_feature_names_path():
    return MODELS_ARTIFACTS / "feature_names.joblib"

def get_model_path(model_id: str):
    return MODELS_TRAINED / f"{model_id}.joblib"

def get_results_path():
    return REPORTS_DIR / "resultados_finales_tp5.csv"
