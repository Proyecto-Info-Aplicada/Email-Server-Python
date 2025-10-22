import requests
import logging
from config import STORAGE_URL

class PdfRetriever:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_pdf_by_correlation(self, correlation_id: str) -> bytes:
        url = f"{STORAGE_URL}/pdf-storage/{correlation_id}"
        self.logger.info(f"[{correlation_id}] Solicitando PDF desde {url}")

        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                self.logger.info(f"[{correlation_id}] PDF recuperado correctamente ({len(resp.content)} bytes)")
                return resp.content
            else:
                self.logger.error(f"[{correlation_id}] Error al obtener PDF: {resp.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"[{correlation_id}] Error al comunicarse con Storage: {str(e)}")
            return None
