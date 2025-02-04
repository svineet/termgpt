import os
import subprocess

from tgpt.prompts import BASH_AGENT_SYSTEM_PROMPT

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from langchain_community.tools.tavily_search import TavilySearchResults

from rich.console import Console
from rich.markdown import Markdown

from prompt_toolkit import PromptSession


DEFAULT_MODEL = "gpt-4o"

console = Console()
prompt_session = PromptSession()


@tool
def execute_bash_command(bash_command: str) -> str:
    """Executes a given bash command using the subprocess module.

    This tool takes a bash command as input, executes it in the shell, and returns
    the standard output of the command. If the command execution fails, it returns
    the error message from the standard error.

    Args:
        bash_command (str): The bash command to be executed.

    Returns:
        str: The standard output of the executed command, or an error message if
        the command fails.
    """
    console.print(f"Execute the following command? \n{bash_command}\n(Y/n): ")
    execute = prompt_session.prompt("> ").strip().lower()
    if execute not in ("", "y", "yes"):
        return "Command execution cancelled by user."
    try:
        result = subprocess.run(bash_command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


class CommandLineAgent:
    def __init__(self, llm, tools, prompt):
        self.llm = llm
        self.tools = tools
        self.system_prompt = prompt
        self.agent_executor = create_react_agent(
            self.llm, self.tools, state_modifier=self.system_prompt, checkpointer=MemorySaver()
        )
        self.total_input_tokens = 0
        self.total_output_tokens = 0


    def start(self, one_off_prompt=None):
        if one_off_prompt:
            self.process_input(one_off_prompt)
            return

        while True:
            user_input = prompt_session.prompt("> ").strip()
            if user_input.lower() == "exit":
                console.print("Exiting.")
                break

            self.process_input(user_input)

    def process_input(self, user_input):
        # Added: Check if the input is a direct bash command prefixed with "$ "
        if user_input.startswith("$ "):
            bash_command = user_input[2:].strip()
            console.print(f"Directly executing bash command: {bash_command}")
            try:
                result = subprocess.run(
                    bash_command,
                    shell=True,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                output = result.stdout.strip()
            except subprocess.CalledProcessError as e:
                output = f"Error: {e.stderr.strip()}" if e.stderr else str(e)
            console.print(output)
            return

        for chunk in self.agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}, config={"configurable": {"thread_id": "main_user_thread"}}
        ):
            if "agent" in chunk:
                agent_message = chunk["agent"]["messages"][0]
                console.print(Markdown(agent_message.content), end="")

                # Update token usage
                token_usage = agent_message.response_metadata["token_usage"]
                self.total_input_tokens += token_usage["prompt_tokens"]
                self.total_output_tokens += token_usage["completion_tokens"]
        console.print()

    def get_token_usage(self):
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
        }


def get_default_agent(OPENAI_API_KEY):
    llm = ChatOpenAI(model=DEFAULT_MODEL, api_key=OPENAI_API_KEY)
    tools = [TavilySearchResults(max_results=3), execute_bash_command]

    agent = CommandLineAgent(llm, tools, BASH_AGENT_SYSTEM_PROMPT)
    return agent


def main():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")
    if not TAVILY_API_KEY:
        raise EnvironmentError("TAVILY_API_KEY not found in environment variables.")

    agent = get_default_agent(OPENAI_API_KEY)
    agent.start()

    # Optionally, print token usage stats
    token_usage = agent.get_token_usage()
    print(f"Total input tokens: {token_usage['total_input_tokens']}")
    print(f"Total output tokens: {token_usage['total_output_tokens']}")


if __name__ == "__main__":
    main()