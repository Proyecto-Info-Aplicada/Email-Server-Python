"""
Punto de entrada principal del Email Server
"""
from flask import Flask
from src.config.logging_config import setup_logging
from src.config.settings import SERVER_HOST, SERVER_PORT, DEBUG_MODE
from src.controller.email_controller import email_blueprint
import logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(email_blueprint)


@app.route("/")
def home():
    """
    Endpoint raíz para verificar que el servidor está funcionando
    """
    return {"message": "Email Server corriendo correctamente ✅"}


if __name__ == "__main__":
    logger.info(f"Iniciando Email Server en http://127.0.0.1:{SERVER_PORT}")
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)
