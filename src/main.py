import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SPREADSHEET_ID
from gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from sheets_service import append_to_sheet
from email_parser import parse_email
from googleapiclient.discovery import build


def main():
    print("--- STARTED EMAIL PROCESSING ---")


    print("1. Authenticating...")
    gmail_service = get_gmail_service()
    
    creds = gmail_service._http.credentials
    sheets_service = build('sheets', 'v4', credentials=creds)

    print("2. Checking for unread emails...")
    messages = fetch_unread_emails(gmail_service)
    
    if not messages:
        print("No new emails found. Exiting.")
        return

    print(f"Found {len(messages)} unread emails. Processing...")

    email_data_list = []
    successful_ids = []

    for msg in messages:
        details = parse_email(msg, gmail_service)
        
        if details:
            row = [
                details['from'],
                details['subject'],
                details['date'],
                details['content']
            ]
            email_data_list.append(row)
            successful_ids.append(details['id'])

    if email_data_list:
        print(f"3. Saving {len(email_data_list)} emails to Google Sheets...")
        success = append_to_sheet(sheets_service, SPREADSHEET_ID, email_data_list)
        
        if success:
            print("4. Marking emails as read...")
            for msg_id in successful_ids:
                mark_as_read(gmail_service, msg_id)
            print("--- JOB COMPLETE: SUCCESS ---")
        else:
            print("--- JOB FAILED: Could not save to Sheets ---")

if __name__ == "__main__":
    main()