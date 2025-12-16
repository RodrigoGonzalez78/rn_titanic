import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio raíz al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import settings
from src.data.loader import cargar_y_limpiar_titanic
from src.data.preprocessing import preparar_datos
from src.models.trainer import entrenar_y_evaluar

def main():
    # Asegurar directorios
    settings.ensure_dirs()
    
    # 1. Carga
    df_raw = cargar_y_limpiar_titanic()
    
    # 2. Preprocesamiento
    X_train, X_test, y_train, y_test = preparar_datos(df_raw)
    
    # 3. Definición de Experimentos
    base_params = settings.DEFAULT_MODEL_PARAMS.copy()

    experimentos = [
        {
            "id": "1_BASE",
            "nombre": "Reference (Simple)",
            "params": base_params.copy()
        },
        {
            "id": "2_DEEP",
            "nombre": "Deep Network (Profunda)",
            "params": {**base_params, "hidden_layer_sizes": (64, 32, 16, 8)} 
        },
        {
            "id": "3_WIDE",
            "nombre": "Wide Network (Ancha)",
            "params": {**base_params, "hidden_layer_sizes": (100,)} 
        },

        {
            "id": "4_ACTIVATION",
            "nombre": "Activación Tanh",
            "params": {**base_params, "activation": "tanh"} 
        },
        {
            "id": "5_SOLVER_SGD",
            "nombre": "Optimizador SGD",
            "params": {**base_params, "solver": "sgd", "learning_rate": "adaptive"} 
        },
        
        {
            "id": "6_LBFGS_OPTIM",
            "nombre": "Solver LBFGS (Matemático)",
            "params": {
                **base_params, 
                "solver": "lbfgs",
                "max_iter": 5000
            }
        },

    ]
    
    # 4. Ejecución
    resultados = []
    
    print(f"\n--- INICIANDO BATERÍA DE {len(experimentos)} EXPERIMENTOS ---")
    
    for exp in experimentos:
        res = entrenar_y_evaluar(exp, X_train, y_train, X_test, y_test)
        resultados.append(res)
        
    df_resultados = pd.DataFrame(resultados)
    df_resultados = df_resultados.sort_values(by="F1-Score", ascending=False)
    
    print("\n" + "="*100)
    print("RANKING DE MODELOS (TP 5 - IA CONEXIONISTA)")
    print("="*100)
    
    cols_view = ["ID", "Descripción", "Accuracy", "F1-Score", "Recall", "Precision", "Tiempo (s)"]
    print(df_resultados[cols_view].to_string(index=False))
    
    # Guardar resultados
    results_path = settings.get_results_path()
    df_resultados.to_csv(results_path, index=False)
    print(f"\n[INFO] Resultados guardados en '{results_path}'.")

if __name__ == "__main__":
    main()
