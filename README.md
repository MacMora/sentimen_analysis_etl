# 📊 Sistema ETL para Análisis de Sentimiento Financiero

Este proyecto implementa un sistema ETL (Extract, Transform, Load) completo para el análisis de sentimiento en noticias financieras, utilizando técnicas de procesamiento de datos y visualización para extraer insights valiosos del mercado financiero.

## 🎯 Descripción del Proyecto

El sistema procesa un dataset de análisis de sentimiento que contiene:
- **Fechas**: Información temporal de las noticias (2000-2019)
- **Etiquetas de Sentimiento**: Clasificación binaria (0=Negativo, 1=Positivo)
- **Títulos de Noticias**: Los 25 títulos más importantes de cada día
- **Métricas Derivadas**: Análisis de palabras clave, longitud de títulos, etc.

### 🏗️ Arquitectura del Sistema

```
sentiment_db/
├── config/           # Configuración del proyecto
│   ├── __init__.py
│   └── settings.py   # Configuración de rutas y base de datos
├── extract/          # Módulo de extracción
│   ├── __init__.py
│   ├── extract.py    # Extracción de datos del CSV
│   └── files/        # Archivos de datos
│       └── stock_senti_analysis.csv
├── transform/        # Módulo de transformación
│   ├── __init__.py
│   └── transform.py  # Limpieza y transformación de datos
├── load/            # Módulo de carga
│   ├── __init__.py
│   └── load.py      # Carga a SQLite y generación de CSV
├── graphs/          # Gráficas generadas (creada automáticamente)
├── output/          # Datos procesados (creada automáticamente)
├── main.py          # Script principal del ETL
├── config.env       # Variables de entorno
└── README.md        # Este archivo
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd sentiment_db
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias principales incluyen:
- `pandas`: Manipulación de datos
- `numpy`: Operaciones numéricas
- `sqlalchemy`: ORM para bases de datos
- `seaborn`: Visualización de datos
- `matplotlib`: Gráficos
- `python-dotenv`: Manejo de variables de entorno

### 4. Configuración

El archivo `config.env` contiene las configuraciones del proyecto:

```env
# Configuración de archivos
INPUT_PATH=extract/files/stock_senti_analysis.csv
OUTPUT_PATH=output/cleaned_sentiment_data.csv

# Configuración de base de datos SQLite local
DB_NAME=sentiment_analysis.db
```

## 🏃‍♂️ Uso del Sistema

### Ejecución Completa del ETL

```bash
python main.py
```

Este comando ejecuta todo el proceso ETL:

1. **🔍 Extracción**: Lee el dataset desde `extract/files/stock_senti_analysis.csv`
2. **🔄 Transformación**: Limpia y transforma los datos
3. **💾 Carga**: Guarda en CSV limpio y carga a SQLite
4. **📊 Visualización**: Genera 5 gráficas de análisis exploratorio

### Salidas del Sistema

#### 1. Datos Procesados
- **CSV Limpio**: `output/cleaned_sentiment_data.csv`
- **Base de Datos SQLite**: `sentiment_analysis.db`

#### 2. Gráficas EDA (Análisis Exploratorio)
Todas las gráficas se guardan en la carpeta `graphs/`:

1. **📈 Distribución de Sentimientos por Año**
   - Muestra la evolución de sentimientos positivos vs negativos a lo largo de los años
   - Archivo: `01_distribucion_sentimientos_por_anio.png`

2. **📅 Sentimientos por Día de la Semana**
   - Analiza patrones de sentimiento según el día de la semana
   - Archivo: `02_sentimientos_por_dia_semana.png`

3. **📊 Evolución Temporal del Sentimiento**
   - Media móvil de 30 días y tendencias mensuales
   - Archivo: `03_evolucion_temporal_sentimiento.png`

4. **🔍 Análisis de Palabras Clave**
   - Correlación entre palabras financieras, positivas y negativas
   - Archivo: `04_analisis_palabras_clave.png`

5. **📰 Análisis de Títulos de Noticias**
   - Longitud de títulos y cantidad de noticias por sentimiento
   - Archivo: `05_analisis_titulos_noticias.png`

## 🔧 Funcionalidades del Sistema

### Módulo de Extracción (`extract/extract.py`)

- ✅ Validación de existencia de archivos
- ✅ Lectura optimizada de CSV
- ✅ Información detallada del dataset
- ✅ Estadísticas básicas de sentimientos

### Módulo de Transformación (`transform/transform.py`)

- 🧹 **Limpieza de Fechas**: Conversión y extracción de componentes temporales
- 🎭 **Procesamiento de Sentimientos**: Normalización de etiquetas binarias
- 📰 **Limpieza de Títulos**: Eliminación de caracteres especiales y normalización
- 🔍 **Análisis de Palabras Clave**: Detección automática de términos financieros, positivos y negativos
- 📊 **Métricas Derivadas**: Longitud promedio de títulos, conteo de títulos válidos
- 🗑️ **Eliminación de Duplicados**: Detección y eliminación de registros duplicados
- ❌ **Manejo de Nulos**: Limpieza de datos faltantes

### Módulo de Carga (`load/load.py`)

- 💾 **Base de Datos SQLite**: Creación automática de esquema y carga de datos
- 📄 **CSV Limpio**: Exportación de datos procesados
- 📊 **Estadísticas**: Generación de métricas de la base de datos

## 📊 Estructura de la Base de Datos

La tabla `sentiment_analysis` contiene:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | Clave primaria |
| `date` | DATE | Fecha de las noticias |
| `year`, `month`, `day` | INTEGER | Componentes de fecha |
| `day_of_week` | TEXT | Día de la semana |
| `label` | INTEGER | Etiqueta de sentimiento (0/1) |
| `sentiment` | TEXT | Sentimiento textual (Positivo/Negativo) |
| `valid_titles` | INTEGER | Número de títulos válidos |
| `avg_title_length` | REAL | Longitud promedio de títulos |
| `financial_keywords` | INTEGER | Conteo de palabras financieras |
| `positive_keywords` | INTEGER | Conteo de palabras positivas |
| `negative_keywords` | INTEGER | Conteo de palabras negativas |
| `top1` - `top25` | TEXT | Títulos de noticias (Top 25) |
| `all_titles` | TEXT | Texto combinado de todos los títulos |
| `created_at` | TIMESTAMP | Fecha de creación del registro |

## 🎨 Características de las Visualizaciones

### Paleta de Colores
- 🔴 **Negativo**: `#ff6b6b` (Rojo coral)
- 🔵 **Positivo**: `#4ecdc4` (Turquesa)
- 🟦 **Evolución**: `#2E86AB` (Azul)
- 🟣 **Tendencias**: `#A23B72` (Púrpura)

### Calidad de Gráficas
- **Resolución**: 300 DPI para impresión de alta calidad
- **Formato**: PNG optimizado para web y documentos
- **Estilo**: Seaborn whitegrid para máxima legibilidad

## 🔍 Análisis de Datos Incluidos

### 1. Análisis Temporal
- Evolución del sentimiento a lo largo del tiempo
- Patrones estacionales y tendencias anuales
- Análisis de días de la semana

### 2. Análisis de Contenido
- Detección automática de palabras clave financieras
- Correlación entre sentimiento y contenido
- Análisis de longitud y complejidad de títulos

### 3. Métricas de Calidad
- Conteo de títulos válidos por día
- Estadísticas de completitud de datos
- Identificación de patrones de calidad

## 🛠️ Desarrollo y Extensión

### Estructura Modular

El sistema está diseñado con una arquitectura modular que permite:

- **Fácil extensión**: Agregar nuevos módulos de transformación
- **Configuración flexible**: Modificar rutas y parámetros via `config.env`
- **Mantenimiento**: Cada módulo es independiente y testeable

### Agregar Nuevas Transformaciones

Para agregar nuevas transformaciones, modifica `transform/transform.py`:

```python
def clean(self):
    # ... transformaciones existentes ...
    
    # Nueva transformación
    df['nueva_metrica'] = df['campo_existente'].apply(transformacion_personalizada)
    
    return df
```

### Agregar Nuevas Visualizaciones

Para agregar gráficas, modifica la función `generate_eda_graphs()` en `main.py`:

```python
# Nueva gráfica
if {'Campo1', 'Campo2'}.issubset(df.columns):
    plt.figure(figsize=(12, 8))
    # Tu código de visualización aquí
    plt.savefig(os.path.join(graph_dir, '06_nueva_grafica.png'))
    plt.close()
    graphs_created.append(plot_path)
```

## 📈 Casos de Uso

### 1. Análisis de Mercado
- Identificar períodos de optimismo/pesimismo en el mercado
- Correlacionar sentimiento con eventos financieros
- Predecir tendencias basadas en análisis histórico

### 2. Investigación Académica
- Estudios de comportamiento del mercado
- Análisis de impacto de noticias en sentimiento
- Investigación en procesamiento de lenguaje natural

### 3. Trading Algorítmico
- Desarrollo de estrategias basadas en sentimiento
- Análisis de correlación precio-sentimiento
- Sistemas de alerta temprana

## 🚨 Solución de Problemas

### Errores Comunes

1. **Error de importación de módulos**
   ```bash
   # Asegúrate de estar en el directorio correcto
   cd sentiment_db
   # Y que el entorno virtual esté activado
   source venv/bin/activate
   ```

2. **Archivo CSV no encontrado**
   ```bash
   # Verifica que el archivo existe en la ruta especificada
   ls extract/files/stock_senti_analysis.csv
   ```

3. **Error de permisos en base de datos**
   ```bash
   # Asegúrate de tener permisos de escritura en el directorio
   chmod 755 .
   ```

### Logs y Debugging

El sistema incluye logging detallado:
- ✅ Mensajes de éxito con emojis
- ❌ Mensajes de error claros
- 📊 Estadísticas de procesamiento
- 🔍 Información de debugging

## 🤝 Contribución

### Cómo Contribuir

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con tests
4. Crear Pull Request con descripción detallada

### Estándares de Código

- **PEP 8**: Seguir convenciones de Python
- **Docstrings**: Documentar todas las funciones
- **Type Hints**: Usar anotaciones de tipo
- **Logging**: Incluir mensajes informativos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- **Desarrollador Principal**: [Tu Nombre]
- **Instituciones**: [Universidad/Organización]
- **Fecha**: 2024

## 📞 Contacto y Soporte

- **Email**: [tu-email@ejemplo.com]
- **GitHub Issues**: Para reportar bugs o solicitar funcionalidades
- **Documentación**: Este README y comentarios en el código

---

## 🎯 Próximas Mejoras

- [ ] **API REST**: Endpoint para consultas dinámicas
- [ ] **Dashboard Web**: Interfaz gráfica interactiva
- [ ] **Machine Learning**: Modelos predictivos de sentimiento
- [ ] **Integración en Tiempo Real**: Procesamiento de datos streaming
- [ ] **Análisis de Redes**: Análisis de co-ocurrencia de términos
- [ ] **Exportación Avanzada**: Formatos JSON, Parquet, etc.

---

*Este proyecto fue desarrollado como parte de un sistema ETL avanzado para análisis de sentimiento financiero. ¡Esperamos que sea útil para tu investigación o aplicación!* 🚀
