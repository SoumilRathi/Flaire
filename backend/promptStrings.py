from helper_functions import use_claude

def componentPrompt(working_memory, can_edit_classes):
    """Returns a prompt for styling the code"""
    prompt = f"""
    You are an intelligent agent specializing in frontend web development. Your primary task is to analyze HTML code and separate it into distinct UI components. This process is crucial for organizing and styling web pages effectively.

    Here is the working memory you have been provided with:

    <working_memory>
    {working_memory.print()}
    </working_memory>

    Instructions:

    1. Carefully examine the provided HTML code in the working memory.

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
    d. Name the component based on how it will look on the final page, not based on its functionality.
        (For example, buttons will likely look the same across webpages even if one is a message button and another is an email button.)

    4. Separate the HTML code for each component.

    5. You are allowed to create new classes and edit existing classes. Feel free to name UI components that you think make sense, even if they do not have a class assigned to them.

    Before providing your final output, use <component_identification> tags to show your component identification process. In this process:

    1. Analyze the overall structure of the HTML code:
    a. Identify the main structural elements (e.g., <header>, <main>, <footer>).
    b. Note any significant container elements (e.g., <div> with class names indicating layout).
    c. Observe the nesting levels and hierarchy of elements.

    2. Identify repeated patterns:
    a. Look for similar structures that appear multiple times.
    b. Note any elements with classes that suggest repeated use (e.g., "card", "list-item").

    3. List each potential component you identify, numbering them sequentially.

    4. For each potential component:
    a. Quote the relevant HTML code.
    b. Explain why you consider it a separate component, considering:
        - Its visual distinctiveness
        - Its potential for reuse
        - Its role in the overall page structure
    c. Justify your chosen name for the component, relating it to:
        - Its visual appearance
        - Its general function (without being too specific)
        - Any modifiers that affect its design

    5. Consider the relationships between components:
    a. Identify any components that might be part of larger components.
    b. Note any components that might have variations (e.g., primary/secondary buttons).

    After your component identification process, list all the identified components with their respective HTML code in the format specified below.

    Your final output should be in the following format:

    <final_output>
    {{
        "components": [
            {{
                "name": "<Component Name>",
                "html": "<HTML Code for component>"
            }},
            // Additional components...
        ]
    }}
    </final_output>

    Ensure that you have identified all the components, no matter how small, to provide a comprehensive breakdown of the provided HTML code. Double-check that your final output is in the correct JSON format with all brackets and quotation marks properly placed.
    """
    # Extract the LLM's response (the chosen action)
    return prompt;


def stylePrompt(components, working_memory, css_type, can_edit_classes):
    """Returns a prompt for styling the components"""
    prompt = f"""
    You are an AI agent specializing in frontend web development. Your task is to analyze UI components within a webpage and provide appropriate styling based on user requirements and best practices. 

    Here's the information you need to work with:

    <working_memory>
    {working_memory.print()}
    </working_memory>

    <css_type>
    {css_type}
    </css_type>

    <can_edit_classes>
    {can_edit_classes}
    </can_edit_classes>

    Please follow these steps to complete your task:

    1. Analyze the working memory to identify all UI components present in the webpage.

    2. For each component, determine the appropriate styling based on the following priority:
    a. User input (highest priority)
    b. Retrieved memory of similar components
    c. Your internal knowledge of best practices for web design (lowest priority)

    3. List out each component along with the styling directions you've determined.

    4. Generate the appropriate <css_type> code for each component.

    5. If <can_edit_classes> is true and you need to modify HTML classes, update the HTML code as necessary. Be mindful to make minimal changes unless absolutely required for styling purposes.

    6. After styling all components, format your final output as follows:

    For CSS/SCSS:
    <html>
    [Updated HTML code, if classes were edited. Otherwise, omit this section.]
    </html>

    <css>
    [Your CSS/SCSS code here]
    </css>

    For Tailwind:
    <html>
    [Updated HTML code with Tailwind classes]
    </html>

    Important notes:
    - Ensure that you style all identified components.
    - Verify that your CSS/SCSS/Tailwind code is valid and correct.
    - If outputting HTML (either due to class edits or Tailwind usage), ensure the entire HTML code for the webpage is included and is valid.
    - Pay attention to any existing CSS code and try to maintain its formatting unless changes are necessary for your styling updates.
    - Do not use CSS variables in your code. The renderer will not be able to process them. This is INCREDIBLY IMPORTANT

    Before providing your final output, wrap your thoughts in <analysis> tags to organize your approach and ensure you've covered all necessary steps. In your analysis:
    1. List all UI components identified in the working memory.
    2. For each component:
    a. Note any relevant user input
    b. Mention any retrieved memory of similar components
    c. State the best practices you'll apply
    d. Write down your styling decision
    3. Double-check that your styling decisions align with the provided information and best practices.
    4. Do not use CSS variables in your code. The renderer will not be able to process them. This is INCREDIBLY IMPORTANT
    """


    return prompt;

def memoryPrompt(working_memory):
    """Returns a prompt for the working memory"""
    prompt = f"""
    You are an intelligent agent specializing in frontend web development. You have recently completed a task analyzing HTML code and separating it into distinct UI components. Now, you need to reflect on your experience and update your long-term memory with valuable learnings, focusing particularly on project preferences and styling decisions.

    Here is your working memory from the recent task:

    <working_memory>
    {working_memory.print()}
    </working_memory>

    Your objective is to carefully examine this working memory, reflect on what you've learned, and formulate updates to your long-term memory. These updates should guide your future actions in similar tasks.

    Instructions:
    1. Examine the working memory thoroughly.
    2. Reflect on the task you've completed and identify key learnings.
    3. Focus on project preferences, styling decisions, and any user input that influenced your choices.
    4. Formulate concise, non-redundant memory updates based on your reflections.
    5. Output these updates in the specified format.

    Wrap your thought process inside the following tags:

    <reflection>
    1. Analyze the working memory:
    - What specific HTML components did I encounter (e.g., divs, spans, forms)?
    - What CSS styling patterns did I observe (e.g., flexbox, grid, specific color schemes)?
    - Were there any specific user preferences or requirements mentioned (e.g., accessibility features, responsive design)?

    2. Identify key learnings:
    - What new techniques or approaches did I use in this task?
    - Did I notice any recurring design elements or color schemes that seem important?
    - Were there any challenges I overcame, and how did I solve them?
    - List out at least 3-5 key learnings from this task.

    3. Consider impact on future tasks:
    - How might these learnings influence my approach to similar tasks in the future?
    - Are there any best practices or patterns I should consistently apply going forward?

    4. Formulate memory updates:
    - Which of the identified learnings are most relevant and impactful for future tasks?
    - How can I express these learnings concisely and clearly?
    - Do these updates align with the project preferences examples provided?

    5. Review and refine:
    - Are my updates non-redundant and non-contradictory?
    - Do they focus on colors, fonts, styles, and other frontend elements?
    - Have I captured all important learnings without overloading the memory?
    </reflection>

    After your reflection, output your memory updates in the following format:

    <memory_update>
    "memory_update": ["Update 1", "Update 2", "Update 3"]
    </memory_update>

    Ensure that each update is:
    - Concise and to the point
    - Focused on project preferences, styling decisions, or important frontend development insights
    - Non-redundant and non-contradictory
    - Expressed as a complete thought, similar to the examples provided

    If you determine that you haven't learned anything significant from this task, output an empty list:

    <memory_update>
    "memory_update": []
    </memory_update>

    Remember, these memory updates are crucial for maintaining consistency in your future tasks and improving your performance over time. Be thorough in your reflection and precise in your updates.
    """ 

    return prompt