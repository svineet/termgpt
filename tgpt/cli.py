import argparse
import os
import subprocess
import re

from tgpt.plugins.plugin_manager import PluginManager
from tgpt.prompts import SYSTEM_PROMPT
from tgpt.gpt import GPTWrapper
from tgpt.agent import get_default_agent


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")


INTRODUCTION = """

▗▄▄▄▖▗▄▄▖▗▄▄▖▗▄▄▄▖
  █ ▐▌   ▐▌ ▐▌ █  
  █ ▐▌▝▜▌▐▛▀▘  █  
  █ ▝▚▄▞▘▐▌    █  
                  

Welcome to TermGPT: Terminal AI Agent
"""


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
    matches = re.findall(r"<bash>(.*?)</bash>", response, re.DOTALL)
    if matches:
        for command in matches:
            command = command.strip()
            print(f"CMD: {command}")

            # Ask for confirmation to execute the command
            execute = input("Execute? (Y/n): ").strip().lower()
            if execute in ("", "y", "yes"):
                output = execute_command(command)
                gpt_client.add_post_execution_context(command=command, output=output)
                print(output)

    return response


def start_chat_mode():
    print(INTRODUCTION)
    gpt_client = GPTWrapper(api_key=OPENAI_API_KEY, system_prompt=SYSTEM_PROMPT)

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            print("Exiting chat mode.")
            break

        process_input(gpt_client, user_input)


def start_agent_mode():
    print(INTRODUCTION)

    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    if not TAVILY_API_KEY:
        raise EnvironmentError("TAVILY_API_KEY not found in environment variables.")

    agent = get_default_agent(OPENAI_API_KEY)
    agent.start()

    # Optionally, print token usage stats
    token_usage = agent.get_token_usage()
    print(f"Total input tokens: {token_usage['total_input_tokens']}")
    print(f"Total output tokens: {token_usage['total_output_tokens']}")


def main():
    parser = argparse.ArgumentParser(description="tgpt: terminal AI agent")
    parser.add_argument("-p", "--prompt", nargs="*", help="Enable prompt mode with natural language prompt")

    args = parser.parse_args()

    if args.prompt is not None:
        prompt = " ".join(args.prompt)
        agent = get_default_agent(OPENAI_API_KEY)
        agent.start(one_off_prompt=prompt)
    else:
        start_agent_mode()

if __name__ == "__main__":
    main()
