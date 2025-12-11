# Titanic Survival Prediction 🚢

Proyecto de Machine Learning para predecir la supervivencia de pasajeros del Titanic usando Redes Neuronales (MLP).

## 📁 Estructura del Proyecto

```
rn_titanic/
├── config/                 # Configuración centralizada
│   ├── __init__.py
│   └── settings.py        # Paths y parámetros globales
│
├── data/                   # Datos
│   ├── raw/               # Datos crudos
│   └── processed/         # Datos procesados
│
├── models/                 # Modelos entrenados
│   ├── trained/           # Archivos .joblib de modelos
│   └── artifacts/         # Scaler, feature names, etc.
│
├── notebooks/              # Jupyter notebooks (exploración)
│
├── reports/                # Resultados y métricas
│   └── resultados_finales_tp5.csv
│
├── src/                    # Código fuente
│   ├── data/              # Carga y preprocesamiento
│   │   ├── loader.py
│   │   └── preprocessing.py
│   ├── models/            # Entrenamiento y utilidades
│   │   ├── trainer.py
│   │   └── utils.py
│   ├── visualization/     # Gráficos y visualizaciones
│   └── web/               # Dashboard web
│       └── app.py
│
├── train.py               # Script principal de entrenamiento
├── run_dashboard.py       # Ejecutar dashboard web
├── requirements.txt       # Dependencias
└── README.md
```

## 🚀 Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd rn_titanic

# Crear entorno virtual (opcional)
conda create -n titanic python=3.10
conda activate titanic

# Instalar dependencias
pip install -r requirements.txt
```

## 📊 Uso

### Entrenar Modelos

```bash
python train.py
```

Esto entrenará 9 modelos MLP con diferentes configuraciones y guardará:
- Los modelos entrenados en `models/trained/`
- Las métricas en `reports/resultados_finales_tp5.csv`

### Ejecutar Dashboard Web

```bash
python run_dashboard.py
```

Abre tu navegador en `http://localhost:5001` para:
- Ver el ranking de modelos
- Explorar métricas y curvas ROC
- Probar predicciones con datos personalizados

### Docker

```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build

# O solo construir la imagen
docker build -t titanic-ml .

# Ejecutar el contenedor
docker run -p 5001:5001 titanic-ml
```

Accede al dashboard en `http://localhost:5001`

## 🧪 Modelos Implementados

| ID | Descripción | Características |
|----|-------------|-----------------|
| 1_BASE | Reference (Simple) | Red básica (10 neuronas) |
| 2_DEEP | Deep Network | 4 capas (64, 32, 16, 8) |
| 3_WIDE | Wide Network | 1 capa amplia (100) |
| 4_ACTIVATION | Activación Tanh | Función tanh |
| 5_SOLVER_SGD | Optimizador SGD | SGD adaptativo |
| 6_REGULARIZED | Alta Regularización | alpha=0.05 |
| 7_LBFGS_OPTIM | Solver LBFGS | Optimizador matemático |
| 8_PYRAMID | Pirámide | Arquitectura 30->15 |
| 9_SLOW_LEARN | Aprendizaje Fino | Learning rate bajo |

## 📈 Métricas

Cada modelo es evaluado con:
- **Accuracy**: Precisión general
- **F1-Score**: Balance entre precisión y recall
- **Precision**: Verdaderos positivos / Predichos positivos
- **Recall**: Verdaderos positivos / Total positivos
- **Tiempo**: Duración del entrenamiento

## 🛠️ Tecnologías

- **Python 3.10+**
- **scikit-learn**: MLPClassifier
- **pandas/numpy**: Manipulación de datos
- **imbalanced-learn**: SMOTE para balanceo
- **FastHTML**: Dashboard web
- **matplotlib**: Visualizaciones