import pandas as pd
import os

class Extract:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def extract(self):
        try:
            # Verificar si el archivo existe
            if not os.path.exists(self.csv_path):
                print(f"❌ Error: El archivo {self.csv_path} no existe")
                return None
            
            # Intentar diferentes codificaciones para leer el CSV
            encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16']
            df = None
            
            for encoding in encodings_to_try:
                try:
                    print(f"🔍 Intentando codificación: {encoding}")
                    df = pd.read_csv(self.csv_path, encoding=encoding)
                    print(f"✅ Archivo leído exitosamente con codificación: {encoding}")
                    break
                except UnicodeDecodeError:
                    print(f"⚠️ Falló con codificación: {encoding}")
                    continue
                except Exception as e:
                    print(f"⚠️ Error con codificación {encoding}: {e}")
                    continue
            
            if df is None:
                print("❌ No se pudo leer el archivo con ninguna codificación disponible")
                return None
            
            print(f"✅ Datos extraídos exitosamente: {len(df)} registros encontrados")
            print(f"📊 Columnas disponibles: {list(df.columns)}")
            print(f"📅 Rango de fechas: {df['Date'].min()} a {df['Date'].max()}")
            print(f"🎭 Distribución de sentimientos:")
            if 'Label' in df.columns:
                sentiment_counts = df['Label'].value_counts()
                print(f"   - Negativo (0): {sentiment_counts.get(0, 0)} registros")
                print(f"   - Positivo (1): {sentiment_counts.get(1, 0)} registros")
            
            return df
        except Exception as e:
            print(f"❌ Error inesperado al leer el archivo CSV: {e}")
            return None

