from .promptStrings import componentPrompt, instructionPrompt, stylePrompt
from helper_functions import use_claude

def style_code(code, css_type, user_input):
    """Styles the code based on the css_type"""

    component_prompt = componentPrompt(code)

    components = use_claude(component_prompt)

    # at some point, you'll have to convert the user input into memory


    # this is where you'll retreive the memory for similar components in the past
    memory = "";

    instruction_prompt = instructionPrompt(components, user_input, memory)

    instructions = use_claude(instruction_prompt)

    style_prompt = stylePrompt(components, instructions, code)

    response = use_claude(style_prompt)
    
    # Extract CSS code from the response
    css_start = response.find('<css>')
    css_end = response.find('</css>')
    if css_start != -1 and css_end != -1:
        css_code = response[css_start + 5:css_end].strip()
    else:
        css_code = ""  # Handle case where CSS tags are not found

    return css_code

