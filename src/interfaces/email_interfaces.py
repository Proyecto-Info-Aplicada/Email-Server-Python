"""
Interfaces del proyecto
"""
from abc import ABC, abstractmethod


class IEmailSender(ABC):
    """
    Interfaz para servicios de envío de email
    """
    @abstractmethod
    def send_email_with_attachment(self, to_email: str, subject: str, body: str, 
                                   pdf_data: bytes, filename: str) -> dict:
        """
        Envía un email con archivo adjunto
        
        Args:
            to_email (str): Email del destinatario
            subject (str): Asunto del correo
            body (str): Cuerpo del mensaje
            pdf_data (bytes): Datos del PDF en bytes
            filename (str): Nombre del archivo adjunto
            
        Returns:
            dict: Resultado del envío
        """
        pass


class IPdfRetriever(ABC):
    """
    Interfaz para servicios de obtención de PDFs
    """
    @abstractmethod
    def get_pdf_by_correlation(self, correlation_id: str) -> bytes:
        """
        Obtiene un PDF usando su correlation ID
        
        Args:
            correlation_id (str): ID de correlación del PDF
            
        Returns:
            bytes: Datos del PDF
        """
        pass
