# Gmail to Google Sheets Automation

Name: Divyansh Srivastava  
Technology: Python 3, Gmail API, Google Sheets API  

## 1. Project Overview
This Python automation tool connects to a Gmail account, fetches unread emails, and logs the Sender, Subject, Date, and Body into a Google Sheet. Once processed, emails are marked as "Read" to ensure they are not duplicated in future runs.

## 2. High-Level Architecture
(Note: You can replace this text with the ASCII diagram below)

[ Gmail Server ]  <-- (1. Fetch 'is:unread') -- [ Python Script ]
       |                                                       |
       |                                                 (2. Parse Data)
       |                                                       |
(4. Remove 'UNREAD' label)                               (3. Append Row)
       ^                                                       |
       |----------------------------------------------- [ Google Sheets ]

## 3. Setup Instructions
### Prerequisites
- Python 3.13.1 installed
- A Google Cloud Project with Gmail and Sheets APIs enabled

4. Design & Technical Explanation
OAuth 2.0 Flow
I used the InstalledAppFlow strategy.

Why: This is a desktop/CLI application running locally, so it needs to launch a local browser for the user to grant permissions safely.

Token Storage: After the first login, the access and refresh tokens are stored in token.json so the user doesn't need to log in every time.

State Management & Duplicate Prevention
Instead of using a local database (SQLite) or a text file to track processed IDs, I utilized Gmail's native "UNREAD" label.

Logic: The script queries specifically for q='is:unread'.

Persistence: After successfully appending the data to Google Sheets, the script calls gmail.modify() to remove the UNREAD label.

Benefit: This makes the script stateless. I can run it on any machine, and it will strictly process only new, unseen emails. If the script fails halfway (before marking as read), the email remains unread and will be retried on the next run, ensuring no data loss.

5. Challenges Faced & Solutions
Challenge: Handling Multiple API Scopes Problem: Initially, I authenticated only with the Gmail scope. When I added the Google Sheets logic later, the application failed with a 403 Forbidden error because the existing token.json did not contain permissions for Sheets. Solution: I modified the SCOPES list in the configuration to include both gmail.modify and spreadsheets. Then, I deleted the old token.json to force the OAuth flow to re-run, prompting the user to grant the new combined permissions.

6. Limitations
Plain Text Only: The parser currently extracts the text/plain part of the email MIME structure. Rich HTML emails might lose formatting.

Attachment Handling: The script ignores attachments (images, PDFs) and only logs the body text.

API Quotas: The solution is subject to Google's daily API rate limits (though sufficient for personal use).

7. Proof of Execution
(Paste your Video Link Here)

Video Demo: https://drive.google.com/file/d/1JiO7QyvHdhIbFXUHbCEKEfvLGL0wZCHT/view?usp=sharing

Screenshots: See the proof/ folder in this repository for screenshots of the Inbox, Sheet, and Terminal output.

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/divyanshsrigit11/mailToSheets.git
   cd gmailToSheets