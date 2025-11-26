import pandas as pd
import carga
import procesamiento
import entrenamiento

# URL del dataset
URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

def main():
    # 1. Carga
    df_raw = carga.cargar_y_limpiar_titanic(URL)
    
    # 2. Preprocesamiento
    X_train, X_test, y_train, y_test = procesamiento.preparar_datos(df_raw)
    
    # 3. Definición de Experimentos Avanzados
    # El TP sugiere variar capas, neuronas, funciones y otros hiperparámetros 
    
    base_params = {
        "hidden_layer_sizes": (10,), 
        "activation": "relu", 
        "solver": "adam",
        "alpha": 0.0001, # Regularización estándar
        "learning_rate_init": 0.001, 
        "max_iter": 3000, 
        "random_state": 42
    }

    experimentos = [
        # --- GRUPO 1: Arquitectura ---
        {
            "id": "1_BASE",
            "nombre": "Reference (Simple)",
            "params": base_params.copy()
        },
        {
            "id": "2_DEEP",
            "nombre": "Deep Network (Profunda)",
            "params": {**base_params, "hidden_layer_sizes": (64, 32, 16, 8)} 
            # Hipótesis: Más capas capturan patrones más complejos.
        },
        {
            "id": "3_WIDE",
            "nombre": "Wide Network (Ancha)",
            "params": {**base_params, "hidden_layer_sizes": (100,)} 
            # Hipótesis: Muchas neuronas en una capa pueden memorizar mejor.
        },

        # --- GRUPO 2: Hiperparámetros de Aprendizaje ---
        {
            "id": "4_ACTIVATION",
            "nombre": "Activación Tanh",
            "params": {**base_params, "activation": "tanh"} 
            # Hipótesis: Tanh maneja mejor valores negativos que ReLU en ciertos casos.
        },
        {
            "id": "5_SOLVER_SGD",
            "nombre": "Optimizador SGD",
            "params": {**base_params, "solver": "sgd", "learning_rate": "adaptive"} 
            # Hipótesis: Descenso de Gradiente Estocástico a veces generaliza mejor que Adam.
        },
        
        # --- GRUPO 3: Regularización (Evitar Overfitting) ---
        {
            "id": "6_REGULARIZED",
            "nombre": "Alta Regularización",
            "params": {**base_params, "hidden_layer_sizes": (100, 50), "alpha": 0.05} 
            # Hipótesis: Un alpha alto penaliza pesos grandes y reduce el sobreajuste.
        },
        
        # --- NUEVO INTENTO 1: SOLVER LBFGS (Arma secreta para data tabular) ---
        {
            "id": "7_LBFGS_OPTIM",
            "nombre": "Solver LBFGS (Matemático)",
            "params": {
                **base_params, 
                "solver": "lbfgs",       # <--- CAMBIO CLAVE
                "max_iter": 5000         # LBFGS necesita más iteraciones
                # Nota: LBFGS no usa learning_rate_init, lo ajusta solo
            }
        },

        # --- NUEVO INTENTO 2: PIRÁMIDE (Estructura media) ---
        {
            "id": "8_PYRAMID",
            "nombre": "Pirámide (30->15)",
            "params": {
                **base_params,
                "hidden_layer_sizes": (30, 15), # Más capacidad que Base, menos que Deep
                "alpha": 0.01                   # Regularización suave para precisión
            }
        },

        # --- NUEVO INTENTO 3: PRECISIÓN QUIRÚRGICA (Lento y seguro) ---
        {
            "id": "9_SLOW_LEARN",
            "nombre": "Aprendizaje Fino",
            "params": {
                **base_params,
                "hidden_layer_sizes": (20,),    # Un poco más de neuronas
                "learning_rate_init": 0.0005,   # Aprende más lento (más preciso)
                "max_iter": 5000                # Más tiempo
            }
        }
    ]
    
    # 4. Ejecución
    resultados = []
    
    print(f"\n--- INICIANDO BATERÍA DE {len(experimentos)} EXPERIMENTOS ---")
    
    for exp in experimentos:
        # Llamamos al trainer (asegúrate de tener el archivo trainer.py del paso anterior)
        res = entrenamiento.entrenar_y_evaluar(exp, X_train, y_train, X_test, y_test)
        resultados.append(res)
        
  
    df_resultados = pd.DataFrame(resultados)
    
   
    df_resultados = df_resultados.sort_values(by="F1-Score", ascending=False)
    
    print("\n" + "="*100)
    print("RANKING DE MODELOS (TP 5 - IA CONEXIONISTA)")
    print("="*100)
    
    cols_view = ["ID", "Descripción", "Accuracy", "F1-Score", "Recall", "Precision"]
    print(df_resultados[cols_view].to_string(index=False))
    
   
    df_resultados.to_csv("resultados_finales_tp5.csv", index=False)
    print("\n[INFO] Resultados guardados en 'resultados_finales_tp5.csv' para la infografía.")

if __name__ == "__main__":
    main()