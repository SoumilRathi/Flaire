import re
import anthropic
import base64

import os
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


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

def process_images(images):
    processed_images = []
    for image_data in images:
        image = image_data['image']
        text = image_data['text']
        if image.startswith('data:image/'):
            image_type, image_data = image.split(',', 1)
            media_type = image_type.split(';')[0].split(':')[1]
            processed_images.append({
                "image": {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    }
                },
                "text": text
            })
    return processed_images

def use_claude(user_prompt, system_prompt=None, temperature=1, json=False, tools=[], images=[]):
    message_params = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 8192,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": []
            }
        ]
    }
    
    if system_prompt is not None:
        message_params["system"] = system_prompt

    if tools is not None and len(tools) > 0:
        message_params["tools"] = tools

    content = []
    if images:
        processed_images = process_images(images)
        for i, image_data in enumerate(processed_images):
            content.append(image_data["image"])
            if image_data["text"]:
                content.append({"type": "text", "text": f"Description for Image {i+1}: {image_data['text']}"})

    content.append({"type": "text", "text": user_prompt})
    message_params["messages"][0]["content"] = content
    
    message = client.messages.create(**message_params)

    return message.content[0].text
# End of Selection
