"""
Punto de entrada principal del Email Server
"""
import asyncio
import logging
import atexit
from flask import Flask
from src.config.logging_config import setup_logging
from src.config.settings import SERVER_HOST, SERVER_PORT, DEBUG_MODE
from src.controller.email_controller import email_blueprint
from src.middleware.correlation_middleware import correlation_id_middleware, add_correlation_headers
from src.services.kafka_service import kafka_producer_service

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)

# Registrar middleware
app.before_request(correlation_id_middleware)
app.after_request(add_correlation_headers)

# Registrar blueprints
app.register_blueprint(email_blueprint)


@app.route("/")
def home():
    """
    Endpoint raíz para verificar que el servidor está funcionando
    """
    return {"message": "Email Server corriendo correctamente ✅"}


def initialize_kafka():
    """
    Inicializa la conexión con Kafka al arrancar el servidor
    """
    try:
        logger.info("Inicializando conexión con Kafka...")
        asyncio.run(kafka_producer_service.initialize())
    except Exception as e:
        logger.warning(f"No se pudo inicializar Kafka: {str(e)}")


def shutdown_kafka():
    """
    Cierra la conexión con Kafka al apagar el servidor
    """
    logger.info("Cerrando conexión con Kafka...")
    kafka_producer_service.disconnect()


# Registrar shutdown handler
atexit.register(shutdown_kafka)


if __name__ == "__main__":
    # Inicializar Kafka antes de iniciar el servidor
    initialize_kafka()
    
    logger.info(f"Iniciando Email Server en http://127.0.0.1:{SERVER_PORT}")
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)
