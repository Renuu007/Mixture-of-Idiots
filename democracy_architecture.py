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

PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

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
    full_prompt = user_message
    if system_message:
        full_prompt = f"{system_message}\n\nUser query: {user_message}"
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

def the_democracy(user_message):
    print(f"{NEON_GREEN}🏛️ --- Starting The Democracy Architecture --- 🏛️{RESET_COLOR}")
    print(f"{YELLOW}🤔 Problem to solve:{RESET_COLOR} {user_message[:200] + '...' if len(user_message) > 200 else user_message}\n")

    vote_counting_system_message = "You are an impartial vote counter. You will be given a list of solutions and then a list of votes. Each vote will state which solution it is for. Count the votes accurately for each solution and clearly state which solution received the most votes and how many votes it received. If there is a tie, state the tied solutions and their vote counts. Present the winning solution text clearly."
    general_expert_system_message = "You are a coder and problem solver expert."
    
    democratic_models = [
        ("openai", "gpt-4o-mini", "GPT-4o mini (OpenAI)"),
        ("openai", "gpt-4-turbo-preview", "GPT-4 Turbo Preview (OpenAI)"),
        ("mistral", "mistral-small-latest", "Mistral Small (Mistral)"),
        ("mistral", "open-mixtral-8x22b", "Mixtral 8x22B (Mistral)"),
        ("gemini", "models/gemini-1.5-flash-latest", "Gemini 1.5 Flash (Google)"),
        ("gemini", "models/gemini-1.5-pro-latest", "Gemini 1.5 Pro (Google)"),
    ]

    initial_solutions = {}
    solution_gen_tasks = [f"Generating solution from {display_name}" for _, _, display_name in democratic_models]
    print(f"{YELLOW}💡 --- Generating Initial Solutions from Democratic Models --- 💡{RESET_COLOR}")
    progress_bar = tqdm(solution_gen_tasks, desc="Generating Initial Solutions", unit="task", leave=False)

    for api_type, model_name, display_name in democratic_models:
        progress_bar.set_description(f"Solution from {display_name}")
        print() # Gap
        print(f"{CYAN}✍️  Generating solution from {display_name}...{RESET_COLOR}")
        solution = ""
        if api_type == "openai":
            solution = call_openai(model_name, user_message, general_expert_system_message)
        elif api_type == "mistral":
            solution = call_mistral(model_name, user_message, general_expert_system_message)
        elif api_type == "gemini":
            solution = call_gemini(model_name, user_message, general_expert_system_message)
        initial_solutions[display_name] = solution
        print(f"{NEON_GREEN}📄 Solution from {display_name}:{RESET_COLOR}\n{solution[:300] + '...' if len(solution) > 300 else solution}")
        print() # Gap
        print(f"{PINK}------------------------------------------------------------------------------------------------{RESET_COLOR}")
        progress_bar.update()
    progress_bar.close()
    print(f"\n{NEON_GREEN}✅ --- All Initial Solutions Generated --- ✅{RESET_COLOR}\n")

    solution_options_str = "\n\n".join(f"Solution Option from {name}:\n{solution_text}" for name, solution_text in initial_solutions.items())
    print(f"{YELLOW}🗳️ --- Preparing for Voting Phase --- 🗳️{RESET_COLOR}")
    print(f"{CYAN}📜 Solution options presented to voters:{RESET_COLOR}\n{solution_options_str[:500] + '...' if len(solution_options_str) > 500 else solution_options_str}\n")
    
    voting_prompt = (f"Review the following SOLUTION OPTIONS provided by different AI advisors to address the PROBLEM. Your task is to VOTE for the single best solution option.\n\nPROBLEM:\n{user_message}\n\nSOLUTION OPTIONS:\n{solution_options_str}\n\nBased on your expert analysis, which of the above solution options (e.g., 'Solution Option from GPT-4o mini (OpenAI)') is the best? State your chosen option clearly.")

    votes = {}
    voting_tasks = [f"Collecting vote from {display_name}" for _, _, display_name in democratic_models]
    print(f"{YELLOW}📮 --- Collecting Votes from Democratic Models --- 📮{RESET_COLOR}")
    progress_bar = tqdm(voting_tasks, desc="Collecting Votes", unit="task", leave=False)
    
    for api_type, model_name, display_name in democratic_models:
        progress_bar.set_description(f"Vote from {display_name}")
        print() # Gap
        print(f"{CYAN}🙋  Collecting vote from {display_name}...{RESET_COLOR}")
        vote = ""
        voter_system_prompt = "You are an AI expert evaluating solutions. Pick the best one from the options provided."
        if api_type == "openai":
            vote = call_openai(model_name, voting_prompt, voter_system_prompt)
        elif api_type == "mistral":
            vote = call_mistral(model_name, voting_prompt, voter_system_prompt)
        elif api_type == "gemini":
            vote = call_gemini(model_name, voting_prompt, voter_system_prompt) 
        votes[display_name] = vote
        print(f"{NEON_GREEN}👍 Vote from {display_name}:{RESET_COLOR}\n{vote[:300] + '...' if len(vote) > 300 else vote}")
        print() # Gap
        print(f"{PINK}------------------------------------------------------------------------------------------------{RESET_COLOR}")
        progress_bar.update()
    progress_bar.close()
    print(f"\n{NEON_GREEN}✅ --- All Votes Collected --- ✅{RESET_COLOR}\n")

    all_votes_str = "\n\n".join(f"Vote from {voter_name}:\n{vote_text}" for voter_name, vote_text in votes.items())
    print(f"{YELLOW}📊 --- Counting Votes --- 📊{RESET_COLOR}")
    print(f"{CYAN}📜 All votes cast:{RESET_COLOR}\n{all_votes_str[:500] + '...' if len(all_votes_str) > 500 else all_votes_str}\n")
    
    vote_counter_model_type = "openai"
    vote_counter_model_name = "gpt-4o" 

    progress_bar = tqdm(total=1, desc=f"🗣️ Counting Votes with {vote_counter_model_name}", unit="task", leave=True) # leave=True for final bar
    
    final_count_prompt = (f"The following solutions were proposed for the problem: '{user_message}'.\\n\\nPROPOSED SOLUTIONS:\\n{solution_options_str}\\n\\nSubsequently, AI advisors cast their votes for the best solution. Here are their votes:\\n\\nVOTES CAST:\\n{all_votes_str}\\n\\nBased on these votes, please determine which solution received the most votes. Clearly state the winning solution's text and the number of votes it received. If there is a tie, list all tied solutions and their vote counts.")
    
    final_answer = ""
    if vote_counter_model_type == "openai":
        final_answer = call_openai(vote_counter_model_name, final_count_prompt, vote_counting_system_message)
    elif vote_counter_model_type == "mistral":
        final_answer = call_mistral(vote_counter_model_name, final_count_prompt, vote_counting_system_message)
    elif vote_counter_model_type == "gemini":
        final_answer = call_gemini(vote_counter_model_name, final_count_prompt, vote_counting_system_message)

    progress_bar.update()
    progress_bar.close()
    print(f"\n{NEON_GREEN}🏆 --- Final Result from The Democracy --- 🏆{RESET_COLOR}")
    print(f"{YELLOW}🌟 Winning Solution/Outcome:{RESET_COLOR}\n{final_answer}")
    return final_answer

question = open_file("problem.txt")
html_response1 = the_democracy(question)
generate_html_response(html_response1, "Democracy")
