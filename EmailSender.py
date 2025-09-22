"""
==================================================
 File:    EmailSender.py
 Author:  Mathis Hurens-Barrette
 Created: 2025-02-15
 Purpose: Goes through a list of senders to create and send a personalise email to each of them

 Notes:
==================================================

"""


import smtplib
import pandas as pd
import traceback
import os
import config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from TextAssembler import textAssemblerFirstEmail
from TextModifier import modifyText
from FollowUp import CreateFollowUpEmail

# Initialise all important data
data = pd.read_excel(config.fullDataSheet)
sender_email = config.MyEmailAddress
password = config.GmailKey
attachement_path = config.CV_path


def FirstEmailCreation():
    try:
        # Iterate throught all the subjects
        for index, row in data.iterrows():
            # Skips email already sent
            if (row['Sent?'].lower() == 'no'):
                startProcess = input(f"I will now write an email for {row['Company Name']}. Proceed? : ")
                if startProcess.lower() != 'yes':
                    continue

                receiver_email = row['Email']
                # Create message
                email_content = (textAssemblerFirstEmail(row['Company Name'], str(row['Member Name']).split()[-1], row['Pronoun'], row['Topic'], row['Website']))
                print(email_content)


                #allows to modify the email before it is send
                while (1==1):
                    delay = input("Would you like to send it to " + str(row['Member Name'])  +'? : ').lower()
                    if delay == 'modify':
                        print ('modifing the email')
                        email_content = modifyText(email_content, row['Company Name'])
                        print('Email modified')
                    else:
                        break

                # allows to stop the email before it is send
                if delay == "skip":
                    continue
                elif delay!= 'send' and delay != "yes":
                    break

                # Creates the email
                msg = MIMEMultipart()
                msg['Subject'] = f"Seeking Internship Opportunity at {row['Company Name']}"
                msg['From'] = sender_email
                msg['To'] = row['Email']

                # Attach the email text as the main body
                msg.attach(MIMEText(email_content, "plain"))


                # Attach the file
                with open(attachement_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                # Encode to base64
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachement_path)}")
                msg.attach(part)

                # Send the message
                # Start the server
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print(f"Email sent to {msg['To']}")

    except Exception as e:
        print(f"Error: {traceback.format_exc()}")


    finally:
        server.quit()


while True:

    choice = input("Would you like to write an email (1) or do a follow-up(2)? : ").strip().lower()
    if choice == "1":
        FirstEmailCreation()

    elif choice == "2":
        CreateFollowUpEmail()

    elif choice == "leave":
        print("Exiting...")
        break
    else:
        print("Invalid input. Please enter 1, 2, or 'leave'.")