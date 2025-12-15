import os
import click
import questionary

import re

WA_RE_PATTERN = re.compile(r"^\[\d{4}-\d{2}-\d{2},\s\d{2}:\d{2}:\d{2}\]\s([^:]+):")


@click.command()
@click.option(
    "--input-file",
    required=True,
    help="Path to the input WA chat file.",
)
def parse_conversations(input_file: str) -> dict:
    """
    Parse raw chat conversations from a file and group them into structured format.
    """

    cleaned_conversation = []
    names = []
    dataset = []

    # Read raw conversations from file
    if os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as file:
            raw_conversations = file.readlines()
    else:
        click.echo(f"Path '{input_file}' does not exist.")
        exit(1)

    click.echo(f"Read {len(raw_conversations)} lines from {input_file}")

    # Get Names
    for conv in raw_conversations:
        match = WA_RE_PATTERN.match(conv)
        if match:
            names.append(match.group(1))
            cleaned_conversation.append(conv)  # Also get the clean convos

    selected_name = questionary.select("What is your name?", choices=set(names)).ask()

    parsed_conversations = [
        {
            "role": "assistant" if selected_name in conv else "user",
            "content": conv.split(":", 3)[
                -1
            ].strip(),  # Extract content after the third colon
        }
        for conv in cleaned_conversation
    ]

    current_conversation = []

    for conv in parsed_conversations:
        if (
            conv["role"] == "user" and current_conversation[-1]["role"] != "user"
            if current_conversation
            else True
        ):
            dataset.append(current_conversation)
            current_conversation = [conv]
        else:
            current_conversation.append(conv)

    if current_conversation:
        dataset.append(current_conversation)

    click.echo(f"Grouped into {len(dataset)} conversations.")

    with open("parsed_conversations.jsonl", "w", encoding="utf-8") as outfile:
        for line in dataset[1:]:
            outfile.write(f"{line}\n")

    click.echo("Parsed conversations saved as parsed_conversations.jsonl ✅")
