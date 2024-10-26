from helper_functions import use_claude

def componentPrompt(code):
    """Returns a prompt for styling the code"""
    prompt = f"""
    You are an intelligent agent specializing in frontend web development. Your task is to analyze HTML code and separate it into distinct UI components. This process is crucial for organizing and styling web pages effectively.

    Here is the HTML code you need to analyze:

    <html_code>
    {code}
    </html_code>

    Instructions:

    1. Carefully examine the provided HTML code.
    2. Identify and separate every single UI component within the code. This includes, but is not limited to:
    - Buttons
    - Input fields
    - Dropdowns
    - Select options
    - Forms
    - Navigation menus
    - Headers
    - Footers
    - Modals or popups
    - Cards or content blocks
    - Any other distinct UI elements

    3. For each identified component:
    a. Create a generalized name that could be reused across different pages of a website.
    b. Ensure the name includes any elements that would affect the component's design.
    c. Consider how the component will appear on the final rendered webpage when determining its name.
    d. Essentially, name the component based on how it will look on the final page, not based on it's functionality.
        This is because buttons will likely look the same across webpages even if one of them is a message button and another is an email button etc.
        
    4. Separate the HTML code for each component.

    5. Present your findings in the following format for each component:

    Component Name
    HTML Code for component

    Example:
    PrimaryButton
    <button class="btn btn-primary">Click me</button>

    Before providing your final output, wrap your component identification process in <component_identification> tags. In this process:

    1. Break down the overall structure of the HTML code.
    2. List each potential component you identify, numbering them sequentially.
    3. For each potential component:
    a. Quote the relevant HTML code.
    b. Explain why you consider it a separate component.
    c. Justify your chosen name for the component.

    This will ensure a thorough interpretation of the code structure and component identification.

    After your component identification process, list all the identified components with their respective HTML code in the format specified above.

    Remember: It's crucial to separate every single UI component, no matter how small, to ensure a comprehensive breakdown of the provided HTML code.
            """

    # Extract the LLM's response (the chosen action)
    return prompt;



def instructionPrompt(components, user_input, memory):
    """Returns a prompt for getting the instructions for styling the components"""

    prompt = f"""
    You are an intelligent agent specializing in frontend web development. You have been given UI components which are typically placed within a web-page. 

    These components are all part of a larger piece of code that the user has entered. 

    You have also been given some details from the user regarding how they want these UI components to look. 

    You job is to just list out these components one by one and list down directions regarding how they are supposed to look.

    Follow these guidelines to decide how to the components are supposed to look:
    1. First priority is what the user input is. If you have received user input regarding how these are supposed to look, use that to list down your directions.
    2. Second priority is your retrieved memory for similar components in the past. If you have been provided any retrieved memory, use that to decide the design for the components
    3. Final priority is internal knowledge. Base the directions on the knowledge that you have regarding how components like these are supposed to look.

    <components>
    {components}
    </components>


    <user_input>
    {user_input}
    </user_input>

    <memory>
    {memory}
    </memory>

    """

    return prompt;


def stylePrompt(components, instructions, code):
    """Returns a prompt for styling the components"""
    prompt = f"""
    You are an intelligent agent specializing in frontend web development. You have been given the html code that the user has entered.

    You have also received the breakdown of this code into different UI components. 

    You have also received instructions for how you are expected to style the UI components. 

    Please use each of these to create the ideal CSS styles for each of the html components.

    <code>
    {code}
    </code>

    <instructions>
    {instructions}
    </instructions>

    <components>
    {components}
    </components>


    Once you have finished styling all the components, output the final CSS code in the following format:

    <css>
    {{css_code}}
    </css>

    """


    return prompt;
