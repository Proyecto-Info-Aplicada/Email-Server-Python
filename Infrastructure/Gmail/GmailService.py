import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from gmail_api import send_with_gmail_api

class GmailService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_email_with_attachment(self, to_email, subject, body, pdf_data, correlation_id):
        msg = MIMEMultipart()
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        attachment = MIMEApplication(pdf_data, _subtype="pdf")
        attachment.add_header("Content-Disposition", "attachment", filename=f"{correlation_id}.pdf")
        msg.attach(attachment)

        self.logger.info(f"[{correlation_id}] Enviando correo a {to_email}")
        send_with_gmail_api(msg)
