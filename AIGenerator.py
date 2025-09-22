"""
==================================================
 File:    AIGenerator.py
 Author:  Mathis Hurens-Barrette
 Created: 2025-02-15
 Purpose: Creates and sends a prompt to a selected chatgpt model

 Notes:
==================================================

"""

import openai
import config

def generateText(replacements : dict, rolePrompt, contentPrompt):
    openai.api_key = config.OpenAiKey

    for key, value in replacements.items():
        rolePrompt = rolePrompt.replace(key, value)
        contentPrompt = contentPrompt.replace(key, value)

    response = openai.chat.completions.create(
        model="o3-mini",  # Select model
        messages=[
            {"role": "system", "content": rolePrompt}, # Defines a role and content prompt using the argument given with generateText
            {"role": "user", "content": contentPrompt}
        ]
    )

    email_content = response.choices[0].message.content
    return email_content
