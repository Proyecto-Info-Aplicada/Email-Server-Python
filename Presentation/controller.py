from flask import Blueprint, request, jsonify
from Application.Services.send_email_service import SendEmailService
import logging

email_blueprint = Blueprint('email_blueprint', __name__)
logger = logging.getLogger(__name__)

@email_blueprint.route('/send-email-task', methods=['POST'])
def send_email_task():
    print("Recibido POST en /send-email-task") 
    data = request.get_json()

    if not data:
        print("No se envió JSON")
        return jsonify({"error": "No se envió JSON"}), 400

    try:
        service = SendEmailService()
        result = service.execute(data)
        print("Resultado del envío:", result)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error en /send-email-task: {str(e)}")
        return jsonify({"error": str(e)}), 500
