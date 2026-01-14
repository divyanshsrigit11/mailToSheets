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

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/divyanshsrigit11/mailToSheets.git
   cd gmailToSheets