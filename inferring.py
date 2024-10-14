'''


    @Author: Shivraj Yelave
    @Date: 14/10/2024
    @Last Modified by: Shivraj Yelave
    @Last Modified time: 14/10/2024
    @Title: Python Code to process reviews, identify item, company, sentiment, and generate appropriate responses


'''

import csv
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Function to analyze sentiment and generate appropriate messages
def analyze_sentiment_and_generate_message(body):

    """
    Description:
    Analyze the sentiment of the review and generate a thank-you or apology message based on the sentiment.

    Parameters:
    body (str): The content of the review.

    Returns:
    tuple: A tuple containing:
        - sentiment_response (str): The sentiment of the review, either 'positive' or 'negative'.
        - response_message (str): A generated thank-you message for positive reviews or an apology message for negative reviews.
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

    # Analyze sentiment
    chat_session = model.start_chat(history=[])
    prompt = f"Analyze the sentiment of the following review. Respond with only 'positive' or 'negative':\n\n{body}\n"
    sentiment_response = chat_session.send_message(prompt).text.strip()

    # Generate appropriate message
    if "positive" in sentiment_response.lower():
        message_prompt = f"Generate a short thank-you message for the following positive review:\n\n{body}\n"
    else:
        message_prompt = f"Generate an short apology message for the following negative review:\n\n{body}\n"
    
    response_message = chat_session.send_message(message_prompt).text.strip()
    
    return sentiment_response, response_message

# Function to extract item and company
def extract_item_and_company(body):
    
    """
    Description:
    Extract the purchased item and the company name from the review.

    Parameters:
    body (str): The content of the review.

    Returns:
    tuple: A tuple containing:
        - item_response (str): The name of the purchased item, or 'unknown' if not identifiable.
        - company_response (str): The name of the company that made the item, or 'unknown' if not identifiable.
    """
    
    generation_config = {
        "temperature": 0.7,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Extract item
    chat_session = model.start_chat(history=[])
    item_prompt = f"Just Identify the purchased item in the following review: Respond with only the company name, such as 'Samsung phone':\n\n{body}\n"
    item_response = chat_session.send_message(item_prompt).text.strip() or "unknown"
    
    # Extract company
    company_prompt = f"Just identify the company name that made the item in the following review. Respond with only the company name, such as 'Samsung':\n\n{body}\n"
    company_response = chat_session.send_message(company_prompt).text.strip() or "unknown"

    return item_response, company_response


def main():
    # Read reviews from the text file
    reviews = []
    with open('C:\\Users\\Admin\\Documents\\ML_programs\\ML_Tasks\\GenAi\\reviews.txt', 'r') as file:
        review_content = file.read().strip().split('END')

    # Process each review
    for review in review_content:
        body = review.strip()

        # Extract item and company
        item, company = extract_item_and_company(body)
        
        # Analyze sentiment and generate message
        sentiment, response_message = analyze_sentiment_and_generate_message(body)
        
        # Store the extracted data
        reviews.append({
            "item": item,
            "company": company,
            "sentiment": sentiment,
            "response_message": response_message
        })

    # Save the extracted data to a CSV file using UTF-8 encoding
    output_file_path = 'C:\\Users\\Admin\\Documents\\ML_programs\\ML_Tasks\\GenAi\\review_output.csv'
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Item', 'Company', 'Sentiment', 'Response Message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for review in reviews:
            writer.writerow({
                'Item': review['item'],
                'Company': review['company'],
                'Sentiment': review['sentiment'],
                'Response Message': review['response_message']
            })

    print(f"Reviews have been processed and saved to {output_file_path}")

if __name__ == '__main__':
    main()
