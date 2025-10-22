"""
Servicio principal para envío de emails con PDFs adjuntos
"""
import logging
from src.dto.email_dto import EmailRequest
from src.services.gmail_service import GmailService
from src.services.storage_service import StorageService


class SendEmailService:
    """
    Servicio de aplicación para enviar emails con PDFs desde Storage
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gmail_service = GmailService()
        self.storage_service = StorageService()

    def execute(self, data: dict) -> dict:
        """
        Ejecuta el proceso de envío de email con PDF adjunto
        
        Args:
            data (dict): Diccionario con los datos del request
            
        Returns:
            dict: Resultado del proceso con status y message
            
        Raises:
            ValueError: Si faltan campos obligatorios
        """
        self.logger.info("Iniciando envío de correo con PDF adjunto...")

        # Crear y validar DTO
        email_request = EmailRequest.from_dict(data)
        email_request.validate()
        
        # Determinar nombre del archivo
        filename = email_request.pdf_filename or f"{email_request.correlation_id}.pdf"
        
        self.logger.info(f"Obteniendo PDF desde Storage Server para ID: {email_request.correlation_id}")
        
        # Obtener PDF desde Storage Server
        pdf_data = self.storage_service.get_pdf_by_correlation(email_request.correlation_id)
        self.logger.info(f"PDF obtenido correctamente ({len(pdf_data)} bytes)")

        # Enviar correo con el PDF adjunto
        self.logger.info(f"Enviando correo a {email_request.email_address} con archivo {filename}")
        email_result = self.gmail_service.send_email_with_attachment(
            to_email=email_request.email_address,
            subject=email_request.subject,
            body=email_request.message_body,
            pdf_data=pdf_data,
            filename=filename
        )

        if email_result["success"]:
            self.logger.info(f"Correo enviado correctamente a {email_request.email_address}")
            return {
                "status": "success",
                "message": f"Correo enviado correctamente a {email_request.email_address}"
            }
        else:
            self.logger.error(f"Error al enviar correo: {email_result.get('error')}")
            return {
                "status": "error",
                "message": email_result.get("error", "Error desconocido al enviar correo")
            }
