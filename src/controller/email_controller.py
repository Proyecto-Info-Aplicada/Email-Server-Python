"""
Controlador REST para endpoints de email
"""
import logging
import asyncio
from datetime import datetime
from flask import Blueprint, request, jsonify, g
from src.services.send_email_service import SendEmailService
from src.services.request_logger import request_logger


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
    correlation_id = getattr(g, 'correlation_id', 'unknown')
    start_time = getattr(g, 'request_start_time', datetime.now())
    
    logger.info(f"[{correlation_id}] Recibido POST en /send-email-task")
    data = request.get_json()

    if not data:
        logger.warning(f"[{correlation_id}] No se envió JSON en el request")
        
        # Log a Kafka
        asyncio.run(request_logger.log_request(
            correlation_id=correlation_id,
            service="Email Server",
            endpoint=request.path,
            is_valid=False,
            reason="No se envió JSON",
            flow="Validación de entrada fallida",
            server_host=request.host,
            is_success=False
        ))
        
        return jsonify({"error": "No se envió JSON"}), 400

    try:
        service = SendEmailService()
        result = service.execute(data, correlation_id, start_time)
        logger.info(f"[{correlation_id}] Resultado del envío: {result}")
        
        if result.get("status") == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except ValueError as ve:
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        logger.error(f"[{correlation_id}] Error de validación: {str(ve)}")
        
        # Log a Kafka
        asyncio.run(request_logger.log_request(
            correlation_id=correlation_id,
            service="Email Server",
            endpoint=request.path,
            is_valid=False,
            reason=f"Error de validación: {str(ve)}",
            flow="Validación de entrada fallida",
            server_host=request.host,
            execution_time_ms=execution_time,
            is_success=False
        ))
        
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        logger.error(f"[{correlation_id}] Error en /send-email-task: {str(e)}")
        
        # Log a Kafka
        asyncio.run(request_logger.log_request(
            correlation_id=correlation_id,
            service="Email Server",
            endpoint=request.path,
            is_valid=True,
            reason=f"Error durante procesamiento: {str(e)}",
            flow=f"1. Validación de entrada exitosa\n2. Error durante el procesamiento\n3. Tipo de error: {type(e).__name__}",
            server_host=request.host,
            execution_time_ms=execution_time,
            is_success=False
        ))
        
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