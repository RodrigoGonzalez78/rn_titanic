"""
Módulo de entrenamiento de modelos MLP
"""
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import joblib
import time
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import settings

def entrenar_y_evaluar(config, X_train, y_train, X_test, y_test):
    """
    Crea un modelo basado en 'config', lo entrena y evalúa.
    Guarda el modelo entrenado en la carpeta 'models/trained/'.
    Retorna un diccionario con los resultados.
    """
    # Asegurar que existan los directorios
    settings.ensure_dirs()
    
    nombre = config.get('nombre', 'Modelo')
    model_id = config.get('id', 'modelo')
    params = config.get('params', {})
    
    print(f"Entrenando: {nombre}...")
    
    # Instanciar Modelo
    clf = MLPClassifier(**params)
    
    # Entrenamiento (con medición de tiempo)
    start_time = time.time()
    clf.fit(X_train, y_train)
    end_time = time.time()
    tiempo_total = round(end_time - start_time, 4)
    
    # Predicción
    y_pred = clf.predict(X_test)
    
    # Cálculo de Métricas
    metrics = {
        "ID": config.get('id'),
        "Descripción": nombre,
        "Accuracy": round(accuracy_score(y_test, y_pred), 4),
        "Precision": round(precision_score(y_test, y_pred), 4),
        "Recall": round(recall_score(y_test, y_pred), 4),
        "F1-Score": round(f1_score(y_test, y_pred), 4),
        "Tiempo (s)": tiempo_total,
        "Params": str(params)
    }
    
    # Guardar el modelo entrenado
    ruta_modelo = settings.get_model_path(model_id)
    joblib.dump(clf, ruta_modelo)
    print(f"  -> Modelo guardado en: {ruta_modelo}")
    
    return metrics