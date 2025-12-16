import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
import io
import base64
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import settings

def cargar_modelo(model_id: str):
    """Carga un modelo entrenado desde la carpeta models/trained/"""
    ruta = settings.get_model_path(model_id)
    if ruta.exists():
        return joblib.load(ruta)
    return None

def cargar_scaler():
    """Carga el scaler guardado"""
    ruta = settings.get_scaler_path()
    if ruta.exists():
        return joblib.load(ruta)
    return None

def cargar_feature_names():
    """Carga los nombres de las features"""
    ruta = settings.get_feature_names_path()
    if ruta.exists():
        return joblib.load(ruta)
    return None

def cargar_resultados():
    """Carga los resultados del CSV"""
    ruta = settings.get_results_path()
    if ruta.exists():
        return pd.read_csv(ruta)
    return None

def listar_modelos():
    """Lista todos los modelos disponibles"""
    modelos = []
    models_dir = settings.MODELS_TRAINED
    if models_dir.exists():
        for archivo in models_dir.iterdir():
            if archivo.suffix == '.joblib':
                model_id = archivo.stem
                modelos.append(model_id)
    return sorted(modelos)

def generar_roc_base64(model_id: str, X_test, y_test):
    """Genera una imagen de curva ROC en base64"""
    modelo = cargar_modelo(model_id)
    if modelo is None:
        return None
    
    # Obtener probabilidades
    y_proba = modelo.predict_proba(X_test)[:, 1]
    
    # Calcular curva ROC
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    
    # Colores que coinciden con la UI (tonos suaves)
    color_primary = '#58a6ff'  # Azul suave
    color_secondary = '#3fb950'  # Verde suave
    bg_color = '#0d1117'  # Fondo oscuro
    text_color = '#c9d1d9'  # Texto claro
    grid_color = '#21262d'  # Color de cards
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    # Curva ROC con gradiente verde-azul
    ax.plot(fpr, tpr, color=color_primary, lw=3, label=f'ROC curve (AUC = {roc_auc:.4f})')
    ax.fill_between(fpr, tpr, alpha=0.2, color=color_primary)
    ax.plot([0, 1], [0, 1], color=color_secondary, lw=2, linestyle='--', alpha=0.7)
    
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=12, color=text_color)
    ax.set_ylabel('True Positive Rate', fontsize=12, color=text_color)
    ax.set_title(f'Curva ROC - {model_id}', fontsize=14, color=text_color, fontweight='bold')
    ax.legend(loc="lower right", facecolor=grid_color, edgecolor=color_primary, labelcolor=text_color)
    ax.grid(True, alpha=0.3, color=grid_color)
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_color(grid_color)
    
    # Convertir a base64
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight', facecolor=bg_color)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    
    return img_base64, roc_auc

def preparar_entrada_prediccion(datos: dict):
    """
    Prepara los datos de entrada para predicción.
    Espera un diccionario con: Pclass, Sex, Age, SibSp, Parch, Fare, Embarked
    """
    scaler = cargar_scaler()
    feature_names = cargar_feature_names()
    
    if scaler is None or feature_names is None:
        return None
    
    # Mapeos
    sex_map = {'male': 1, 'female': 0, 'hombre': 1, 'mujer': 0}
    embarked_map = {'C': 0, 'Q': 1, 'S': 2, 'c': 0, 'q': 1, 's': 2}
    
    # Procesar datos
    sex_val = sex_map.get(datos.get('Sex', 'male').lower(), 1)
    embarked_val = embarked_map.get(datos.get('Embarked', 'S'), 2)
    
    # Crear array con las features en orden
    entrada = {
        'Pclass': int(datos.get('Pclass', 3)),
        'Sex': sex_val,
        'Age': float(datos.get('Age', 30)),
        'SibSp': int(datos.get('SibSp', 0)),
        'Parch': int(datos.get('Parch', 0)),
        'Fare': float(datos.get('Fare', 30)),
        'Embarked': embarked_val
    }
    
    # Crear DataFrame con el orden correcto de features
    df_entrada = pd.DataFrame([entrada])
    
    # Asegurar que las columnas estén en el orden correcto
    df_entrada = df_entrada[feature_names]
    
    # Escalar
    X_scaled = scaler.transform(df_entrada)
    
    return X_scaled

def predecir(model_id: str, datos: dict):
    """Realiza una predicción con el modelo especificado"""
    modelo = cargar_modelo(model_id)
    if modelo is None:
        return None, None
    
    X = preparar_entrada_prediccion(datos)
    if X is None:
        return None, None
    
    prediccion = modelo.predict(X)[0]
    probabilidad = modelo.predict_proba(X)[0]
    
    return prediccion, probabilidad
