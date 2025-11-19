"""
Middleware para manejar Correlation IDs en requests Flask
"""
import uuid
import logging
from flask import request, g
from datetime import datetime

logger = logging.getLogger(__name__)


def correlation_id_middleware():
    """
    Middleware que genera o extrae el Correlation ID de los headers
    y lo almacena en el contexto de Flask (g)
    """
    # Intentar obtener el Correlation ID de los headers
    correlation_id = (
        request.headers.get('X-Correlation-ID') or
        request.headers.get('Correlation-ID') or
        str(uuid.uuid4())
    )
    
    # Determinar el origen del Correlation ID
    origin = (
        'Recibido desde cliente' 
        if request.headers.get('X-Correlation-ID') or request.headers.get('Correlation-ID')
        else 'Generado por servidor'
    )
    
    # Almacenar en el contexto de Flask
    g.correlation_id = correlation_id
    g.request_start_time = datetime.now()
    
    # Log del request entrante
    logger.info(
        f"{request.method} {request.path} | "
        f"Origen del Correlation ID: {origin} | "
        f"Timestamp: {datetime.now().isoformat()} | "
        f"Servicio: email-server | "
        f"Servidor: {request.host} | "
        f"CorrelationId: {correlation_id}"
    )


def add_correlation_headers(response):
    """
    Middleware para agregar el Correlation ID a los headers de respuesta
    
    Args:
        response: Objeto de respuesta de Flask
        
    Returns:
        response: Respuesta modificada con headers
    """
    if hasattr(g, 'correlation_id'):
        response.headers['X-Correlation-ID'] = g.correlation_id
    return response
