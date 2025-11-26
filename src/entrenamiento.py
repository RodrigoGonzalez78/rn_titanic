from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

def entrenar_y_evaluar(config, X_train, y_train, X_test, y_test):
    """
    Crea un modelo basado en 'config', lo entrena y evalúa.
    Retorna un diccionario con los resultados.
    """
    nombre = config.get('nombre', 'Modelo')
    params = config.get('params', {})
    
    print(f"Entrenando: {nombre}...")
    
    # Instanciar Modelo (Pipeline de construcción)
    clf = MLPClassifier(**params)
    
    # Entrenamiento
    clf.fit(X_train, y_train)
    
    # Predicción
    y_pred = clf.predict(X_test)
    
    #Cálculo de Métricas (Tabla de resultados)
    metrics = {
        "ID": config.get('id'),
        "Descripción": nombre,
        "Accuracy": round(accuracy_score(y_test, y_pred), 4),
        "Precision": round(precision_score(y_test, y_pred), 4),
        "Recall": round(recall_score(y_test, y_pred), 4),
        "F1-Score": round(f1_score(y_test, y_pred), 4),
        "Params": str(params)
    }
    
    return metrics