"""
Servicio para envío de emails con Gmail API
"""
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from src.connection.gmail_connection import send_with_gmail_api
from src.interfaces.email_interfaces import IEmailSender


class GmailService(IEmailSender):
    """
    Servicio para envío de correos mediante Gmail API
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_email_with_attachment(self, to_email: str, subject: str, body: str, 
                                   pdf_data: bytes, filename: str) -> dict:
        """
        Envía un correo con archivo PDF adjunto
        
        Args:
            to_email (str): Email del destinatario
            subject (str): Asunto del correo
            body (str): Cuerpo del mensaje
            pdf_data (bytes): Datos del PDF en bytes
            filename (str): Nombre del archivo adjunto
            
        Returns:
            dict: Resultado del envío con success y message
        """
        try:
            # Crear mensaje MIME
            message = MIMEMultipart()
            message["to"] = to_email
            message["subject"] = subject
            
            # Adjuntar cuerpo del mensaje
            message.attach(MIMEText(body, "plain"))
            
            # Adjuntar PDF
            part = MIMEApplication(pdf_data, Name=filename)
            part["Content-Disposition"] = f'attachment; filename="{filename}"'
            message.attach(part)
            
            # Enviar correo
            self.logger.info(f"Enviando correo a {to_email} con adjunto '{filename}'")
            send_with_gmail_api(message)
            
            self.logger.info(f"Correo enviado exitosamente a {to_email}")
            return {"success": True, "message": f"Correo enviado a {to_email}"}
        
        except Exception as e:
            self.logger.error(f"Error al enviar correo: {str(e)}")
            return {"success": False, "error": str(e)}
