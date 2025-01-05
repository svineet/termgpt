# TermGPT: Terminal AI Agent

**TermGPT** is a general Terminal AI Agent, that can search the web and execute commands from natural language instructions. It is powered by the OpenAI API, and also functions as a generic ChatGPT interface from the terminal.

## Features

- Convert natural language into Bash commands.
- Search the web, and incorporate those details into relevant bash commands, or just ask for the weather.
- Execute commands interactively in chat mode.

## Installation

### Prerequisites

- Python 3.8 or later
- A valid OpenAI API key
- A valid Tavily API key

### Setting Up the Environment

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/svineet/termgpt.git
   cd tgpt
   ```

2. **Install the Package:**

   Using pip:
   ```bash
   python3 -m pip install .
   ```

   Or, using pipx for isolation:
   ```bash
   pipx install .
   ```

3. **Set Up API Keys:**

   Export your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

   Export your Tavily search API key as an environment variable:
   ```bash
   export TAVILY_API_KEY="your-tavily-api-key"
   ```

4. **Run the Tool:**

   Agent chat mode:
   ```bash
   tgpt
   ```

   Prompt mode:
   ```bash
   tgpt -p "List all Python files in the current directory"
   ```

   To exit agent mode, type `exit`.
