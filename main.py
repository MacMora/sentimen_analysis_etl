from config.settings import Settings
from extract.extract import Extract
from transform.transform import Transform
from load.load import Load
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def create_graphs_directory():
    """Crear directorio para gráficas si no existe"""
    graph_dir = "graphs"
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
        print(f"📁 Directorio 'graphs' creado")
    return graph_dir

def generate_eda_graphs(df, graph_dir):
    """Generar 5 gráficas de análisis exploratorio de datos"""
    print("\n📊 GENERANDO GRÁFICAS DE ANÁLISIS EXPLORATORIO...")
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    
    graphs_created = []

    # Gráfica 1: Distribución de sentimientos por año
    if {'Year', 'Sentiment'}.issubset(df.columns):
        plt.figure(figsize=(14, 8))
        sentiment_year = df.groupby(['Year', 'Sentiment']).size().unstack(fill_value=0)
        sentiment_year.plot(kind='bar', stacked=True, color=['#ff6b6b', '#4ecdc4'])
        plt.title('Distribución de Sentimientos por Año', fontsize=16, fontweight='bold')
        plt.xlabel('Año', fontsize=12)
        plt.ylabel('Número de Registros', fontsize=12)
        plt.legend(title='Sentimiento', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot1_path = os.path.join(graph_dir, '01_distribucion_sentimientos_por_anio.png')
        plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
        plt.close()
        graphs_created.append(plot1_path)

    # Gráfica 2: Sentimientos por día de la semana
    if {'DayOfWeek', 'Sentiment'}.issubset(df.columns):
        plt.figure(figsize=(12, 8))
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_clean = df[df['DayOfWeek'].isin(day_order)]
        
        # Crear tabla de contingencia
        crosstab = pd.crosstab(df_clean['DayOfWeek'], df_clean['Sentiment'])
        crosstab = crosstab.reindex(day_order)
        
        # Gráfico de barras apiladas
        ax = crosstab.plot(kind='bar', stacked=True, color=['#ff6b6b', '#4ecdc4'])
        plt.title('Distribución de Sentimientos por Día de la Semana', fontsize=16, fontweight='bold')
        plt.xlabel('Día de la Semana', fontsize=12)
        plt.ylabel('Número de Registros', fontsize=12)
        plt.legend(title='Sentimiento', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot2_path = os.path.join(graph_dir, '02_sentimientos_por_dia_semana.png')
        plt.savefig(plot2_path, dpi=300, bbox_inches='tight')
        plt.close()
        graphs_created.append(plot2_path)

    # Gráfica 3: Evolución temporal del sentimiento
    if {'Date', 'Label'}.issubset(df.columns):
        plt.figure(figsize=(16, 8))
        df_temp = df.copy()
        df_temp['Date'] = pd.to_datetime(df_temp['Date'])
        df_temp = df_temp.sort_values('Date')
        
        # Calcular media móvil de 30 días
        df_temp['Sentiment_MA'] = df_temp['Label'].rolling(window=30, min_periods=1).mean()
        
        plt.subplot(2, 1, 1)
        plt.plot(df_temp['Date'], df_temp['Sentiment_MA'], linewidth=2, color='#2E86AB')
        plt.title('Evolución del Sentimiento (Media Móvil 30 días)', fontsize=14, fontweight='bold')
        plt.ylabel('Sentimiento Promedio', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Distribución mensual
        plt.subplot(2, 1, 2)
        monthly_sentiment = df_temp.groupby(df_temp['Date'].dt.to_period('M'))['Label'].mean()
        monthly_sentiment.plot(kind='line', marker='o', color='#A23B72')
        plt.title('Sentimiento Promedio por Mes', fontsize=14, fontweight='bold')
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Sentimiento Promedio', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plot3_path = os.path.join(graph_dir, '03_evolucion_temporal_sentimiento.png')
        plt.savefig(plot3_path, dpi=300, bbox_inches='tight')
        plt.close()
        graphs_created.append(plot3_path)

    # Gráfica 4: Análisis de palabras clave por sentimiento
    if {'Sentiment', 'FinancialKeywords', 'PositiveKeywords', 'NegativeKeywords'}.issubset(df.columns):
        plt.figure(figsize=(14, 10))
        
        # Preparar datos
        keywords_data = df.groupby('Sentiment')[['FinancialKeywords', 'PositiveKeywords', 'NegativeKeywords']].mean()
        
        # Gráfico de calor
        plt.subplot(2, 2, 1)
        sns.heatmap(keywords_data.T, annot=True, cmap='RdYlBu_r', fmt='.2f', cbar_kws={'label': 'Promedio de Palabras'})
        plt.title('Promedio de Palabras Clave por Sentimiento', fontsize=12, fontweight='bold')
        plt.xlabel('Sentimiento')
        plt.ylabel('Tipo de Palabras')
        
        # Distribución de palabras financieras
        plt.subplot(2, 2, 2)
        sns.boxplot(data=df, x='Sentiment', y='FinancialKeywords')
        plt.title('Distribución de Palabras Financieras', fontsize=12, fontweight='bold')
        plt.xlabel('Sentimiento')
        plt.ylabel('Número de Palabras Financieras')
        
        # Distribución de palabras positivas vs negativas
        plt.subplot(2, 2, 3)
        sentiment_keywords = df.groupby('Sentiment')[['PositiveKeywords', 'NegativeKeywords']].mean()
        sentiment_keywords.plot(kind='bar', color=['#4ecdc4', '#ff6b6b'])
        plt.title('Palabras Positivas vs Negativas por Sentimiento', fontsize=12, fontweight='bold')
        plt.xlabel('Sentimiento')
        plt.ylabel('Promedio de Palabras')
        plt.legend(['Positivas', 'Negativas'])
        plt.xticks(rotation=0)
        
        # Correlación entre tipos de palabras
        plt.subplot(2, 2, 4)
        correlation_data = df[['FinancialKeywords', 'PositiveKeywords', 'NegativeKeywords']].corr()
        sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title('Correlación entre Tipos de Palabras', fontsize=12, fontweight='bold')
        
        """
        plt.tight_layout()
        plot4_path = os.path.join(graph_dir, '04_analisis_palabras_clave.png')
        plt.savefig(plot4_path, dpi=300, bbox_inches='tight')
        plt.close()
        graphs_created.append(plot4_path)
        """

    # Gráfica 5: Análisis de longitud de títulos y cantidad de noticias
    if {'Sentiment', 'AvgTitleLength', 'ValidTitles'}.issubset(df.columns):
        plt.figure(figsize=(16, 8))
        
        # Longitud promedio de títulos por sentimiento
        plt.subplot(2, 2, 1)
        sns.boxplot(data=df, x='Sentiment', y='AvgTitleLength')
        plt.title('Distribución de Longitud Promedio de Títulos', fontsize=12, fontweight='bold')
        plt.xlabel('Sentimiento')
        plt.ylabel('Longitud Promedio de Títulos')
        
        # Cantidad de títulos válidos por sentimiento
        plt.subplot(2, 2, 2)
        sns.boxplot(data=df, x='Sentiment', y='ValidTitles')
        plt.title('Distribución de Títulos Válidos por Día', fontsize=12, fontweight='bold')
        plt.xlabel('Sentimiento')
        plt.ylabel('Número de Títulos Válidos')
        
        # Relación entre longitud y cantidad de títulos
        plt.subplot(2, 2, 3)
        sns.scatterplot(data=df, x='ValidTitles', y='AvgTitleLength', hue='Sentiment', alpha=0.6)
        plt.title('Relación entre Títulos Válidos y Longitud Promedio', fontsize=12, fontweight='bold')
        plt.xlabel('Número de Títulos Válidos')
        plt.ylabel('Longitud Promedio de Títulos')
        
        # Distribución temporal de títulos válidos
        plt.subplot(2, 2, 4)
        if 'Year' in df.columns:
            yearly_titles = df.groupby(['Year', 'Sentiment'])['ValidTitles'].mean().unstack(fill_value=0)
            yearly_titles.plot(kind='line', marker='o', color=['#ff6b6b', '#4ecdc4'])
            plt.title('Promedio de Títulos Válidos por Año', fontsize=12, fontweight='bold')
            plt.xlabel('Año')
            plt.ylabel('Promedio de Títulos Válidos')
            plt.legend(title='Sentimiento')
        
        plt.tight_layout()
        plot5_path = os.path.join(graph_dir, '05_analisis_titulos_noticias.png')
        plt.savefig(plot5_path, dpi=300, bbox_inches='tight')
        plt.close()
        graphs_created.append(plot5_path)

    return graphs_created

def main():
    print("🚀 === INICIANDO PROCESO ETL PARA ANÁLISIS DE SENTIMIENTO ===")
    
    # Configuración
    config = Settings()
    print(f"📁 Archivo de entrada: {config.INPUT_PATH}")
    print(f"📁 Archivo de salida: {config.OUTPUT_PATH}")
    print(f"🗄️ Base de datos: {config.DATABASE_URL}")
    
    # 1. EXTRACCIÓN
    print("\n🔍 --- FASE 1: EXTRACCIÓN ---")
    extractor = Extract(config.INPUT_PATH)
    df = extractor.extract()
    if df is None:
        print("❌ No se pudo extraer datos. Terminando proceso ETL.")
        return
    
    print(f"✅ Extracción exitosa: {len(df)} registros extraídos")

    # 2. TRANSFORMACIÓN
    print("\n🔄 --- FASE 2: TRANSFORMACIÓN ---")
    transformer = Transform(df)
    df_transformed = transformer.clean()
    
    if df_transformed is None or len(df_transformed) == 0:
        print("❌ Error en la transformación. Terminando proceso ETL.")
        return
    
    print(f"✅ Transformación exitosa: {len(df_transformed)} registros transformados")

    # 3. CARGA
    print("\n💾 --- FASE 3: CARGA ---")
    loader = Load(df_transformed)
    
    # Guardar CSV limpio
    if not loader.save_clean_csv(config.OUTPUT_PATH):
        print("❌ Error al guardar CSV limpio. Terminando proceso ETL.")
        return
    
    # Cargar a base de datos SQLite
    if not loader.load_to_database():
        print("❌ Error al cargar datos a la base de datos. Terminando proceso ETL.")
        return
    
    # Mostrar estadísticas de la base de datos
    loader.get_database_stats()

    # 4. GENERACIÓN DE GRÁFICAS
    print("\n📊 --- FASE 4: ANÁLISIS EXPLORATORIO ---")
    graph_dir = create_graphs_directory()
    
    # Leer datos limpios para gráficas
    try:
        df_plot = pd.read_csv(config.OUTPUT_PATH)
        df_plot['Date'] = pd.to_datetime(df_plot['Date'])
    except Exception as e:
        print(f"❌ Error al leer datos para gráficas: {e}")
        return
    
    # Generar gráficas EDA
    graphs_created = generate_eda_graphs(df_plot, graph_dir)
    
    if graphs_created:
        print("✅ Gráficas EDA generadas exitosamente:")
        for i, graph_path in enumerate(graphs_created, 1):
            print(f"   {i}. {graph_path}")
    else:
        print("⚠️ No se generaron gráficas; faltan columnas necesarias en el dataset.")

    print("\n🎉 === PROCESO ETL COMPLETADO EXITOSAMENTE ===")
    print("📋 Resumen del proceso:")
    print(f"   • Datos extraídos: {len(df)} registros")
    print(f"   • Datos transformados: {len(df_transformed)} registros")
    print(f"   • CSV limpio guardado en: {config.OUTPUT_PATH}")
    print(f"   • Base de datos SQLite: {config.DATABASE_URL}")
    print(f"   • Gráficas EDA: {len(graphs_created)} gráficas en carpeta 'graphs/'")
    print("\n✨ El proyecto está listo para análisis de sentimiento financiero!")

if __name__ == "__main__":
    main()