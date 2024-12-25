# TGPT: Natural Language to Bash Command Tool

**TGPT** is a command-line tool that converts natural language prompts into Bash commands. It integrates with OpenAI's API and provides extensibility through a plugin system.

---

## Features

- Convert natural language to Bash commands.
- Execute or refine commands in an interactive chat mode.
- Extend functionality via plugins (e.g., `@web` for internet searches).

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

2. **Install Dependencies:**

   Using pip:
   ```bash
   python3 -m pip install -r requirements.txt
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
   tgpt "List all Python files in the current directory"
   ```

   Chat mode:
   ```bash
   tgpt -c
   ```
