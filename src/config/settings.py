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

# Configuración de Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(',')
KAFKA_CLIENT_ID = os.getenv("KAFKA_CLIENT_ID", "email-server-python")
KAFKA_REQUEST_TOPIC = os.getenv("KAFKA_REQUEST_TOPIC", "email-server-requests")
KAFKA_REQUEST_TIMEOUT = int(os.getenv("KAFKA_REQUEST_TIMEOUT", "30000"))
KAFKA_CONNECTION_TIMEOUT = int(os.getenv("KAFKA_CONNECTION_TIMEOUT", "3000"))
KAFKA_ENABLED = os.getenv("KAFKA_ENABLED", "true").lower() == "true"
