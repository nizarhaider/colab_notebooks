# WhatsApp Chat Parser

A Python utility to parse WhatsApp chat exports and convert them into a structured format suitable for fine-tuning language models.

## Overview

This tool reads raw WhatsApp chat files, extracts conversations, and transforms them into a conversation format where messages are labeled as either "user" or "assistant" based on who sent them. The output is saved as a JSONL file for easy processing in machine learning pipelines.

## Features

- 📱 Parses WhatsApp chat exports
- 🔍 Extracts participant names automatically
- 👤 Filters conversations by selected participant
- 📊 Groups messages into conversation threads
- 💾 Exports to JSONL format

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Getting Started

Simply run:

```bash
uv run parse_conv --input-file ~/Downloads/chat.txt
```

`uv` will automatically install dependencies and execute the command.

#### Interactive Prompt

The tool will ask you to select your name from the list of participants:

```
What is your name?
❯ Alice
  Bob
  Charlie
```

#### Output

The script generates a `parsed_conversations.jsonl` file in your current directory containing structured conversations:

```json
[{"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hi there!"}]
[{"role": "user", "content": "How are you?"}, {"role": "assistant", "content": "I'm doing great!"}]
```

## Chat Export Format

Your WhatsApp chat file should be in the standard export format:

```
[2024-12-15, 14:30:45] Alice: Hello
[2024-12-15, 14:31:12] Bob: Hi Alice!
[2024-12-15, 14:31:45] Alice: How are you?
[2024-12-15, 14:32:10] Bob: I'm great, thanks!
```

## Python Terminal Usage

If you prefer to work in a Python interactive session:

```python
import os
from main import parse_conversations

# Using expanduser for ~ paths
path = os.path.expanduser("~/Downloads/chat.txt")

# Or use absolute path
path = "/Users/nizar/Downloads/chat.txt"

with open(path, "r", encoding="utf-8") as file:
    content = file.readlines()

print(f"Loaded {len(content)} lines")
```

## Project Structure

```
Finetuning - Data Preparation/
├── main.py                    # Main parser script
├── pyproject.toml            # Project configuration
└── parsed_conversations.jsonl # Output file (generated)
```

## Notes

- The script skips the first conversation in the output by design: `dataset[1:]`
- Messages are grouped so that consecutive messages from the same sender are in the same conversation
- The output JSONL format is compatible with OpenAI's fine-tuning API
