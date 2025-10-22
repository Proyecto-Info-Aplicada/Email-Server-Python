"""
Servicio para obtener PDFs desde el Storage Server
"""
import logging
import requests
from src.config.settings import STORAGE_URL, TIMEOUT_SECONDS
from src.interfaces.email_interfaces import IPdfRetriever


class StorageService(IPdfRetriever):
    """
    Servicio para obtener archivos PDF desde el Storage Server
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage_url = STORAGE_URL

    def get_pdf_by_correlation(self, correlation_id: str) -> bytes:
        """
        Obtiene un archivo PDF del Storage Server usando el correlation_id
        
        Args:
            correlation_id (str): ID de correlación del PDF
            
        Returns:
            bytes: Datos del PDF en bytes
            
        Raises:
            RuntimeError: Si falla la obtención del PDF
        """
        url = f"{self.storage_url}/{correlation_id}"
        self.logger.info(f"[{correlation_id}] Solicitando PDF desde {url}")

        try:
            response = requests.get(url, timeout=TIMEOUT_SECONDS, stream=True)
            
            if response.status_code == 200:
                self.logger.info(f"[{correlation_id}] PDF recuperado correctamente ({len(response.content)} bytes)")
                return response.content
            else:
                error_msg = f"Error al obtener PDF ({response.status_code}): {response.text}"
                self.logger.error(f"[{correlation_id}] {error_msg}")
                raise RuntimeError(error_msg)
                
        except requests.RequestException as e:
            error_msg = f"Error al comunicarse con Storage Server: {str(e)}"
            self.logger.error(f"[{correlation_id}] {error_msg}")
            raise RuntimeError(error_msg)
