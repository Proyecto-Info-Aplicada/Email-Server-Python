"""
Data Transfer Objects (DTOs) para el proyecto
"""
import uuid
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class EmailRequest:
    """
    DTO para solicitudes de envío de email
    """
    correlation_id: str
    email_address: str
    subject: str
    message_body: str
    pdf_filename: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de EmailRequest desde un diccionario
        
        Args:
            data (dict): Diccionario con los datos del request
            
        Returns:
            EmailRequest: Instancia creada
        """
        return cls(
            correlation_id=data.get("CorrelationId", str(uuid.uuid4())),
            email_address=data.get("EmailAddress"),
            subject=data.get("Subject", "Reporte generado automáticamente"),
            message_body=data.get("MessageBody", "Adjunto encontrará su documento PDF."),
            pdf_filename=data.get("PdfFileName")
        )
    
    def validate(self):
        """
        Valida que los campos obligatorios estén presentes
        
        Raises:
            ValueError: Si falta algún campo obligatorio
        """
        if not self.correlation_id:
            raise ValueError("Falta el campo 'CorrelationId'")
        if not self.email_address:
            raise ValueError("Falta el campo 'EmailAddress'")


@dataclass
class BaseRequest:
    """
    DTO base para requests genéricos
    """
    correlation_id: str
    path: str
    timestamp: str
    
    def __init__(self, path: str):
        self.correlation_id = str(uuid.uuid4())
        self.path = path
        self.timestamp = datetime.now().isoformat()
