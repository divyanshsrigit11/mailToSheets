import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    """Authenticates and returns the Gmail service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def fetch_unread_emails(service):
    """Fetches a list of unread email messages."""
    try:
        results = service.users().messages().list(userId='me', q='is:unread in:inbox').execute()
        messages = results.get('messages', [])
        return messages
    except Exception as error:
        print(f"An error occurred fetching emails: {error}")
        return []

def mark_as_read(service, message_id):
    """Removes the 'UNREAD' label from an email."""
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"Marked email {message_id} as read.")
    except Exception as error:
        print(f"Error marking email as read: {error}")