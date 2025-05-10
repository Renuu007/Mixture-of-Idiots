import openai
import os
from dotenv import load_dotenv
import re
import requests
import markdown
import webbrowser
import tempfile
from tqdm import tqdm
import time
from mistralai import Mistral
import google.generativeai as genai


load_dotenv()

# API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Clients
openai_client = openai.OpenAI(api_key=openai_api_key)
mistral_client = Mistral(api_key=mistral_api_key)
genai.configure(api_key=gemini_api_key)

# Colors (unused in HTML output, kept for possible console outputs or further expansions)
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def call_mistral(model_name, user_message, system_message=None):
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": user_message})
    try:
        response = mistral_client.chat.complete(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling Mistral model {model_name}: {str(e)}")
        return f"Error: Could not get response from {model_name}"

def call_gemini(model_name, user_message):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini model {model_name}: {str(e)}")
        return f"Error: Could not get response from {model_name}"

def call_openai(model_name, user_message, system_message="You are a coder and problem solver expert"):
    response = openai_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

def generate_html_response(full_response, architecture_name):
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>✨ AI Response Report ✨</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
                background-color: #f0f2f5; /* Light grey background */
                margin: 0;
                padding: 20px;
                color: #1c1e21; /* Darker grey text */
                display: flex;
                justify-content: center;
                align-items: flex-start; /* Align to top if content is short */
                min-height: 100vh;
            }}
            .container {{
                background-color: #ffffff; /* White container background */
                border-radius: 12px; /* More rounded corners */
                padding: 30px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.1); /* Softer, more prominent shadow */
                width: 100%;
                max-width: 800px; /* Max width for better readability */
                border: 1px solid #e0e0e0; /* Light border */
            }}
            pre {{
                background-color: #282c34; /* Dark background for code block */
                color: #abb2bf; /* Light text for code block */
                border-radius: 8px; /* Rounded corners for code block */
                padding: 20px;
                font-family: 'Cascadia Code', 'Consolas', 'SFMono-Regular', 'Menlo', 'Courier New', monospace;
                overflow: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 0.95em;
                border: none; /* Remove explicit border if shadow is sufficient */
            }}
            h1 {{
                color: #007bff; /* Blue accent for heading */
                text-align: center;
                margin-bottom: 25px;
                font-size: 2em;
            }}
            p.intro {{
                line-height: 1.6;
                color: #4b5563; /* Slightly lighter text for intro */
                font-size: 1.1em;
                text-align: center;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✨ AI Response Report ✨</h1>
            <p class="intro">📄 This report presents the findings from the Mixture of Models (MOM) system, utilizing the <strong>{architecture_name}</strong> architecture.</p>
            <pre>{full_response}</pre>
        </div>
    </body>
    </html>
    '''

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as temp_file:
        temp_file.write(html_content)
        webbrowser.open('file://' + temp_file.name)

def the_king(user_message):
    king_system_message = """You are a wise and knowledgeable coder and problem solver king who provides thoughtful answers to questions.
    
    You have several advisors, who offer their insights to assist you.
    
    Consider their perspectives and advice, but ultimately provide your own well-reasoned response to the
    problem based on all context and advice. If you find their input helpful, feel free to acknowledge their
    contributions in your answer."""

    advisor_models = {
        # OpenAI Advisors
        "gpt-4o": ("openai", "GPT-4o (OpenAI)"),
        "gpt-4-turbo": ("openai", "GPT-4 Turbo (OpenAI)"),
        # Mistral Advisors
        "open-mixtral-8x22b": ("mistral", "Mixtral 8x22B (Mistral)"),
        "mistral-large-latest": ("mistral", "Mistral Large (Mistral)"),
        # Gemini Advisors
        "models/gemini-2.0-pro-exp-02-05": ("gemini", "Gemini 2.0 Pro (Google)"),
        "models/gemini-2.5-pro-exp-03-25": ("gemini", "Gemini 2.5 Pro (Google)"),
        "models/gemini-2.5-flash-preview-04-17-thinking": ("gemini", "Gemini 2.5 Flash (Google)"),
        "models/gemma-3-27b-it": ("gemini", "Gemma 3.27B (Google)"),
        # Add more models as desired, up to your 10 advisor target if you wish
    }
    
    answers = {}
    print(f"{NEON_GREEN}👑 --- Starting The King Architecture --- 👑{RESET_COLOR}")
    print(f"{YELLOW}🤔 Problem to solve:{RESET_COLOR} {user_message[:200] + '...' if len(user_message) > 200 else user_message}\n")
    
    tasks = [f"Consulting {name_tuple[1]}" for model_key, name_tuple in advisor_models.items()]
    progress_bar = tqdm(tasks, desc="Gathering insights", unit="task", leave=False)

    for model_key, (api_type, display_name) in advisor_models.items():
        progress_bar.set_description(f"Consulting {display_name}")
        print()
        print(f"{CYAN}🗣️  Consulting Advisor: {display_name}...{RESET_COLOR}")
        advice = ""
        if api_type == "openai":
            advice = call_openai(model_key, user_message)
        elif api_type == "mistral":
            advice = call_mistral(model_key, user_message)
        elif api_type == "gemini":
            advice = call_gemini(model_key, user_message)
        
        answers[display_name] = advice
        print(f"{NEON_GREEN}💡 Advice from {display_name}:{RESET_COLOR}\n{advice[:300] + '...' if len(advice) > 300 else advice}")
        print(f"{PINK}---------------------------------------------------------------------------------------------------------------------------------{RESET_COLOR}")
        progress_bar.update()
    progress_bar.close()
    print(f"\n{NEON_GREEN}✅ --- All Advisor Consultations Complete --- ✅{RESET_COLOR}")

    advisor_answers_str = "\n\n".join(f"{name}'s advice:\n{advice}" for name, advice in answers.items())

    print(f"\n{YELLOW}📝 --- Preparing Prompt for The King --- 📝{RESET_COLOR}")
    king_model_name = "gpt-4o" 
    king_prompt = f"Advisors' Advice:\n{advisor_answers_str}\n\nProblem: {user_message}\n\nBased on all the ADVISORS' ADVICE and the original PROBLEM, provide your comprehensive, step-by-step solution. Acknowledge helpful contributions from specific advisors if appropriate by referencing their names (e.g., 'As {display_name} pointed out,...')."
    
    print(f"{CYAN}📜 Full prompt for The King ({king_model_name}):{RESET_COLOR}\n{king_prompt}\n")

    progress_bar_king = tqdm(total=1, desc=f"The King ({king_model_name}) is solving the problem", unit="task")
    
    king_answer = call_openai(king_model_name, king_prompt, king_system_message)
    progress_bar_king.update()
    progress_bar_king.close()
    
    print(f"\n{NEON_GREEN}📣 --- The King Has Spoken --- 📣{RESET_COLOR}")
    print(f"{YELLOW}🌟 Final Answer from The King:{RESET_COLOR}\n{king_answer}")

    return king_answer

question = open_file("problem.txt")
html_response1 = the_king(question)  #First Run
#html_response2 = the_king(html_response1)  # Run it twice
generate_html_response(html_response1, "King")
