"""
Configuración de logging para el proyecto
"""
import logging
import os

def setup_logging():
    """
    Configura el sistema de logging para el Email Server
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "email-server.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logging.info("Logging configurado para Email Server")
