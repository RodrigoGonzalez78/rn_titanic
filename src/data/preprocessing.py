from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
import joblib
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import settings

def preparar_datos(df, target_col='Survived', test_size=0.2, val_size=0.2):
    """
    Prepara los datos para entrenamiento: encoding, split, balanceo y escalado.
    Guarda el scaler y los nombres de features para uso posterior.
    
    Args:
        df: DataFrame con los datos
        target_col: Nombre de la columna objetivo
        test_size: Proporción para test (del total)
        val_size: Proporción para validación (del conjunto train)
    
    Returns:
        X_train, X_val, X_test, y_train, y_val, y_test
    """
    # Asegurar que existan los directorios
    settings.ensure_dirs()
    
    # Encoding (Texto -> Números)
    le = LabelEncoder()
    
    # Identificamos columnas categóricas
    cat_cols = ['Sex', 'Embarked']
    for col in cat_cols:
        if col in df.columns:
            df[col] = le.fit_transform(df[col])

    # Separar X (Features) e y (Target)
    X = df.drop(target_col, axis=1)
    y = df[target_col]

    # Split (División) - Primero separamos Test (20% del total)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    # Luego separamos Validation del resto (20% del 80% = 16% del total)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=42, stratify=y_temp
    )
    
    print(f"División de datos:")
    print(f"  - Train: {len(y_train)} ({len(y_train)/len(y)*100:.1f}%)")
    print(f"  - Validation: {len(y_val)} ({len(y_val)/len(y)*100:.1f}%)")
    print(f"  - Test: {len(y_test)} ({len(y_test)/len(y)*100:.1f}%)")

    # Balanceo (Solo en Training)
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    print(f"Balanceo aplicado. Train original: {len(y_train)}, Train balanceado: {len(y_train_res)}")

    # Escalado (StandardScaler)
    scaler = StandardScaler()
    X_train_final = scaler.fit_transform(X_train_res)
    X_val_final = scaler.transform(X_val)
    X_test_final = scaler.transform(X_test)
    
    # Guardar el scaler para uso en predicciones
    scaler_path = settings.get_scaler_path()
    joblib.dump(scaler, scaler_path)
    print(f"Scaler guardado en: {scaler_path}")
    
    # Guardar los nombres de las features
    feature_names_path = settings.get_feature_names_path()
    joblib.dump(list(X.columns), feature_names_path)

    return X_train_final, X_val_final, X_test_final, y_train_res, y_val, y_test