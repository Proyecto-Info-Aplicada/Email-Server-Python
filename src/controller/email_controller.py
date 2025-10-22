"""
Controlador REST para endpoints de email
"""
import logging
from flask import Blueprint, request, jsonify
from src.services.send_email_service import SendEmailService


# Blueprint de Flask para rutas de email
email_blueprint = Blueprint('email_blueprint', __name__)
logger = logging.getLogger(__name__)


@email_blueprint.route('/send-email-task', methods=['POST'])
def send_email_task():
    """
    Endpoint POST para enviar email con PDF adjunto
    
    Request JSON:
        {
            "CorrelationId": "string",
            "EmailAddress": "string",
            "Subject": "string" (opcional),
            "MessageBody": "string" (opcional),
            "PdfFileName": "string" (opcional)
        }
    
    Returns:
        JSON con status y message
    """
    logger.info("Recibido POST en /send-email-task")
    data = request.get_json()

    if not data:
        logger.warning("No se envió JSON en el request")
        return jsonify({"error": "No se envió JSON"}), 400

    try:
        service = SendEmailService()
        result = service.execute(data)
        logger.info(f"Resultado del envío: {result}")
        
        if result.get("status") == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except ValueError as ve:
        logger.error(f"Error de validación: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error en /send-email-task: {str(e)}")
        return jsonify({"error": str(e)}), 500


@email_blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar el estado del servicio
    
    Returns:
        JSON con status del servicio
    """
    return jsonify({
        "status": "healthy",
        "service": "email-server"
    }), 200
