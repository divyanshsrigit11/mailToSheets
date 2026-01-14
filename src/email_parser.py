import base64

def parse_email(message, service):
    """
    Parses a single email message object from the Gmail API.
    Returns a dictionary with: From, Subject, Date, Content, ID.
    """
    try:
        msg = service.users().messages().get(
            userId='me', 
            id=message['id'], 
            format='full'
        ).execute()

        headers = msg['payload']['headers']
        subject = "No Subject"
        sender = "Unknown"
        date = "Unknown"

        for h in headers:
            if h['name'] == 'Subject':
                subject = h['value']
            elif h['name'] == 'From':
                sender = h['value']
            elif h['name'] == 'Date':
                date = h['value']

        body = ""
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode()
                        break
        else:
            data = msg['payload']['body'].get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode()

        clean_body = " ".join(body.split())[:500]  # limited it to 500 chars

        return {
            "id": message['id'],
            "from": sender,
            "subject": subject,
            "date": date,
            "content": clean_body
        }

    except Exception as e:
        print(f"Error parsing email {message['id']}: {e}")
        return None