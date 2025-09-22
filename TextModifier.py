"""
==================================================
 File:    TextModifier.py
 Author:  Mathis Hurens-Barrette
 Created: 2025-02-23
 Purpose: Opens the email in Notepad before it is send to allow the user to apply last minut modifications

 Notes:
==================================================

"""

import subprocess
import os
import config

def modifyText(textToModify, nameOfFile):

    # Save the email to a file
    email_filename = f"{nameOfFile}.txt"
    saveFolderPath = config.emailSavePath

    filePath = os.path.join(saveFolderPath,email_filename)
    with open(filePath, "w") as file:
        file.write(textToModify)

    # Open Notepad and WAIT until it is closed
    subprocess.run(["notepad.exe", filePath])

    print("Notepad closed. Proceeding with the next steps...")

    # return the modified text
    with open(filePath, "r") as file:
        return file.read()
