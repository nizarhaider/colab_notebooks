# Open file
print('Opening file...')
with open('dataset/chats.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

print(f'Total lines read: {len(lines)}')


def parse_conversation(line: str) -> dict[str, str]:
    """
    Parse a single conversation of WA chat.
    """

    parsed_conversation = {
        "role": "assistant" if "Nizu" in line else "user",
        "content": line.split(":", 3)[-1].strip()
    }
    return parsed_conversation


def group_conversations(parsed_conversation: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    """
    Transform conversations from flat dicts to nested lists of dicts:
    {'role': 'user', 'content': 'lol'}
    {'role': 'assistant', 'content': 'whassup'}

    to:
    dataset['conversations'] = [
        [
            {'role': 'user', 'content': 'lol'},
            {'role': 'assistant', 'content': 'whassup'},
            {'role': 'user', 'content': 'hows life?'}
            {'role': 'user', 'content': 'hows life?'}
        ],
        ...
    ]
    """
    dataset = {'conversations': []}
    conversation = []

    for entry in parsed_conversation:
        if entry['role'] == 'user' and conversation[-1]['role'] != 'user' if conversation else True:
            dataset['conversations'].append(conversation)
            conversation = [entry]
        else:
            conversation.append(entry)

    if conversation:
        dataset['conversations'].append(conversation)

    return dataset

# Parse lines
parsed_conversations = [parse_conversation(line) for line in lines]
print(f'Total lines parsed: {len(parsed_conversations)}')

# Save parsed lines to JSONL file
with open('dataset/parsed_chats.jsonl', 'w', encoding='utf-8') as outfile:
    for line in parsed_conversations:
        outfile.write(f"{line}\n")
    
# Group conversations
dataset = group_conversations(parsed_conversations)
print(f'Total conversations grouped: {len(dataset["conversations"])}')

# Save grouped conversations to JSON file
with open('dataset/grouped_conversations.jsonl', 'w', encoding='utf-8') as outfile:
    for line in dataset['conversations'][1:]:
        outfile.write(f"{line}\n")
