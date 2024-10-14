'''


    @Author: Shivraj Yelave
    @Date: 13/10/2024
    @Last Modified by: Shivraj Yelave
    @Last Modified time: 13/10/2024
    @Title: python Code To summarize the mail and translate into spanish using prompt engineering


'''

import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Function to summarize the email body
def summarize_email(body):
    
    """
    Generate a summary for the given email body using Google Generative AI.

    Parameters:
    body (str): The content of the email.

    Returns:
    str: A brief summary of the email content.
    
    """

    generation_config = {
        "temperature": 1,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    # Start a chat session for summarization
    chat_session = model.start_chat(history=[])
    prompt = f"Summarize the following email in short:\n\n{body}\n"
    response = chat_session.send_message(prompt)
    
    return response.text.strip()

# Function to translate text to Spanish
def translate_to_spanish(text):
    
    """
    Translate the given text to Spanish using Google Generative AI.

    Parameters:
    text (str): The text to be translated.

    Returns:
    str: The translated text in Spanish.
    
    """
    
    translation_config = {
        "temperature": 0.5,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=translation_config,
    )

    # Start a chat session for translation
    chat_session = model.start_chat()
    prompt = f"Translate the following text to Spanish:\n\n{text}\n"
    response = chat_session.send_message(prompt)
    
    return response.text.strip()

def  main():

    # Read emails from the text file
    emails = []
    with open('C:\\Users\\Admin\\Documents\\ML_programs\\ML_Tasks\\GenAi\\sample_mails.txt', 'r') as file:
        email_content = file.read().strip().split('END')

    # Process each email
    for email in email_content:
        lines = email.strip().split('\n')
        if len(lines) < 4:
            continue  # Skip incomplete emails

        # Extract relevant fields
        to_line = lines[1].replace("To: ", "").strip()
        from_line = lines[0].replace("From: ", "").strip()
        subject_line = lines[2].replace("Subject: ", "").strip()
        body = "\n".join(lines[4:]).replace("Body:\n", "").strip() 

        # Get the summary
        summary = summarize_email(body)
        
        # Translate the summary to Spanish
        summary_spanish = translate_to_spanish(summary)

        # Store the extracted data
        emails.append({
            "to": to_line,
            "from": from_line,
            "subject": subject_line,
            "summary": summary,
            "summary_spanish": summary_spanish,
        })

    # Save the extracted data to a CSV file
    csv_file_path = 'C:\\Users\\Admin\\Documents\\ML_programs\\ML_Tasks\\GenAi\\emails.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ["to", "from", "subject", "summary", "summary_spanish"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(emails)

    print(f"Emails have been saved to {csv_file_path}")
if __name__ == '__main__':
    main()