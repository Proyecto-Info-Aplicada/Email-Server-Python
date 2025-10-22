"""
Configuración general del proyecto
"""
import os

# Configuración del Storage Server
STORAGE_URL = os.getenv("STORAGE_URL", "http://127.0.0.1:5000/pdf-storage")
TIMEOUT_SECONDS = 10

# Configuración de Gmail API
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# Configuración del servidor
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
DEBUG_MODE = True
