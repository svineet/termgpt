import argparse
import os
import subprocess
import re
from tgpt.plugins.plugin_manager import PluginManager
from tgpt.prompts import SYSTEM_PROMPT
from tgpt.gpt import GPTWrapper


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


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

    # LLM Call
    response = gpt_client.send_with_log(prompt)
    print (response)
    
    # Check for <bash> tags in the response, and if to execute
    match = re.search(r"<bash>(.*?)</bash>", response, re.DOTALL)
    if match:
        command = match.group(1).strip()
        print(f"Detected Command: {command}")

        # Ask for confirmation to execute the command
        execute = input("Execute this command? (Y/n): ").strip().lower()
        if execute in ("", "y", "yes"):
            output = execute_command(command)
            print(output)
    else:
        print("No command detected in the response.")

    return response



def start_chat_mode():
    print("Chat mode enabled. Type 'exit' to quit.")
    print(SYSTEM_PROMPT)
    gpt_client = GPTWrapper(api_key=OPENAI_API_KEY, system_prompt=SYSTEM_PROMPT)

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            print("Exiting chat mode.")
            break

        process_input(gpt_client, user_input)


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
