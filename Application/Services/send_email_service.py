import logging
from service_storage import get_storage_file
from service_email import send_email_with_pdf

logger = logging.getLogger(__name__)

class SendEmailService:
  
    def execute(self, data: dict):
        logger.info("Iniciando envío de correo con PDF adjunto...")

        correlation_id = data.get("CorrelationId")
        email_to = data.get("EmailAddress")
        subject = data.get("Subject", "Reporte generado automáticamente")
        body = data.get("MessageBody", "Adjunto encontrará su documento PDF.")
        filename = data.get("PdfFileName", f"{correlation_id}.pdf")

        
        if not correlation_id:
            raise ValueError("Falta el campo 'CorrelationId'")
        if not email_to:
            raise ValueError("Falta el campo 'EmailAddress'")

        logger.info(f"Obteniendo PDF desde Storage Server para ID: {correlation_id}")

        # Para Obtener PDF desde Storage Server
        pdf_data = get_storage_file(correlation_id)
        logger.info(f"PDF obtenido correctamente ({len(pdf_data)} bytes)")

        # Para Enviar correo con el PDF adjunto
        logger.info(f"Enviando correo a {email_to} con archivo {filename}")
        email_result = send_email_with_pdf(
            to_email=email_to,
            subject=subject,
            body=body,
            pdf_data=pdf_data,
            filename=filename
        )

        if email_result["success"]:
            logger.info(f"Correo enviado correctamente a {email_to}")
            return {
                "status": "success",
                "message": f"Correo enviado correctamente a {email_to}"
            }
        else:
            logger.error(f"Error al enviar correo: {email_result.get('error')}")
            return {
                "status": "error",
                "message": email_result.get("error", "Error desconocido al enviar correo")
            }
