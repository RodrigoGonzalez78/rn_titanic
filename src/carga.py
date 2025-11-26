import pandas as pd

def cargar_y_limpiar_titanic(url):
 
    print(f"--- Cargando datos desde: {url} ---")
    df = pd.read_csv(url)

    # Eliminar columnas irrelevantes para la predicción
    cols_to_drop = ['PassengerId', 'Name', 'Ticket', 'Cabin']
    df = df.drop(cols_to_drop, axis=1)

    # Imputación de valores nulos (Fillna)
    # Edad: Rellenamos con el promedio
    df['Age'] = df['Age'].fillna(df['Age'].mean())
    
    # Embarque: Rellenamos con la moda (el valor más común)
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    
    print("Datos cargados y limpiados correctamente.")
    return df