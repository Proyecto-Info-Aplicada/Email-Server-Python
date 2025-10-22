import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from gmail_api import send_with_gmail_api


def send_email_with_pdf(to_email: str, subject: str, body: str, pdf_data: bytes, filename: str):
    
    try:
        
        message = MIMEMultipart()
        message["to"] = to_email
        message["subject"] = subject

        
        message.attach(MIMEText(body, "plain"))

        part = MIMEApplication(pdf_data, Name=filename)
        part["Content-Disposition"] = f'attachment; filename="{filename}"'
        message.attach(part)

        send_with_gmail_api(message)

        print(f"Correo enviado a {to_email} con adjunto '{filename}'")
        return {"success": True}

    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return {"success": False, "error": str(e)}
