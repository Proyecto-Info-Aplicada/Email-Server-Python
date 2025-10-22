from flask import Flask
from logging_config import setup_logging
from Presentation.controller import email_blueprint
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)


app.register_blueprint(email_blueprint)

@app.route("/")
def home():
    return {"message": "Email Server corriendo correctamente ✅"}

if __name__ == "__main__":
    logger.info("Iniciando Email Server en http://127.0.0.1:5001")
    app.run(host="0.0.0.0", port=5001, debug=True)
