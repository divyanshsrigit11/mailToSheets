from googleapiclient.discovery import build

def append_to_sheet(service, spreadsheet_id, email_data):
    """
    Appends a list of email data to the Google Sheet.
    email_data should be a LIST of lists: [['sender', 'sub', 'date', 'body'], [...]]
    """
    try:
        range_name = "Sheet1!A:D"
        
        body = {
            "values": email_data
        }

        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print(f"Success! {result.get('updates').get('updatedCells')} cells appended.")
        return True

    except Exception as e:
        print(f"Error writing to Sheet: {e}")
        return False