#!/usr/bin/env python3
import sys
import os
import argparse

import pdb

from colorama import Fore, Style
import pyperclip

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

import openai

from ascii_assets import bollingen_logo, logo

from prompt_lib import prompt_catalog


class Config:
    model_engine = "text-davinci-003"
    max_tokens = 2*1024
    temperature = 0.5
    max_p = 1

config = Config()

completer = WordCompleter([
    '/copy', '/inspect', '/help', '/context'
], ignore_case=True)


class GPT3:
    def __init__(self, config):
        self.config = config

    def set_config(self, conf):
        self.config = conf

    def query(self, prompt):
        config = self.config
        completion = openai.Completion.create(
            model=config.model_engine,
            prompt=prompt,
            temperature=config.temperature,
            max_tokens=config.max_tokens)
        
        return completion
    
    def query_via_prompt_format(self, prompt, format):
        pass


def main(args, argparser):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not args.prompt:
        # Start interactive prompting session

        print(Fore.LIGHTYELLOW_EX + logo + Style.RESET_ALL)
        print()

        completion = ""
        context = ""
        summarised_ctx_mode = False
        ctx_mode = False
        prompt_sesh = PromptSession()
        gpt3 = GPT3(config)

        while True:
            prompt = prompt_sesh.prompt(ANSI(Fore.GREEN + ">>> "),
                                        completer=completer,
                                        auto_suggest=AutoSuggestFromHistory())
            print(Style.RESET_ALL)

            if prompt == '/inspect':
                print()
                print(Fore.RED + "Entering inspect mode" + Style.RESET_ALL)
                print()

                pdb.set_trace()

                continue
            elif prompt == "/copy":
                if completion != "":
                    pyperclip.copy(completion["choices"][0]["text"])
                else:
                    print("Nothing to copy.")
                continue
            elif prompt == "/help":
                argparser.print_help()
                print("A Bollingen Product".center(80, ' '))
                print(bollingen_logo)
                continue
            elif prompt.startswith('/context'):
                opt = prompt.split(' ')[-1]
                if opt == "on":
                    ctx_mode = True
                elif opt == "off":
                    ctx_mode = False
                print("Context mode: %s" % ctx_mode)
                continue
            elif prompt == "/summarised-context":
                summarised_ctx_mode = not summarised_ctx_mode
                print("Summarised context: %s" % summarised_ctx_mode)

            # TODO: Add config editing from here
            # TODO: Add config file option

            try:
                fin_prompt = prompt
                if ctx_mode:
                    fin_prompt = context + "\n" + prompt

                completion = gpt3.query(fin_prompt)
                print(completion["choices"][0]["text"].strip())

                compl_text = completion["choices"][0]["text"].strip()

                if summarised_ctx_mode:
                    # Summarise the above completion using 'tl;dr:' prompt and add to context.
                    # This saves some tokens, but misses a lot of context.
                    completion = gpt3.query(compl_text + "\ntl;dr: ")

                context += completion["choices"][0]["text"].strip()
            except Exception as error:
                print('we dun fked up bro')
                print(error)
    else:
        # Just use the concatenated args as prompt
        try:
            completion = openai.Completion.create(
                model=config.model_engine,
                prompt=args.prompt,
                temperature=config.temperature,
                max_tokens=config.max_tokens)

            print(completion["choices"][0]["text"])
        except Exception as error:
            print(error)
            sys.exit(1)


def modify_config(args):
    if args.temperature:
        config.temperature = args.temperature

    if args.max_p:
        config.max_p = args.max_p

    if args.max_tokens:
        config.max_tokens = args.max_tokens



if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="TermGPT",
        description="Terminal frontend for GPT3.5",
        epilog="Make sure that OPENAI_API_KEY is defined as an environment variable."
    )

    argparser.add_argument("--prompt", "-p", action="store")

    argparser.add_argument("--temperature", "-t", action="store")
    argparser.add_argument("--max-tokens", action="store")
    argparser.add_argument("--max-p", action="store")
    argparser.add_argument("--model-engine", "-m", action="store")

    args = argparser.parse_args()

    modify_config(args)
    main(args, argparser)

