import os
import base64
import logging
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

logger = logging.getLogger(__name__)

def get_gmail_service():
   
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            logger.info("Abriendo flujo OAuth para Gmail...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Guardar token
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

   
    service = build('gmail', 'v1', credentials=creds)
    return service


def send_with_gmail_api(msg: MIMEMultipart):
   
    try:
        service = get_gmail_service()

      
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        message = {'raw': raw_message}

        # Enviar el correo
        send_result = service.users().messages().send(userId="me", body=message).execute()
        logger.info(f"Correo enviado exitosamente. ID del mensaje: {send_result['id']}")
        return send_result

    except HttpError as error:
        logger.error(f"Error al enviar correo: {error}")
        raise RuntimeError("Fallo al enviar el correo por Gmail API.")
