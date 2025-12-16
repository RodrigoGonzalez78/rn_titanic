from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
import joblib
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import settings

def preparar_datos(df, target_col='Survived'):
    """
    Prepara los datos para entrenamiento: encoding, split, balanceo y escalado.
    Guarda el scaler y los nombres de features para uso posterior.
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

    # Split (División) - 80% Train, 20% Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Balanceo (Solo en Training)
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    print(f"Balanceo aplicado. Train original: {len(y_train)}, Train balanceado: {len(y_train_res)}")

    # Escalado (StandardScaler)
    scaler = StandardScaler()
    X_train_final = scaler.fit_transform(X_train_res)
    X_test_final = scaler.transform(X_test)
    
    # Guardar el scaler para uso en predicciones
    scaler_path = settings.get_scaler_path()
    joblib.dump(scaler, scaler_path)
    print(f"Scaler guardado en: {scaler_path}")
    
    # Guardar los nombres de las features
    feature_names_path = settings.get_feature_names_path()
    joblib.dump(list(X.columns), feature_names_path)

    return X_train_final, X_test_final, y_train_res, y_test