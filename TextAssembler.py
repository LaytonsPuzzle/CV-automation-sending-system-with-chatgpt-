"""
==================================================
 File:    TextAssembler.py
 Author:  Mathis Hurens-Barrette
 Created: 2025-02-15
 Purpose: Assemble the first email the AI and man made text to create a smooth transition between the email

 Notes:
==================================================

"""

from AIGenerator import generateText
import config

def textAssemblerFirstEmail(companyName, memberName, pronoun, topic, Website):
    fileToRead = ""

# Example of a possible roal or prompt to be used 
    rolePrompt = "You are an AI assistant that generates personalized internship application emails. Your task is to craft a compelling, first-person paragraph (max 4 sentences) explaining why I want to join a given company. You will connect my past projects to the company's work, selecting only the most relevant examples to maximize impact."
    contentPrompt = """I am interested in an internship at {CompanyName}, which specializes in {Focus}. My interests include new technology, artificial intelligence, creativity, hands-on building, helping others, and solving challenges.

    I have worked on several projects, including:
    - A price-tracking software for a bathroom company.
    - A data visualization tool for my club Kelpie’s submarine competition.
    - A simple security system using a Dragon12 board.
    - A custom-designed ALU.
    - A basic Android app with a database.
    - Programuse, a company I created to teach kids programming.

    Generate a concise, singular and professional sentence that starts with : 'I’m particularly interested in joining {CompanyName}...' explaining why I want to join {CompanyName} based on their work and my interests**. Then, include a few words like "Here are some of my experience that can relate to your companies goals" followed by **bullet points** highlighting how my most **relevant** projects align with their work (using {Website}). **Only select the most relevant projects** instead of listing everything. Keep it professional, engaging, and easy to read.

    """

    # Define the replacements (Generated words from your code)
    replacement_dict = {
        "[Gender]": pronoun,
        "[Name]": memberName,
        "[Company Name]" : companyName,
        # Will generate text using AI
        "[Personalized Text]": generateText({"{CompanyName}": companyName , "{Focus}" : topic, "{Website}": Website}, rolePrompt,contentPrompt)
    }

    # Select one of two text depending on if you know to whom it is address

    if (str(pronoun).lower() == 'none' or str(pronoun).lower() == 'nan' or str(pronoun).lower()  == 'no'):
        fileToRead = config.basicEmailWithoutName
    else:
        fileToRead = config.basicEmailWithName
    

    # Read the original text
    with open(fileToRead, "r") as file:
        original_text = file.read()

    # Replace words
    for old_word, new_word in replacement_dict.items():
        original_text = original_text.replace(str(old_word), str(new_word))

    print("Text processed and appended successfully!")
    return original_text


# Assemble the emailwith generated parts, and man made one
def AssembleFollowUp(secondName, companyName, pronoun, knowName : bool):
    # Decide the start
    if (knowName):
        text = f"Dear {pronoun} {secondName}, \n"
    else:
        text = "To whom it may concern, \n "

    # add the rest of the text
    text += f"""
I hope you're doing well. I wanted to follow up on my last email regarding a position at {companyName} for this Summer. I’m still very interested in the opportunity and excited about the possibility of contributing to your team.

Please let me know if there are any updates regarding my application or if you need any additional information from me. I appreciate your time and consideration since I am sure that you are quite busy.

Best regards,
Mathis Hurens Barrette
3rd Year Computer Engineering Student, University of Ottawa  
Email : ... | Phone : ... | Website : ...
    """
    return text