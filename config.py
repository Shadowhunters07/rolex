import os

class Config:
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    ADMIN_ID = [7047543426]
    DB_URL = "mongodb+srv://navedmohammad2516:zu02cmOW6medghcJ@cluster0.cq1x5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DB_NAME = os.environ.get("DB_NAME")
    TXT_LOG = -1002322908140
    HOST = "https://www.masterapi.tech"
    
