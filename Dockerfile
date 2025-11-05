# Imagen base ligera de Python
FROM python:3.11-slim

# Evitar prompts interactivos en apt
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias para matplotlib/seaborn
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       g++ \
       libfreetype6-dev \
       libpng-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cache
COPY requirements.txt ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Establecer variable para evitar problemas de permisos de matplotlib
ENV MPLCONFIGDIR=/tmp/matplotlib
RUN mkdir -p /tmp/matplotlib

# Crear directorios que se usarán como volúmenes (se sobrescribirán si se montan)
RUN mkdir -p /app/graphs /app/output

# Comando por defecto: ejecutar el ETL
CMD ["python", "main.py"]

