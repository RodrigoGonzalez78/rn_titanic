"""
Módulo de carga de datos del Titanic
"""
import pandas as pd
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import settings

def cargar_y_limpiar_titanic(url=None):
    """
    Carga el dataset de Titanic y realiza limpieza básica.
    """
    if url is None:
        url = settings.DATASET_URL
        
    print(f"--- Cargando datos desde: {url} ---")
    
    # Carga
    df = pd.read_csv(url)
    
    # Limpieza Estándar
    # Eliminar columnas irrelevantes 
    cols_drop = ['PassengerId', 'Name', 'Ticket', 'Cabin']
    df = df.drop(columns=[c for c in cols_drop if c in df.columns], errors='ignore')
    
    # Rellenar valores nulos
    if 'Age' in df.columns:
        df['Age'] = df['Age'].fillna(df['Age'].median())
    if 'Embarked' in df.columns:
        df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    if 'Fare' in df.columns:
        df['Fare'] = df['Fare'].fillna(df['Fare'].median())
        
    print("Datos cargados y limpiados correctamente.")
    return df