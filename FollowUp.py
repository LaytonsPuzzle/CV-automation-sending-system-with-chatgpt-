"""
==================================================
 File:    TextAssembler.py
 Author:  Mathis Hurens-Barrette
 Created: 2025-02-15
 Purpose: Create a follow up email with the given data

 Notes:
==================================================

"""

import imaplib
import smtplib
import email
import pandas as pd
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from TextAssembler import AssembleFollowUp

# Your Gmail credentials
EMAIL_ADDRESS = config.MyEmailAddress
APP_PASSWORD = config.GmailKey

# Read contacts from Excel
excelData = pd.read_excel(config.fullDataSheet)  # Ensure it has a column "Email"


# Connect to Gmail's IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL_ADDRESS, APP_PASSWORD)


mail.select('"[Gmail]/Send"')  # Access the message envoyé folder



def find_sent_email(recipient):
    """Find the last email sent to the recipient."""
    print(recipient)
    result, data = mail.search(None, f'TO "{recipient}"')
    if result == "OK":
        email_ids = data[0].split()
        if email_ids:
            return email_ids[-1]  # Get the latest sent email
    return None

def send_follow_up(original_email_id, recipient, secondName, companyName, pronoun):
    iKnowTheName = True
    # Verify how to start email
    if str(pronoun).lower() == 'none' or str(pronoun).lower() == 'nan' or str(pronoun).lower()  == 'no':
            iKnowTheName = False


    """Send a follow-up email as a reply."""
    # Fetch original email
    result, data = mail.fetch(original_email_id, "(RFC822)")
    if result != "OK":
        print(f"Could not fetch email for {recipient}")
        return

    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    subject = "Re: " + msg["Subject"]  # Reply with original subject
    original_message = msg.get_payload()  # Get original message content

    # Create follow-up email
    follow_up = MIMEMultipart()
    follow_up["From"] = EMAIL_ADDRESS
    follow_up["To"] = recipient
    follow_up["Subject"] = subject
    follow_up["In-Reply-To"] = msg["Message-ID"]
    follow_up.attach(MIMEText(AssembleFollowUp(secondName, companyName, pronoun, iKnowTheName), "plain"))

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient, follow_up.as_string())

    print(f"Follow-up email sent to {recipient}")

def CreateFollowUpEmail():
    # Process each contact
    global excelData
    for index, row in excelData.iterrows():
        if row["Follow-Up"].lower() == "no":
            choice = input(f"I will send a follow up to {row['Member Name']}. Send?: ")
            # Confirms if you want to send the follow-up
            if choice.lower() != "yes":
                continue
            # sends the email
            email_id = find_sent_email(row["Email"])
            if email_id:
                send_follow_up(email_id, row["Email"], str(row['Member Name']).split()[-1], row['Company Name'], row['Pronoun'])
            else:
                print(f"No sent email found for {row["Email"]}")

    # Close IMAP connection
    mail.logout()
