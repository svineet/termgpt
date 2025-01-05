# To-do and Ideas

## Initial Steps
- Develop a CLI assistant that constructs and executes commands on your behalf, while maintaining the context of the conversation, by generating bash commands
- Enable the assistant to perform tasks autonomously: plan and execute command's on user's behalf

## Features that can be implemented

## More sophisticated prompting regime
- Currently we use LangGraph's default ReAct agent. It doesn't plan. Use planning and self reflection instead.
- Maybe even roll our own agent framework instead of having to engage with langgraph.

### Slash Commands
- Implement slash commands for:
  - Model configuration
  - Direct `/bash` command execution
  - Help documentation

### User Interface Enhancements
- Integrate `prompt_toolkit` for an improved UI experience and autocomplete functionality.
- Add autocomplete powered by a lightweight language model or an alternative fuzzy finding method.
- Make sure colours and other bash features are retained with subprocess, and handle `sudo`

### Voice Input
- Enable voice input functionality with the `/voice` command.

## Future Developments
- Enhance the assistant to plan actions, build code repositories, and operate the computer, evolving into a comprehensive AI agent.

### Long-Term Memory
- Implement long-term memory capabilities with commands like `show memory`.
- Introduce a `<memory>` tag to store and recall memories for long-term retention.

### Additional Tools
- Instead of using bash as a catch-all tool for manipulating the whole system, maybe more fine-grained tools 
could work better
- Add tools like GMail and GCalendar integrations, using Composio

### Agent Mesh Deployment
- Implement the capability to deploy autonomous agents, that `tgpt` writes itself.
- A default network of subagents

### Add type hints everywhere (make tgpt itself do it?)
