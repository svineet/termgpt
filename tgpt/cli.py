import argparse
import os
import subprocess
from tgpt.plugins.plugin_manager import PluginManager
from tgpt.gpt import GPTWrapper


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = None
prompt_file_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
if os.path.exists(prompt_file_path):
    with open(prompt_file_path, "r") as file:
        SYSTEM_PROMPT = file.read().strip()


def execute_command(command):
    print(f"Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


def process_input(gpt_client, prompt):
    for tag, plugin in PluginManager.get_plugins().items():
        if tag in prompt:
            context = {}
            return plugin.run(prompt, context)

    # Use GPTWrapper to generate a command from the prompt
    return gpt_client.send_with_log(prompt)


def start_chat_mode():
    print("Chat mode enabled. Type 'exit' to quit.")
    gpt_client = GPTWrapper(api_key=OPENAI_API_KEY, system_prompt=SYSTEM_PROMPT)

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            print("Exiting chat mode.")
            break

        result = process_input(gpt_client, user_input)

        print(f"Generated Command: {result}")
        execute = input("Execute this command? (y/n): ").strip().lower()
        if execute == "y":
            output = execute_command(result)
            print(output)


def main():
    parser = argparse.ArgumentParser(description="tgpt: Natural language to bash command tool")
    parser.add_argument("prompt", nargs="*", help="Natural language prompt")
    parser.add_argument("-c", "--chat", action="store_true", help="Enable chat mode")

    args = parser.parse_args()
    PluginManager.load_plugins()

    if args.chat:
        start_chat_mode()
    elif args.prompt:
        prompt = " ".join(args.prompt)
        result = process_input(prompt)
        print(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
