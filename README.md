# TGPT: Natural Language to Bash Command Tool

**TGPT** is a command-line tool designed to transform natural language prompts into Bash commands. It leverages OpenAI's API and offers extensibility through a robust plugin system.

---

## Features

- Seamlessly convert natural language into Bash commands.
- Execute commands interactively in a chat mode.
- Enhance functionality with plugins (e.g., `@web` for internet searches).

---

## Installation

### Prerequisites

- Python 3.8 or later
- A valid OpenAI API key

### Setting Up the Environment

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/tgpt.git
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

3. **Set Up OpenAI API Key:**

   Export your API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

4. **Run the Tool:**

   Direct mode:
   ```bash
   tgpt -p "List all Python files in the current directory"
   ```

   Chat mode:
   ```bash
   tgpt
   ```

   To exit chat mode, type `exit`.

---

