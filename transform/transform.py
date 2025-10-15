
import pandas as pd
import numpy as np
import re

class Transform:
    def __init__(self, df):
        self.df = df

    def clean(self):
        df = self.df.copy()
        print("🧹 Iniciando transformación de datos de análisis de sentimiento...")

        initial_count = len(df)
        
        # 1. Limpieza de fechas
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
            df['Day'] = df['Date'].dt.day
            df['DayOfWeek'] = df['Date'].dt.day_name()
            print(f"📅 Fechas procesadas: {df['Date'].min()} a {df['Date'].max()}")

        # 2. Limpieza de etiquetas de sentimiento
        if 'Label' in df.columns:
            # Asegurar que Label sea binario (0 o 1)
            df['Label'] = pd.to_numeric(df['Label'], errors='coerce')
            df['Label'] = df['Label'].astype('Int64')
            
            # Crear columna de sentimiento textual
            df['Sentiment'] = df['Label'].map({0: 'Negativo', 1: 'Positivo'})
            print(f"🎭 Sentimientos procesados: {df['Sentiment'].value_counts().to_dict()}")

        # 3. Limpieza de títulos de noticias (Top1-Top25)
        news_columns = [col for col in df.columns if col.startswith('Top')]
        print(f"📰 Procesando {len(news_columns)} columnas de noticias...")
        
        for col in news_columns:
            if col in df.columns:
                # Limpiar espacios y caracteres especiales
                df[col] = df[col].astype(str).str.strip()
                # Reemplazar valores vacíos o 'nan' con None
                df[col] = df[col].replace(['', 'nan', 'NaN'], np.nan)
                
                # Limpiar caracteres especiales pero mantener contenido
                df[col] = df[col].str.replace(r'[^\w\s\.,;:!?\'"()-]', ' ', regex=True)
                df[col] = df[col].str.replace(r'\s+', ' ', regex=True)  # Múltiples espacios a uno
                df[col] = df[col].str.strip()

        # 4. Crear columnas derivadas útiles para análisis
        # Contar títulos válidos por día
        df['ValidTitles'] = df[news_columns].notna().sum(axis=1)
        
        # Crear texto combinado de todos los títulos
        df['AllTitles'] = df[news_columns].apply(
            lambda row: ' '.join([str(val) for val in row if pd.notna(val)]), axis=1
        )
        
        # Longitud promedio de títulos
        df['AvgTitleLength'] = df[news_columns].apply(
            lambda row: np.mean([len(str(val)) for val in row if pd.notna(val)]), axis=1
        )

        # 5. Detectar y eliminar duplicados
        initial_count = len(df)
        df = df.drop_duplicates(subset=['Date', 'Label'])
        duplicates_removed = initial_count - len(df)
        if duplicates_removed > 0:
            print(f"🔄 Duplicados eliminados: {duplicates_removed}")

        # 6. Eliminar filas con datos críticos faltantes
        initial_count = len(df)
        df = df.dropna(subset=['Date', 'Label'])
        missing_data_removed = initial_count - len(df)
        if missing_data_removed > 0:
            print(f"❌ Filas eliminadas por datos faltantes: {missing_data_removed}")

        # 7. Análisis de palabras clave en títulos (para análisis adicional)
        # Palabras relacionadas con mercados financieros
        financial_keywords = ['stock', 'market', 'trading', 'price', 'earnings', 'revenue', 
                            'profit', 'loss', 'investor', 'investment', 'bank', 'economy']
        
        # Palabras relacionadas con sentimientos positivos
        positive_keywords = ['rise', 'gain', 'up', 'increase', 'growth', 'profit', 'success', 
                           'boost', 'surge', 'rally', 'positive', 'strong', 'better']
        
        # Palabras relacionadas con sentimientos negativos  
        negative_keywords = ['fall', 'drop', 'down', 'decrease', 'loss', 'decline', 'crisis',
                           'crash', 'plunge', 'negative', 'weak', 'worse', 'trouble']

        for keyword_list, col_name in [(financial_keywords, 'FinancialKeywords'), 
                                      (positive_keywords, 'PositiveKeywords'),
                                      (negative_keywords, 'NegativeKeywords')]:
            df[col_name] = df['AllTitles'].str.lower().str.count(
                '|'.join(keyword_list)
            )

        # 8. Reordenar columnas para mejor organización
        preferred_order = [
            'Date', 'Year', 'Month', 'Day', 'DayOfWeek', 'Label', 'Sentiment',
            'ValidTitles', 'AvgTitleLength', 'FinancialKeywords', 'PositiveKeywords', 'NegativeKeywords'
        ] + news_columns + ['AllTitles']
        
        # Mantener solo las columnas que existen
        ordered_cols = [c for c in preferred_order if c in df.columns]
        other_cols = [c for c in df.columns if c not in ordered_cols]
        df = df[ordered_cols + other_cols]

        # 9. Resetear índice
        df = df.reset_index(drop=True)
        
        print(f"✅ Transformación completada. Registros finales: {len(df)}")
        print(f"📊 Estadísticas finales:")
        print(f"   - Rango de fechas: {df['Date'].min()} a {df['Date'].max()}")
        print(f"   - Sentimientos: {df['Sentiment'].value_counts().to_dict()}")
        print(f"   - Títulos válidos promedio por día: {df['ValidTitles'].mean():.1f}")
        
        self.df = df
        return self.df
