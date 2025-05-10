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

def call_gemini(model_name, user_message, system_message=None):
    # Gemini API typically takes system instruction differently or as part of the first user message
    # For simplicity, we prepend system message to user message if provided.
    full_prompt = user_message
    if system_message:
        full_prompt = f"{system_message}\n\n{user_message}"
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(full_prompt)
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
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def duopoly(user_message):
    print(f"{NEON_GREEN}👑 --- Starting The Duopoly Architecture --- 👑{RESET_COLOR}")
    print(f"{YELLOW}🤔 Problem to solve:{RESET_COLOR} {user_message[:200] + '...' if len(user_message) > 200 else user_message}\n")

    # Define Oracles and Summarizer - using a mix from available APIs
    oracle1_model_type = "openai"
    oracle1_model_name = "gpt-4o" # Powerful OpenAI model
    oracle1_display_name = "Oracle GPT-4o"

    oracle2_model_type = "mistral"
    oracle2_model_name = "open-mixtral-8x22b" # Powerful Mistral model
    oracle2_display_name = "Oracle Mixtral"
    
    # Alternatively, Oracle 2 could be Gemini:
    # oracle2_model_type = "gemini"
    # oracle2_model_name = "models/gemini-1.5-pro-latest"
    # oracle2_display_name = "Oracle Gemini 1.5 Pro"

    summarizer_model_type = "openai" # Or choose mistral/gemini
    summarizer_model_name = "gpt-4-turbo"
    summarizer_display_name = "Summarizer GPT-4 Turbo"

    system_message_oracle1 = (f"You are {oracle1_display_name}, a wise and knowledgeable coder and problem solver expert. Discuss and push back at {oracle2_display_name}, challenge their suggestions, and evaluate the best solutions based on context from other advisors and the problem: {user_message}")
    system_message_oracle2 = (f"You are {oracle2_display_name}, a wise and knowledgeable coder and problem solver expert. Discuss and push back at {oracle1_display_name}, challenge their suggestions, and evaluate the best solutions based on context from other advisors and the problem: {user_message}")
    system_message_summarizer = ("You are an expert at looking at a conversation between two smart oracles and extracting the best answer to a problem from the conversation.")
    
    print(f"{CYAN}🛠️  Setting up Oracles and Summarizer...{RESET_COLOR}")
    print(f"{PINK}Oracle 1 ({oracle1_model_type}): {oracle1_display_name} ({oracle1_model_name}){RESET_COLOR}")
    print(f"{PINK}Oracle 2 ({oracle2_model_type}): {oracle2_display_name} ({oracle2_model_name}){RESET_COLOR}")
    print(f"{PINK}Summarizer ({summarizer_model_type}): {summarizer_display_name} ({summarizer_model_name}){RESET_COLOR}\n")

    conversation_history = []
    
    # Updated advisor models (formerly peasant_models)
    advisor_models = {
        "gpt-4-turbo-preview": ("openai", "GPT-4 Turbo Preview (OpenAI)"),
        "mistral-small-latest": ("mistral", "Mistral Small (Mistral)"),
        "models/gemini-1.5-flash-latest": ("gemini", "Gemini 1.5 Flash (Google)"),
        # Add a few more diverse advisors if desired
    }
    initial_answers = {}
    tasks = [f"Consulting {name_tuple[1]}" for model_key, name_tuple in advisor_models.items()]
    print(f"{YELLOW}🤝 --- Gathering Initial Insights from Advisors --- 🤝{RESET_COLOR}")
    progress_bar = tqdm(tasks, desc="Gathering initial insights", unit="task", leave=False)

    for model_key, (api_type, display_name) in advisor_models.items():
        progress_bar.set_description(f"Consulting {display_name}")
        print() # Gap before advisor name
        print(f"{CYAN}🗣️  Consulting Advisor: {display_name}...{RESET_COLOR}")
        advice = ""
        if api_type == "openai":
            advice = call_openai(model_key, user_message)
        elif api_type == "mistral":
            advice = call_mistral(model_key, user_message)
        elif api_type == "gemini":
            advice = call_gemini(model_key, user_message)
        initial_answers[display_name] = advice
        print(f"{NEON_GREEN}💡 Advice from {display_name}:{RESET_COLOR}\n{advice[:300] + '...' if len(advice) > 300 else advice}")
        print() # Gap after advice
        print(f"{PINK}------------------------------------------------------------------------------------------------{RESET_COLOR}")
        progress_bar.update()  
    progress_bar.close()
    print(f"\n{NEON_GREEN}✅ --- Initial Advisor Insights Gathered --- ✅{RESET_COLOR}\n")
        
    advisor_insights_str = "\n\n".join(f"{name}'s advice: {advice}" for name, advice in initial_answers.items())
    
    print(f"{YELLOW}💬 --- Starting Oracle Discussion --- 💬{RESET_COLOR}")
    # Initial prompt for the discussion
    discussion_start_prompt = (f"ADVISORS' INSIGHTS:\n{advisor_insights_str}\n\nHello {oracle1_display_name} and {oracle2_display_name}. Let's discuss and find a solution to the PROBLEM while challenging each other and taking the ADVISORS' INSIGHTS into consideration. Solve the PROBLEM: {user_message}")
    
    # Let Oracle 1 (e.g. OpenAI) start the conversation based on the initial prompt for Oracle 2
    # Oracle 2 will then respond to Oracle 1
    current_message_for_oracle2 = discussion_start_prompt
    conversation_history.append(f"System: The problem to solve is: {user_message}. Initial insights have been gathered. The discussion begins.")
    conversation_history.append(f"System to {oracle2_display_name}: {discussion_start_prompt}")
    print(f"{CYAN}📜 Initial prompt for {oracle2_display_name} (and for {oracle1_display_name} to start):{RESET_COLOR}\n{discussion_start_prompt[:300]+'...'}\n")

    # Number of turns for the discussion (e.g., 3 exchanges = 6 messages total)
    num_exchanges = 3 

    discussion_progress_bar = tqdm(range(num_exchanges * 2), desc="Oracle Discussion", unit="turn", leave=False)

    for i in range(num_exchanges * 2):
        turn_context = "\n".join(conversation_history)
        
        if i % 2 == 0:  # Oracle 1's turn (e.g., OpenAI)
            print() # Gap
            discussion_progress_bar.set_description(f"🗣️ {oracle1_display_name} is thinking...")
            # Oracle 1 uses the message intended for Oracle 2 as its input, plus its own system prompt
            response_oracle1 = ""
            if oracle1_model_type == "openai":
                response_oracle1 = call_openai(oracle1_model_name, current_message_for_oracle2, system_message_oracle1)
            elif oracle1_model_type == "mistral":
                response_oracle1 = call_mistral(oracle1_model_name, current_message_for_oracle2, system_message_oracle1)
            elif oracle1_model_type == "gemini":
                response_oracle1 = call_gemini(oracle1_model_name, current_message_for_oracle2, system_message_oracle1)
            
            message_from_oracle1 = f"{oracle1_display_name} said: {response_oracle1}"
            print(f"{YELLOW}💬 {message_from_oracle1}{RESET_COLOR}")
            print() # Gap after message
            print(f"{PINK}------------------------------------------------------------------------------------------------{RESET_COLOR}")
            conversation_history.append(message_from_oracle1)
            current_message_for_oracle1 = response_oracle1 # Next input for Oracle 2 will be this response
        else:  # Oracle 2's turn (e.g., Mistral/Gemini)
            print() # Gap
            discussion_progress_bar.set_description(f"🗣️ {oracle2_display_name} is thinking...")
            # Oracle 2 responds to what Oracle 1 just said
            response_oracle2 = ""
            prompt_for_oracle2 = f"{oracle1_display_name} previously said: {current_message_for_oracle1}\n\nNow, {oracle2_display_name}, please respond considering the ongoing discussion, the initial advisors' insights, and the problem."
            if oracle2_model_type == "openai":
                response_oracle2 = call_openai(oracle2_model_name, prompt_for_oracle2, system_message_oracle2)
            elif oracle2_model_type == "mistral":
                response_oracle2 = call_mistral(oracle2_model_name, prompt_for_oracle2, system_message_oracle2)
            elif oracle2_model_type == "gemini":
                response_oracle2 = call_gemini(oracle2_model_name, prompt_for_oracle2, system_message_oracle2)

            message_from_oracle2 = f"{oracle2_display_name} said: {response_oracle2}"
            print(f"{CYAN}💬 {message_from_oracle2}{RESET_COLOR}")
            print() # Gap after message
            print(f"{PINK}------------------------------------------------------------------------------------------------{RESET_COLOR}")
            conversation_history.append(message_from_oracle2)
            current_message_for_oracle2 = response_oracle2 # Next input for Oracle 1 will be this response

        discussion_progress_bar.update()
        time.sleep(0.5) # Small delay
    discussion_progress_bar.close()
    print(f"\n{NEON_GREEN}✅ --- Oracle Discussion Complete --- ✅{RESET_COLOR}\n")

    full_conversation = "\n".join(conversation_history)
    
    print(f"{YELLOW}📝 --- Summarizing Discussion --- 📝{RESET_COLOR}")
    # Summarize the conversation
    summarizer_progress_bar = tqdm(total=1, desc=f"🗣️ {summarizer_display_name} is summarizing", unit="task", leave=True) # leave=True for final bar
    final_response = ""
    final_prompt = f"Based on the following discussion between {oracle1_display_name} and {oracle2_display_name}, and the initial advisors' insights, provide a comprehensive final answer to the original problem: {user_message}\n\nFull Discussion:\n{full_conversation}"
    if summarizer_model_type == "openai":
        final_response = call_openai(summarizer_model_name, final_prompt, system_message_summarizer)
    elif summarizer_model_type == "mistral":
        final_response = call_mistral(summarizer_model_name, final_prompt, system_message_summarizer)
    elif summarizer_model_type == "gemini":
        final_response = call_gemini(summarizer_model_name, final_prompt, system_message_summarizer)
    
    summarizer_progress_bar.update()
    summarizer_progress_bar.close()
    print(f"\n{NEON_GREEN}🏆 --- Final Answer from Duopoly Summarizer --- 🏆{RESET_COLOR}")
    print(f"{YELLOW}🌟 Summarized Answer:{RESET_COLOR}\n{final_response}")
    return final_response


# The HTML generator function remains the same
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

# Example usage
question = open_file("problem.txt")
final_response = duopoly(question)
generate_html_response(final_response, "Duopoly")
