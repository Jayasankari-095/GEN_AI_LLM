import google.generativeai as genai
import os
import pandas as pd

# Configure Gemini AI
genai.configure(api_key="YOUR_GEMINI_API_KEY")  
model = genai.GenerativeModel("gemini-2.0-flash")

def read_text_file(file_path):
    """Reads the content of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""

def ask_llm(content, questions):
    """Uses Gemini AI to extract answers from text."""
    answers = {}
    
    for question in questions:
        prompt = f"""
        Given the following company information:
        {content}
       
        Answer the question concisely:
        {question}
        """
        
        try:
            response = model.generate_content(prompt)
            answers[question] = response.text.strip() if response.text else "No valid response."
        except Exception as e:
            answers[question] = f"Error: {e}"
    
    return answers

def save_to_excel(data, filename="website_data.xlsx"):
    """Saves the extracted details to an Excel file."""
    df = pd.DataFrame.from_dict(data, orient='index')
    df.reset_index(inplace=True)
    df.columns = ["Website", "Mission Statement", "Products/Services", "Founded", "Headquarters", "Executives", "Awards"]
    
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"Data saved to {filename}")

def main():
    questions = [
        "What is the company's mission statement or core values?",
        "What products or services does the company offer?",
        "When was the company founded, and who were the founders?",
        "Where is the company's headquarters located?",
        "Who are the key executives or leadership team members?",
        "Has the company received any notable awards or recognitions?"
    ]
    
    files = [f for f in os.listdir() if f.endswith(".txt")]
    
    if not files:
        print("Error: No text files found.")
        return
    
    website_data = {}
    
    for file_name in files:
        content = read_text_file(file_name)
        if content:
            answers = ask_llm(content, questions)
            website_data[file_name.replace(".txt", "")] = [answers[q] for q in questions]
    
    save_to_excel(website_data)
    
if __name__ == "__main__":
    main()