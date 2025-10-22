from abc import ABC, abstractmethod

class IEmailSender(ABC):
    @abstractmethod
    def send_email_with_attachment(self, to_email, subject, body, pdf_data, correlation_id):
        pass
