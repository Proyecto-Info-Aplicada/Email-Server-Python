from abc import ABC, abstractmethod

class IPdfRetriever(ABC):
    @abstractmethod
    def get_pdf_by_correlation(self, correlation_id: str) -> bytes:
        pass
