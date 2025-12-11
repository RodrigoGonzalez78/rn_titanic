"""
Dashboard Web para visualizar métricas y probar modelos Titanic
Usando FastHTML
"""
from fasthtml.common import *
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.models import utils
from src.data import loader, preprocessing
from config import settings

# Crear la aplicación FastHTML
app, rt = fast_app(
    hdrs=(
        Style("""
            :root {
                --bg-primary: #0d1117;
                --bg-secondary: #161b22;
                --bg-card: #21262d;
                --accent: #58a6ff;
                --accent-light: #388bfd;
                --text-primary: #c9d1d9;
                --text-secondary: #8b949e;
                --success: #3fb950;
                --warning: #d29922;
                --info: #58a6ff;
            }
            
            * { box-sizing: border-box; margin: 0; padding: 0; }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
                color: var(--text-primary);
                min-height: 100vh;
                padding: 2rem;
            }
            
            .container { max-width: 1200px; margin: 0 auto; }
            
            h1 {
                text-align: center;
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                background: linear-gradient(90deg, var(--accent), var(--accent-light));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .subtitle {
                text-align: center;
                color: var(--text-secondary);
                margin-bottom: 2rem;
            }
            
            .nav {
                display: flex;
                justify-content: center;
                gap: 1rem;
                margin-bottom: 2rem;
            }
            
            .nav a {
                background: var(--bg-card);
                color: var(--text-primary);
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                text-decoration: none;
                transition: all 0.3s;
                border: 1px solid transparent;
            }
            
            .nav a:hover, .nav a.active {
                border-color: var(--accent);
                box-shadow: 0 0 15px rgba(88, 166, 255, 0.25);
            }
            
            .card {
                background: var(--bg-card);
                border-radius: 15px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            }
            
            .card h2 {
                color: var(--accent-light);
                margin-bottom: 1rem;
                font-size: 1.3rem;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
            }
            
            th, td {
                padding: 1rem;
                text-align: left;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            
            th {
                background: rgba(88, 166, 255, 0.15);
                color: var(--accent);
                font-weight: 600;
            }
            
            tr:hover { background: rgba(255,255,255,0.05); }
            
            .metric {
                display: inline-block;
                background: var(--bg-secondary);
                padding: 0.5rem 1rem;
                border-radius: 20px;
                margin: 0.25rem;
                font-size: 0.9rem;
            }
            
            .metric-value {
                color: var(--success);
                font-weight: bold;
            }
            
            .btn {
                background: linear-gradient(90deg, var(--accent), var(--accent-light));
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1rem;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(88, 166, 255, 0.3);
            }
            
            .btn-small {
                padding: 0.5rem 1rem;
                font-size: 0.85rem;
            }
            
            .form-group {
                margin-bottom: 1rem;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--text-secondary);
            }
            
            .form-group input, .form-group select {
                width: 100%;
                padding: 0.75rem;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.1);
                background: var(--bg-secondary);
                color: var(--text-primary);
                font-size: 1rem;
            }
            
            .form-group input:focus, .form-group select:focus {
                outline: none;
                border-color: var(--accent);
            }
            
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
            
            .result-box {
                text-align: center;
                padding: 2rem;
                border-radius: 15px;
                margin-top: 1rem;
            }
            
            .result-survive {
                background: linear-gradient(135deg, #238636, #2ea043);
                color: #c9d1d9;
            }
            
            .result-die {
                background: linear-gradient(135deg, #8b3535, #a04040);
                color: #c9d1d9;
            }
            
            .result-box h3 { font-size: 1.5rem; margin-bottom: 0.5rem; }
            .result-box p { font-size: 1.1rem; opacity: 0.9; }
            
            .roc-container {
                text-align: center;
                padding: 1rem;
            }
            
            .roc-container img {
                max-width: 100%;
                border-radius: 10px;
            }
            
            .back-link {
                display: inline-block;
                color: var(--accent);
                text-decoration: none;
                margin-bottom: 1rem;
            }
            
            .back-link:hover { text-decoration: underline; }
            
            .model-link {
                color: var(--accent-light);
                text-decoration: none;
            }
            
            .model-link:hover { text-decoration: underline; }
            
            .params-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 1rem;
            }
            
            .param-item {
                background: linear-gradient(135deg, var(--bg-secondary) 0%, rgba(88, 166, 255, 0.05) 100%);
                border-radius: 12px;
                padding: 1rem 1.25rem;
                border-left: 3px solid var(--accent);
                transition: all 0.3s ease;
            }
            
            .param-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(88, 166, 255, 0.15);
                border-left-color: var(--accent-light);
            }
            
            .param-label {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.8rem;
                color: var(--text-secondary);
                margin-bottom: 0.4rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .param-value {
                font-size: 1.1rem;
                color: var(--success);
                font-weight: 600;
                font-family: 'Fira Code', 'Consolas', monospace;
                word-break: break-word;
            }
            
            .param-value.string { color: #a5d6ff; }
            .param-value.number { color: #79c0ff; }
            .param-value.bool { color: #d2a8ff; }
            .param-value.none { color: var(--text-secondary); font-style: italic; }
            
            .param-icon {
                font-size: 1rem;
            }
        """),
    ),
    title="🚢 Dashboard Titanic - IA Conexionista"
)

import json

def crear_seccion_parametros(modelo_info):
    """Crea una sección visual para los parámetros del modelo"""
    params_raw = modelo_info.get('Params', 'N/A')
    
    # Si no hay parámetros, mostrar mensaje simple
    if not params_raw or params_raw == 'N/A':
        return Div(
            H2("⚙️ Parámetros"),
            P("No hay información de parámetros disponible", style="color: var(--text-secondary); font-style: italic;"),
            cls="card"
        )
    
    # Intentar parsear como JSON o diccionario de Python
    try:
        if isinstance(params_raw, str):
            # Limpiar el string para parseo
            params_str = params_raw.strip()
            # Convertir sintaxis de Python a JSON donde sea posible
            # Reemplazar tuplas (10,) por listas [10]
            import re
            params_str = re.sub(r'\((\d+),\)', r'[\1]', params_str)
            params_str = re.sub(r'\((\d+,\s*\d+(?:,\s*\d+)*)\)', r'[\1]', params_str)
            params_str = params_str.replace("'", '"')
            params_str = params_str.replace("True", "true").replace("False", "false")
            params_str = params_str.replace("None", "null")
            params = json.loads(params_str)
        else:
            params = params_raw
    except Exception as e:
        # Si falla el parseo, mostrar como texto formateado
        return Div(
            H2("⚙️ Parámetros"),
            Pre(str(params_raw), style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; overflow-x: auto; white-space: pre-wrap;"),
            cls="card"
        )
    
    # Mapeo de nombres de parámetros a descripciones e iconos más amigables
    param_labels = {
        'hidden_layer_sizes': ('🧠', 'Capas Ocultas'),
        'hidden_layers': ('🧠', 'Capas Ocultas'),
        'activation': ('⚡', 'Función de Activación'),
        'solver': ('🔧', 'Optimizador'),
        'alpha': ('📊', 'Regularización (alpha)'),
        'learning_rate': ('📈', 'Tasa de Aprendizaje'),
        'learning_rate_init': ('🚀', 'LR Inicial'),
        'max_iter': ('🔄', 'Iteraciones Máx.'),
        'batch_size': ('📦', 'Tamaño de Batch'),
        'momentum': ('💨', 'Momentum'),
        'early_stopping': ('🛑', 'Parada Temprana'),
        'validation_fraction': ('✅', 'Fracción Validación'),
        'n_iter_no_change': ('⏳', 'Iteraciones Sin Cambio'),
        'tol': ('🎯', 'Tolerancia'),
        'random_state': ('🎲', 'Semilla Aleatoria'),
        'shuffle': ('🔀', 'Mezclar Datos'),
        'verbose': ('📝', 'Modo Verbose'),
        'warm_start': ('🔥', 'Inicio Caliente'),
        'nesterovs_momentum': ('🏃', 'Momentum Nesterov'),
        'beta_1': ('β₁', 'Beta 1 (Adam)'),
        'beta_2': ('β₂', 'Beta 2 (Adam)'),
        'epsilon': ('ε', 'Epsilon'),
        'power_t': ('📉', 'Power T'),
    }
    
    # Crear items de parámetros
    param_items = []
    for key, value in params.items():
        icon, label = param_labels.get(key, ('⚙️', key.replace('_', ' ').title()))
        
        # Determinar clase de estilo según tipo de valor
        if value is None:
            value_class = "param-value none"
            display_value = "Auto"
        elif isinstance(value, bool):
            value_class = "param-value bool"
            display_value = "Sí ✓" if value else "No ✗"
        elif isinstance(value, (int, float)):
            value_class = "param-value number"
            display_value = str(value)
        elif isinstance(value, (list, tuple)):
            value_class = "param-value string"
            display_value = str(value)
        else:
            value_class = "param-value string"
            display_value = str(value)
        
        param_items.append(
            Div(
                Div(
                    Span(icon, cls="param-icon"),
                    Span(label),
                    cls="param-label"
                ),
                Div(display_value, cls=value_class),
                cls="param-item"
            )
        )
    
    return Div(
        H2("⚙️ Parámetros del Modelo"),
        Div(*param_items, cls="params-grid"),
        cls="card"
    )

def nav_bar(active=""):
    return Div(
        A("📊 Métricas", href="/", cls="active" if active == "metrics" else ""),
        A("🔮 Predictor", href="/predecir", cls="active" if active == "predict" else ""),
        cls="nav"
    )

@rt("/")
def home():
    """Página principal con tabla de métricas"""
    df = utils.cargar_resultados()
    
    if df is None:
        return Div(
            H1("🚢 Dashboard Titanic"),
            P("No se encontraron resultados. Ejecuta primero el entrenamiento.", cls="subtitle"),
            cls="container"
        )
    
    # Crear filas de la tabla
    rows = []
    for _, row in df.iterrows():
        rows.append(Tr(
            Td(A(row['ID'], href=f"/modelo/{row['ID']}", cls="model-link")),
            Td(row['Descripción']),
            Td(f"{row['Accuracy']:.4f}"),
            Td(f"{row['F1-Score']:.4f}"),
            Td(f"{row['Precision']:.4f}"),
            Td(f"{row['Recall']:.4f}"),
            Td(f"{row.get('Tiempo (s)', 'N/A')}s" if 'Tiempo (s)' in row else "N/A"),
            Td(A("Ver detalles →", href=f"/modelo/{row['ID']}", cls="btn btn-small"))
        ))
    
    return Div(
        H1("🚢 Dashboard Titanic"),
        P("IA Conexionista - TP5 - Ranking de Modelos", cls="subtitle"),
        nav_bar("metrics"),
        Div(
            H2("📈 Comparativa de Modelos"),
            Table(
                Thead(Tr(
                    Th("ID"), Th("Descripción"), Th("Accuracy"), 
                    Th("F1-Score"), Th("Precision"), Th("Recall"),
                    Th("Tiempo"), Th("Acción")
                )),
                Tbody(*rows)
            ),
            cls="card"
        ),
        cls="container"
    )

@rt("/modelo/{model_id}")
def modelo_detalle(model_id: str):
    """Página de detalle de un modelo con curva ROC"""
    df = utils.cargar_resultados()
    
    if df is None:
        return Div(P("No se encontraron resultados."), cls="container")
    
    # Buscar el modelo
    modelo_data = df[df['ID'] == model_id]
    if modelo_data.empty:
        return Div(P(f"Modelo {model_id} no encontrado."), cls="container")
    
    modelo_info = modelo_data.iloc[0]
    
    # Intentar generar la curva ROC
    roc_html = Div()
    try:
        # Cargar datos para generar ROC
        df_raw = loader.cargar_y_limpiar_titanic()
        X_train, X_test, y_train, y_test = preprocessing.preparar_datos(df_raw)
        
        result = utils.generar_roc_base64(model_id, X_test, y_test)
        if result:
            img_base64, auc_score = result
            roc_html = Div(
                H2(f"📉 Curva ROC (AUC: {auc_score:.4f})"),
                Img(src=f"data:image/png;base64,{img_base64}", alt="Curva ROC"),
                cls="card roc-container"
            )
    except Exception as e:
        roc_html = Div(P(f"Error generando ROC: {str(e)}"), cls="card")
    
    return Div(
        A("← Volver al ranking", href="/", cls="back-link"),
        H1(f"🔬 {modelo_info['Descripción']}"),
        P(f"ID: {model_id}", cls="subtitle"),
        nav_bar(),
        
        Div(
            H2("📊 Métricas"),
            Div(
                Span("Accuracy: ", Span(f"{modelo_info['Accuracy']:.4f}", cls="metric-value"), cls="metric"),
                Span("F1-Score: ", Span(f"{modelo_info['F1-Score']:.4f}", cls="metric-value"), cls="metric"),
                Span("Precision: ", Span(f"{modelo_info['Precision']:.4f}", cls="metric-value"), cls="metric"),
                Span("Recall: ", Span(f"{modelo_info['Recall']:.4f}", cls="metric-value"), cls="metric"),
                Span("Tiempo: ", Span(f"{modelo_info.get('Tiempo (s)', 'N/A')}s", cls="metric-value"), cls="metric") if 'Tiempo (s)' in modelo_info else "",
            ),
            cls="card"
        ),
        
        crear_seccion_parametros(modelo_info),
        
        roc_html,
        
        cls="container"
    )

@rt("/predecir")
def predecir_form():
    """Formulario para probar predicciones"""
    modelos = utils.listar_modelos()
    
    return Div(
        H1("🔮 Predictor de Supervivencia"),
        P("Ingresa los datos del pasajero para predecir si sobrevive", cls="subtitle"),
        nav_bar("predict"),
        
        Div(
            H2("📝 Datos del Pasajero"),
            Form(
                Div(
                    Div(
                        Label("Modelo a usar:"),
                        Select(
                            *[Option(m, value=m) for m in modelos],
                            name="model_id",
                            id="model_id"
                        ),
                        cls="form-group"
                    ),
                    Div(
                        Label("Clase (1=1ra, 2=2da, 3=3ra):"),
                        Select(
                            Option("1ra Clase", value="1"),
                            Option("2da Clase", value="2"),
                            Option("3ra Clase", value="3", selected=True),
                            name="Pclass", id="Pclass"
                        ),
                        cls="form-group"
                    ),
                    Div(
                        Label("Sexo:"),
                        Select(
                            Option("Masculino", value="male"),
                            Option("Femenino", value="female"),
                            name="Sex", id="Sex"
                        ),
                        cls="form-group"
                    ),
                    Div(
                        Label("Edad:"),
                        Input(type="number", name="Age", id="Age", value="30", min="0", max="100"),
                        cls="form-group"
                    ),
                    cls="grid"
                ),
                Div(
                    Div(
                        Label("Hermanos/Cónyuge (SibSp):"),
                        Input(type="number", name="SibSp", id="SibSp", value="0", min="0", max="10"),
                        cls="form-group"
                    ),
                    Div(
                        Label("Padres/Hijos (Parch):"),
                        Input(type="number", name="Parch", id="Parch", value="0", min="0", max="10"),
                        cls="form-group"
                    ),
                    Div(
                        Label("Tarifa (Fare):"),
                        Input(type="number", name="Fare", id="Fare", value="30", min="0", step="0.01"),
                        cls="form-group"
                    ),
                    Div(
                        Label("Puerto de Embarque:"),
                        Select(
                            Option("Cherbourg (C)", value="C"),
                            Option("Queenstown (Q)", value="Q"),
                            Option("Southampton (S)", value="S", selected=True),
                            name="Embarked", id="Embarked"
                        ),
                        cls="form-group"
                    ),
                    cls="grid"
                ),
                Button("🚀 Predecir", type="submit", cls="btn"),
                action="/predecir/resultado",
                method="post"
            ),
            cls="card"
        ),
        
        cls="container"
    )

@rt("/predecir/resultado", methods=["POST"])
def predecir_resultado(model_id: str, Pclass: str, Sex: str, Age: str, SibSp: str, Parch: str, Fare: str, Embarked: str):
    """Muestra el resultado de la predicción"""
    datos = {
        'Pclass': Pclass,
        'Sex': Sex,
        'Age': Age,
        'SibSp': SibSp,
        'Parch': Parch,
        'Fare': Fare,
        'Embarked': Embarked
    }
    
    prediccion, probabilidad = utils.predecir(model_id, datos)
    
    if prediccion is None:
        return Div(
            A("← Volver", href="/predecir", cls="back-link"),
            H1("❌ Error"),
            P("No se pudo realizar la predicción. Asegúrate de haber entrenado los modelos primero."),
            cls="container"
        )
    
    sobrevive = prediccion == 1
    prob_sobrevivir = probabilidad[1] * 100
    prob_morir = probabilidad[0] * 100
    
    result_class = "result-survive" if sobrevive else "result-die"
    emoji = "✅ ¡SOBREVIVE!" if sobrevive else "❌ NO SOBREVIVE"
    
    return Div(
        A("← Nueva predicción", href="/predecir", cls="back-link"),
        H1("🔮 Resultado de Predicción"),
        P(f"Modelo: {model_id}", cls="subtitle"),
        nav_bar("predict"),
        
        Div(
            H2("📋 Datos Ingresados"),
            Div(
                Span(f"Clase: {Pclass}", cls="metric"),
                Span(f"Sexo: {Sex}", cls="metric"),
                Span(f"Edad: {Age}", cls="metric"),
                Span(f"SibSp: {SibSp}", cls="metric"),
                Span(f"Parch: {Parch}", cls="metric"),
                Span(f"Tarifa: ${Fare}", cls="metric"),
                Span(f"Embarque: {Embarked}", cls="metric"),
            ),
            cls="card"
        ),
        
        Div(
            H3(emoji),
            P(f"Probabilidad de sobrevivir: {prob_sobrevivir:.1f}%"),
            P(f"Probabilidad de no sobrevivir: {prob_morir:.1f}%"),
            cls=f"result-box {result_class}"
        ),
        
        cls="container"
    )

if __name__ == "__main__":
    print("🚢 Iniciando Dashboard Titanic...")
    print("📊 Abre tu navegador en: http://localhost:5001")
    serve(port=5001)
