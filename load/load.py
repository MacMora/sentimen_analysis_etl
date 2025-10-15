from sqlalchemy import create_engine, text
from config.settings import Settings
import os

class Load:
    def __init__(self, df):
        self.df = df
        self.config = Settings()

    def create_table(self):
        """Crear la tabla en la base de datos SQLite si no existe"""
        try:
            # Crear conexión usando SQLAlchemy
            engine = create_engine(self.config.DATABASE_URL)
            
            # Definir el esquema de la tabla para datos de sentimiento
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS sentiment_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                day_of_week TEXT,
                label INTEGER NOT NULL,
                sentiment TEXT,
                valid_titles INTEGER,
                avg_title_length REAL,
                financial_keywords INTEGER,
                positive_keywords INTEGER,
                negative_keywords INTEGER,
                top1 TEXT,
                top2 TEXT,
                top3 TEXT,
                top4 TEXT,
                top5 TEXT,
                top6 TEXT,
                top7 TEXT,
                top8 TEXT,
                top9 TEXT,
                top10 TEXT,
                top11 TEXT,
                top12 TEXT,
                top13 TEXT,
                top14 TEXT,
                top15 TEXT,
                top16 TEXT,
                top17 TEXT,
                top18 TEXT,
                top19 TEXT,
                top20 TEXT,
                top21 TEXT,
                top22 TEXT,
                top23 TEXT,
                top24 TEXT,
                top25 TEXT,
                all_titles TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            with engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
            
            print("✅ Tabla 'sentiment_analysis' creada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error al crear la tabla: {e}")
            return False

    def load_to_database(self):
        """Cargar datos transformados a la base de datos SQLite"""
        try:
            # Crear la tabla primero
            if not self.create_table():
                return False
            
            # Preparar los datos para la inserción
            df_to_load = self.df.copy()
            
            # Mapear nombres de columnas del DataFrame a los nombres de la tabla
            column_mapping = {
                'Date': 'date',
                'Year': 'year',
                'Month': 'month',
                'Day': 'day',
                'DayOfWeek': 'day_of_week',
                'Label': 'label',
                'Sentiment': 'sentiment',
                'ValidTitles': 'valid_titles',
                'AvgTitleLength': 'avg_title_length',
                'FinancialKeywords': 'financial_keywords',
                'PositiveKeywords': 'positive_keywords',
                'NegativeKeywords': 'negative_keywords',
                'Top1': 'top1',
                'Top2': 'top2',
                'Top3': 'top3',
                'Top4': 'top4',
                'Top5': 'top5',
                'Top6': 'top6',
                'Top7': 'top7',
                'Top8': 'top8',
                'Top9': 'top9',
                'Top10': 'top10',
                'Top11': 'top11',
                'Top12': 'top12',
                'Top13': 'top13',
                'Top14': 'top14',
                'Top15': 'top15',
                'Top16': 'top16',
                'Top17': 'top17',
                'Top18': 'top18',
                'Top19': 'top19',
                'Top20': 'top20',
                'Top21': 'top21',
                'Top22': 'top22',
                'Top23': 'top23',
                'Top24': 'top24',
                'Top25': 'top25',
                'AllTitles': 'all_titles'
            }
            
            # Renombrar columnas
            df_to_load = df_to_load.rename(columns=column_mapping)
            
            # Seleccionar solo las columnas que existen en el DataFrame
            available_columns = [col for col in column_mapping.values() if col in df_to_load.columns]
            df_to_load = df_to_load[available_columns]
            
            # Crear conexión usando SQLAlchemy
            engine = create_engine(self.config.DATABASE_URL)
            
            # Cargar datos a la base de datos
            df_to_load.to_sql(
                'sentiment_analysis',
                engine,
                if_exists='replace',  # Reemplazar datos existentes
                index=False,
                method='multi'  # Inserción más eficiente
            )
            
            print(f"✅ Datos cargados exitosamente a SQLite: {len(df_to_load)} registros insertados")
            return True
            
        except Exception as e:
            print(f"❌ Error al cargar datos a la base de datos: {e}")
            return False

    def save_clean_csv(self, output_path):
        """Guardar datos limpios en CSV"""
        try:
            # Crear directorio si no existe
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            self.df.to_csv(output_path, index=False)
            print(f"✅ CSV limpio guardado exitosamente en: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error al guardar el CSV limpio: {e}")
            return False

    def get_database_stats(self):
        """Obtener estadísticas de la base de datos"""
        try:
            engine = create_engine(self.config.DATABASE_URL)
            
            with engine.connect() as conn:
                # Contar registros totales
                result = conn.execute(text("SELECT COUNT(*) FROM sentiment_analysis"))
                total_records = result.scalar()
                
                # Obtener estadísticas por sentimiento
                sentiment_stats = conn.execute(text("""
                    SELECT sentiment, COUNT(*) as count 
                    FROM sentiment_analysis 
                    GROUP BY sentiment 
                    ORDER BY count DESC
                """)).fetchall()
                
                # Estadísticas por año
                yearly_stats = conn.execute(text("""
                    SELECT year, COUNT(*) as count 
                    FROM sentiment_analysis 
                    GROUP BY year 
                    ORDER BY year DESC 
                    LIMIT 5
                """)).fetchall()
                
                print(f"📊 Estadísticas de la base de datos:")
                print(f"   - Total de registros: {total_records}")
                print(f"   - Distribución por sentimiento:")
                for sentiment, count in sentiment_stats:
                    print(f"     • {sentiment}: {count} registros")
                print(f"   - Top 5 años con más datos:")
                for year, count in yearly_stats:
                    print(f"     • {year}: {count} registros")
                
                return True
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return False