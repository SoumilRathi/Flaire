import re
import anthropic

client = anthropic.Anthropic(api_key="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")


def sort_actions_by_priority(actions):
        actions_with_priorities = []
        
        for action in actions:
            # Use regex to extract the number at the end of the action, if it exists
            match = re.search(r'(\d+)', action)
            if match:
                priority = int(match.group(1))
                actions_with_priorities.append((action, priority))
        
        # Sort actions based on the numerical values in descending order
        sorted_actions = sorted(actions_with_priorities, key=lambda x: x[1], reverse=True)
        
        # Return the action with the highest priority if available
        return sorted_actions[0][0] if sorted_actions else None


def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

actions_instructions = load_file("actions.txt")

def use_claude(user_prompt, system_prompt=None, temperature=0, json=False):
    message_params = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 2048,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}]
            }
        ]
    }
    
    if system_prompt is not None:
        message_params["system"] = system_prompt
    
    message = client.messages.create(**message_params)


    return message.content[0].text
