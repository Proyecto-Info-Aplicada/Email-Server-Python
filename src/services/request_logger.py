"""
Logger de requests que envía logs estructurados a Kafka
"""
import logging
from datetime import datetime
from typing import Optional
from src.services.kafka_service import kafka_producer_service


class RequestLogger:
    """
    Servicio para registrar requests y enviarlos a Kafka con fallback a consola
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.log_topic = kafka_producer_service.request_log_topic
    
    async def log_request(
        self,
        correlation_id: str,
        service: str,
        endpoint: str,
        is_valid: bool,
        reason: str,
        flow: str,
        server_host: str = "localhost",
        execution_time_ms: Optional[float] = None,
        is_success: bool = True
    ):
        """
        Registra un request y lo envía a Kafka
        
        Args:
            correlation_id (str): ID de correlación del request
            service (str): Nombre del servicio
            endpoint (str): Endpoint invocado
            is_valid (bool): Si el request es válido
            reason (str): Razón del estado
            flow (str): Flujo de validación detallado
            server_host (str): Host del servidor
            execution_time_ms (float, optional): Tiempo de ejecución en ms
            is_success (bool): Si la operación fue exitosa
        """
        status = "VALIDA" if is_valid else "BLOQUEADA"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "correlationId": correlation_id,
            "service": service,
            "endpoint": endpoint,
            "status": status,
            "reason": reason,
            "validationFlow": flow,
            "serverHost": server_host,
            "executionTimeMs": execution_time_ms,
            "isSuccess": is_success
        }
        
        try:
            # Preparar headers
            headers = {
                "CorrelationId": correlation_id,
                "LogLevel": "Information" if is_valid else "Warning",
                "Source": "Email Server Python"
            }
            
            # Enviar a Kafka
            sent = kafka_producer_service.produce_request_log_async(log_entry, headers)
            
            if sent:
                self.logger.info(f"[{correlation_id}] Log enviado a Kafka exitosamente")
            else:
                # Fallback a consola si Kafka no está disponible
                self._log_to_console(log_entry, status, reason, flow)
                
        except Exception as error:
            self.logger.error(f"Error enviando a Kafka: {str(error)}")
            self._log_to_console(log_entry, status, reason, flow)
    
    def _log_to_console(self, log_entry: dict, status: str, reason: str, flow: str):
        """
        Fallback: imprime el log en consola si Kafka no está disponible
        
        Args:
            log_entry (dict): Entrada de log completa
            status (str): Estado del request
            reason (str): Razón del estado
            flow (str): Flujo de validación
        """
        self.logger.info(
            f"[{log_entry['timestamp']}] CorrelationId: {log_entry['correlationId']} | "
            f"Status: {status} | Motivo: {reason}"
        )
        self.logger.info("===== Flujo de validacion =====")
        self.logger.info(flow)
        self.logger.info("================================")


# Singleton del logger
request_logger = RequestLogger()
