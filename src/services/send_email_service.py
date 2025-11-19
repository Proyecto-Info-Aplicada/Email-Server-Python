"""
Servicio principal para envío de emails con PDFs adjuntos
"""
import logging
import asyncio
from datetime import datetime
from typing import Optional
from src.dto.email_dto import EmailRequest
from src.services.gmail_service import GmailService
from src.services.storage_service import StorageService
from src.services.request_logger import request_logger

class SendEmailService:
    """
    Servicio de aplicación para enviar emails con PDFs desde Storage
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gmail_service = GmailService()
        self.storage_service = StorageService()

    def execute(
        self, 
        data: dict, 
        correlation_id: Optional[str] = None,
        start_time: Optional[datetime] = None
    ) -> dict:
        """
        Ejecuta el proceso de envío de email con PDF adjunto
        
        Args:
            data (dict): Diccionario con los datos del request
            correlation_id (str, optional): ID de correlación del request
            start_time (datetime, optional): Timestamp de inicio del request
            
        Returns:
            dict: Resultado del proceso con status y message
            
        Raises:
            ValueError: Si faltan campos obligatorios
        """
        if start_time is None:
            start_time = datetime.now()
            
        self.logger.info(f"[{correlation_id}] Iniciando envío de correo con PDF adjunto...")

        # Crear y validar DTO
        email_request = EmailRequest.from_dict(data)
        email_request.validate()
        
        if correlation_id:
            email_request.correlation_id = correlation_id
        
        # Determinar nombre del archivo
        filename = email_request.pdf_filename or f"{email_request.correlation_id}.pdf"
        
        flow_steps = []
        flow_steps.append("1. Validación de entrada exitosa")
        
        try:
            self.logger.info(f"[{email_request.correlation_id}] Obteniendo PDF desde Storage Server")
            
            # Obtener PDF desde Storage Server
            pdf_data = self.storage_service.get_pdf_by_correlation(email_request.correlation_id)
            self.logger.info(f"[{email_request.correlation_id}] PDF obtenido correctamente ({len(pdf_data)} bytes)")
            flow_steps.append(f"2. PDF obtenido del storage ({len(pdf_data)} bytes)")

            # Enviar correo con el PDF adjunto
            self.logger.info(f"[{email_request.correlation_id}] Enviando correo a {email_request.email_address} con archivo {filename}")
            email_result = self.gmail_service.send_email_with_attachment(
                to_email=email_request.email_address,
                subject=email_request.subject,
                body=email_request.message_body,
                pdf_data=pdf_data,
                filename=filename
            )

            # Calcular tiempo de ejecución
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            if email_result["success"]:
                self.logger.info(f"[{email_request.correlation_id}] Correo enviado correctamente a {email_request.email_address}")
                flow_steps.append(f"3. Email enviado exitosamente a {email_request.email_address}")
                flow_steps.append(f"4. Tiempo total: {execution_time:.2f}ms")
                
                # Log a Kafka
                asyncio.run(request_logger.log_request(
                    correlation_id=email_request.correlation_id,
                    service="Email Server",
                    endpoint="/send-email-task",
                    is_valid=True,
                    reason="Request procesado exitosamente",
                    flow="\n".join(flow_steps),
                    execution_time_ms=execution_time,
                    is_success=True
                ))
                
                return {
                    "status": "success",
                    "message": f"Correo enviado correctamente a {email_request.email_address}",
                    "pdfFileSize": f"{len(pdf_data)} bytes",
                    "executionTimeMs": round(execution_time, 2)
                }
            else:
                self.logger.error(f"[{email_request.correlation_id}] Error al enviar correo: {email_result.get('error')}")
                flow_steps.append(f"3. Error al enviar email: {email_result.get('error')}")
                
                # Log a Kafka
                asyncio.run(request_logger.log_request(
                    correlation_id=email_request.correlation_id,
                    service="Email Server",
                    endpoint="/send-email-task",
                    is_valid=True,
                    reason=f"Error al enviar email: {email_result.get('error')}",
                    flow="\n".join(flow_steps),
                    execution_time_ms=execution_time,
                    is_success=False
                ))
                
                return {
                    "status": "error",
                    "message": email_result.get("error", "Error desconocido al enviar correo")
                }
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            error_step = f"Error durante procesamiento: {str(e)}"
            flow_steps.append(f"{len(flow_steps) + 1}. {error_step}")
            
            # Log a Kafka
            asyncio.run(request_logger.log_request(
                correlation_id=email_request.correlation_id,
                service="Email Server",
                endpoint="/send-email-task",
                is_valid=True,
                reason=error_step,
                flow="\n".join(flow_steps),
                execution_time_ms=execution_time,
                is_success=False
            ))
            
            raise

