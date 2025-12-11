# Titanic ML Dashboard - Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/data/raw /app/data/processed /app/models/trained /app/models/artifacts /app/reports

# Exponer puerto
EXPOSE 5001

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Comando por defecto: entrenar y luego ejecutar dashboard
CMD ["sh", "-c", "python train.py && python run_dashboard.py"]
