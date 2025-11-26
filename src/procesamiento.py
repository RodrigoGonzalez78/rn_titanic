from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE

def preparar_datos(df, target_col='Survived'):
   
    # Encoding (Texto -> Números)
    le = LabelEncoder()
    
    # Identificamos columnas categóricas automáticamente o manual
    cat_cols = ['Sex', 'Embarked']
    for col in cat_cols:
        if col in df.columns:
            df[col] = le.fit_transform(df[col])

    # Separar X (Features) e y (Target)
    X = df.drop(target_col, axis=1)
    y = df[target_col]

    # Split (División) - 80% Train, 20% Test
    # Hacemos el split ANTES del balanceo para no contaminar el test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Balanceo (Solo en Training)
    # Aplicar técnicas como Over-Sampling
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    print(f"Balanceo aplicado. Train original: {len(y_train)}, Train balanceado: {len(y_train_res)}")

    # Escalado (StandardScaler)
    # Ajustamos el escalador solo con datos de train para evitar sesgo
    scaler = StandardScaler()
    X_train_final = scaler.fit_transform(X_train_res)
    X_test_final = scaler.transform(X_test)

    return X_train_final, X_test_final, y_train_res, y_test