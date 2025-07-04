<div align="center">
  🚩🧡🕉️ || जय श्री राम || 🕉️🧡🚩
</div>

---

<h1 align="center" id="top">Mixture of Idiots 🤪🧠💥</h1>

<p align="center">
  <strong>Sometimes, a team of "idiots" can be surprisingly brilliant!</strong>
</p>

Welcome to **Mixture of Idiots (MoI)**, a project exploring how combining multiple Large Language Models (LLMs)—each with its own quirks and strengths—can lead to more robust, nuanced, and intelligent solutions than any single "genius" model might produce on its own. This is an implementation of a "Mixture of Models (MOM)" system.

## 📜 Table of Contents

1.  [🤔 The Core Idea: Strength in Imperfect Numbers](#core-idea)
2.  [📂 Project Structure](#project-structure)
3.  [🏛️ Architectures Explored](#architectures-explored)
    *   [👑 The King Architecture](#king-architecture)
    *   [🤝 The Duopoly Architecture](#duopoly-architecture)
    *   [🗳️ The Democracy Architecture](#democracy-architecture)
4.  [🛠️ Tech Stack](#tech-stack)
5.  [🚀 Getting Started](#getting-started)
    *   [1. Prerequisites](#prerequisites)
    *   [2. Clone the Repository](#clone-repository)
    *   [3. Set Up a Virtual Environment (Recommended)](#set-up-virtual-environment)
    *   [4. Install Dependencies](#install-dependencies)
    *   [5. Configure API Keys 🔑](#configure-api-keys)
6.  [🏃 How to Run](#how-to-run)
    *   [1. Prepare Your Problem](#prepare-problem)
    *   [2. Execute an Architecture Script](#execute-script)
    *   [3. View the Output](#view-output)
7.  [✨ Example Output](#example-output)
8.  [🔮 Future Ideas & Enhancements](#future-ideas)
9.  [🤝 Contributing](#contributing)

---

<h2 id="core-idea">🤔 The Core Idea: Strength in Imperfect Numbers</h2>

The premise is simple: LLMs, while powerful, aren't perfect. They can hallucinate, miss nuances, or approach problems from a limited perspective. Instead of relying on one, MoI orchestrates a team of diverse AI models. Each "idiot" in the "mixture" contributes its perspective, and through structured collaboration, debate, or democratic processes, we aim to distill a collectively wiser output.

<h2 id="project-structure">📂 Project Structure</h2>

A typical folder structure for this project might look like:

```
Mixture-of-Idiots/
├── .env                      # Your local environment variables (GITIGNORED!)
├── .env.template             # Template for environment variables
├── .gitignore                # Specifies intentionally untracked files
├── README.md                 # This file!
├── requirements.txt          # Python package dependencies
├── problem.txt               # Input file for the problem/question
├── king_architecture.py      # Script for the King architecture
├── duopoly_architecture.py   # Script for the Duopoly architecture
├── democracy_architecture.py # Script for the Democracy architecture
└── utils.py                  # Optional: For shared helper functions (e.g., API calls)
```

<h2 id="architectures-explored">🏛️ Architectures Explored</h2>

We're experimenting with several architectures to harness this collective (potential) idiocy. 

**(Note: The text-based diagrams below are illustrative. For more polished graphical diagrams, consider creating them with a tool like draw.io or Lucidchart and embedding them as images.)**

---

<h3 id="king-architecture">👑 The King Architecture</h3>

*   **Concept:** A "King" AI model makes the final decision after consulting a diverse council of "Advisor" AI models. It's a hierarchical approach where specialized advice informs a central, authoritative decision-maker.
*   **Visual Workflow (Illustrative Text):**
    ```
    +----------------+     +-----------------+     +----------------------+
    |  User Problem  | --> | Advisor Model 1 | --> |       Advice 1       |
    +----------------+     +-----------------+     +----------------------+
           |
           |               +-----------------+     +----------------------+
           +-------------> | Advisor Model 2 | --> |       Advice 2       |
           |               +-----------------+     +----------------------+
           |
           |                   ... (N Advisors) ...
           |
           |               +-----------------+     +----------------------+
           +-------------> | Advisor Model N | --> |       Advice N       |
                           +-----------------+     +----------------------+
                                      |
                                      V
                           +----------------------+
                           |   All Advice         |
                           |   Compiled           |
                           +----------------------+
                                      |
                                      V
                           +-------------------------+
                           |      👑 King Model      |
                           | (with Problem & Advice) |
                           +-------------------------+
                                      |
                                      V
                           +----------------------+
                           |   Final Solution ✨  |
                           +----------------------+
    ```
*   **How it Works:**
    1.  📥 **Problem Input:** The user provides a problem or question.
    2.  🧠 **Advisor Consultation:** Multiple "Advisor" models (from OpenAI, Mistral, Gemini) independently analyze the problem and generate their individual advice or solutions.
    3.  📜 **Advice Compilation:** All pieces of advice are gathered.
    4.  👑 **The King's Decree:** A powerful "King" model (e.g., GPT-4o) receives the original problem *and* all the advisors' inputs.
    5.  💡 **Final Solution:** The King model synthesizes this wealth of information to produce a single, comprehensive, and hopefully more refined final solution.

---

<h3 id="duopoly-architecture">🤝 The Duopoly Architecture</h3>

*   **Concept:** Two primary "Oracle" AI models engage in a multi-turn debate and discussion, much like two experts arguing a case. Their dialogue is informed by initial insights from other "Advisor" models. A "Summarizer" model then distills their rich conversation into a final answer.
*   **Visual Workflow (Illustrative Text):**
    ```
    +----------------+     +--------------------------+     +-----------------------+
    |  User Problem  | --> |  Initial Advisors (Pool) | --> |  Insights Summary     |
    +----------------+     +--------------------------+     +-----------------------+
                                                                  |
                                                                  V
                                              +--------------------------------------+
                                              |      🗣️ Oracle 1 (e.g., OpenAI)      |
                                              +--------------------------------------+
                                                           ^      |
                                                           |      | Discussion Turn 1
                                               (Responds)  |      V (Receives & Responds)
                                              +--------------------------------------+
                                              |      🗣️ Oracle 2 (e.g., Mistral)     |
                                              +--------------------------------------+
                                                           ^      |
                                                           |      | Discussion Turn 2
                                                           ... (N Turns) ...
                                                           ^      |
                                                           |      | Discussion Turn N
                                              +--------------------------------------+
                                              |      Full Conversation Record        |
                                              +--------------------------------------+
                                                           |
                                                           V
                                              +--------------------------------------+
                                              |      📜 Summarizer Model             |
                                              +--------------------------------------+
                                                           |
                                                           V
                                              +--------------------------------------+
                                              |         Final Solution ✨            |
                                              +--------------------------------------+
    ```
*   **How it Works:**
    1.  📥 **Problem Input:** The user submits a problem.
    2.  🧐 **Initial Insights:** A set of "Advisor" models provide quick, initial perspectives on the problem.
    3.  🗣️ **Oracle Designation:** Two main "Oracle" models (e.g., one from OpenAI, one from Mistral/Gemini) are chosen to lead the discussion.
    4.  💬 **Discussion Kick-off:** The Oracles receive the problem and the initial advisor insights.
    5.  🔄 **Iterative Debate:** The Oracles engage in a series of conversational turns. They challenge each other's points, build on ideas, and explore the problem from different angles.
    6.  📝 **Record Keeping:** Their entire discussion is logged.
    7.  💡 **Synthesized Conclusion:** A "Summarizer" model reviews the full conversation and the original problem to extract and present a final, synthesized answer that ideally captures the best of the debate.

---

<h3 id="democracy-architecture">🗳️ The Democracy Architecture</h3>

*   **Concept:** A pool of diverse AI models first independently propose solutions to a problem. Then, the same (or another) pool of models votes on these proposed solutions. The solution that garners the most votes is declared the winner. Power to the AI people!
*   **Visual Workflow (Illustrative Text):**
    ```
    +----------------+     +-----------------------+     +--------------------+
    |  User Problem  | --> | Democratic Model A    | --> |     Solution 1     |
    +----------------+     +-----------------------+     +--------------------+
           |
           |               +-----------------------+     +--------------------+
           +-------------> | Democratic Model B    | --> |     Solution 2     |
           |               +-----------------------+     +--------------------+
           |
           |                   ... (N Solution Generators) ...
           |
           |               +-----------------------+     +--------------------+
           +-------------> | Democratic Model Z    | --> |     Solution N     |
                           +-----------------------+     +--------------------+
                                      |
                                      V
                           +-----------------------------------------+
                           |      Solution Options Pool (Ballot) 📜  |
                           +-----------------------------------------+
                                      |
                                      +----------------------------------------------------+
                                      | (Presented with Problem & All Solution Options)    |
                                      V                                                    V
    +-----------------------+     +-----------------------+          +-----------------------+     +-----------------------+
    |   Voting Model A      | --> |        Vote A         |          |   Voting Model Z      | --> |        Vote Z         |
    +-----------------------+     +-----------------------+          +-----------------------+     +-----------------------+
                 |                   ... (N Voters) ...                   |
                 +--------------------------------------------------------+
                                      |
                                      V
                           +---------------------------------------+
                           |  🗳️ Vote Aggregation / Counter Model  |
                           +---------------------------------------+
                                      |
                                      V
                           +------------------------------------+
                           |      🏆 Winning Solution ✨       |
                           +------------------------------------+
    ```
*   **How it Works:**
    1.  📥 **Problem Input:** The user presents a problem.
    2.  ✍️ **Solution Generation:** A diverse set of "Democratic Models" each independently generate a complete solution to the problem.
    3.  📜 **Ballot Creation:** All generated solution options are collected, forming a "ballot."
    4.  🙋 **Casting Votes:** The same (or a different set of) models are then presented with the original problem and all the solution options from the ballot. Each model "votes" for what it considers the best solution.
    5.  📊 **Vote Tallying:** The votes are collected.
    6.  🏆 **Declaring the Winner:** A "Vote Counter" model (or simple aggregation logic) tallies the votes to determine the winning solution. If there's a tie, it might be noted or handled by a tie-breaking rule (not explicitly implemented yet).

---

<h2 id="tech-stack">🛠️ Tech Stack</h2>

*   **Python 3.x**
*   LLM APIs:
    *   OpenAI
    *   MistralAI
    *   Google Gemini
*   Libraries: `openai`, `mistralai`, `google-generativeai`, `python-dotenv`, `tqdm`, `markdown`

<h2 id="getting-started">🚀 Getting Started</h2>

Follow these steps to get the Mixture of Idiots running on your local machine.

<h3 id="prerequisites">1. Prerequisites</h3>

*   Python 3.8 or higher.
*   Access to API keys for OpenAI, MistralAI, and Google Gemini.

<h3 id="clone-repository">2. Clone the Repository</h3>

```bash
git clone https://github.com/VinsmokeSomya/Mixture-of-Idiots.git
cd Mixture-of-Idiots
```

<h3 id="set-up-virtual-environment">3. Set Up a Virtual Environment (Recommended)</h3>

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

<h3 id="install-dependencies">4. Install Dependencies</h3>

```bash
pip install -r requirements.txt
```

<h3 id="configure-api-keys">5. Configure API Keys 🔑</h3>

1.  Make a copy of the `.env.template` file and name it `.env`.
    ```bash
    # On Windows
    copy .env.template .env
    # On macOS/Linux
    cp .env.template .env
    ```
2.  Open the `.env` file and replace the placeholder values with your actual API keys:
    ```env
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
    MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY_HERE
    ```
    **Important:** The `.env` file is listed in `.gitignore`, so your secret keys will not be committed to the repository.

<h2 id="how-to-run">🏃 How to Run</h2>

<h3 id="prepare-problem">1. Prepare Your Problem</h3>

Create a file named `problem.txt` in the root directory of the project. Write the problem or question you want the MoI system to solve inside this file.

<h3 id="execute-script">2. Execute an Architecture Script</h3>

Open your terminal (with the virtual environment activated) and run one of the architecture scripts:

*   **King Architecture:**
    ```bash
    python king_architecture.py
    ```
*   **Duopoly Architecture:**
    ```bash
    python duopoly_architecture.py
    ```
*   **Democracy Architecture:**
    ```bash
    python democracy_architecture.py
    ```

<h3 id="view-output">3. View the Output</h3>

*   **Console:** The script will print verbose logs to the console, showing the step-by-step process, including individual model contributions, with colors and emojis for better readability.
*   **HTML Report:** After the script finishes, an HTML file will be automatically generated and opened in your default web browser. This report presents the final solution in a clean, modern format, indicating which MoI architecture was used.

<h2 id="example-output">✨ Example Output</h2>

The HTML report provides a nicely formatted view of the final solution, making it easy to read and share. It looks something like this (but with your actual results!):

*(Imagine a screenshot of your cool HTML output here! Since I can't generate images, you might want to add one later.)*

The report clearly states it's from the "Mixture of Models (MOM) system" and specifies the architecture (e.g., King, Duopoly, Democracy) that generated the result.

<h2 id="future-ideas">🔮 Future Ideas & Enhancements</h2>

*   More sophisticated vote-counting and tie-breaking in Democracy.
*   Dynamic model selection based on problem type.
*   Web interface for easier interaction.
*   More complex conversational patterns for Duopoly.
*   Error handling for individual model failures within a run.

<h2 id="contributing">🤝 Contributing</h2>

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/VinsmokeSomya/Mixture-of-Idiots/issues) if you want to contribute.

---

Let the smartest idiot win! 🎉
