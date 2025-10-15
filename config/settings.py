import os

class Settings:
    # Configuración de archivos (valores por defecto)
    INPUT_PATH = 'extract/files/stock_senti_analysis.csv'
    OUTPUT_PATH = 'output/cleaned_sentiment_data.csv'
    
    # Configuración de base de datos SQLite local
    DB_NAME = 'sentiment_analysis.db'
    
    # URL de conexión a SQLite
    @property
    def DATABASE_URL(self):
        return f"sqlite:///{self.DB_NAME}"