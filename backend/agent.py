import random
import json
import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from memory.working_memory import WorkingMemory
from memory.lt_memory import LongTermMemory
from helper_functions import sort_actions_by_priority, actions_instructions, use_claude
from actions.styling.promptStrings import componentPrompt, instructionPrompt, stylePrompt
import threading
import os
from dotenv import load_dotenv
from actions.styling.styleAction import style_code as style_action

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key='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')

class Agent:
    def __init__(self):
        """Initialize the agent with working and long-term memory and OpenAI API key"""
        self.reply_callback = None 
        self.style_callback = None
        self.screenshot_callback = None
        self.working_memory = WorkingMemory()
        self.long_term_memory = LongTermMemory()
        self.client_sid = None
        # self.actions_instructions = self.load_actions_from_file("actions.txt")
        self.decision_loop_running = False
        self.decision_thread = None


    def style_code(self, html, css, css_type, edit_classes):
        """Styles the code based on the css_type"""
        component_prompt = componentPrompt(html, self.working_memory)

        componentsResponse = use_claude(component_prompt)

        # we can then convert these components into memory. 
        # the intricacies here have not been decided LMAO.
        # TODO: Decide on how to convert components into memory.

        # Extract components from the Claude response
        components_start = componentsResponse.find('<final_output>')
        components_end = componentsResponse.find('</final_output>')
        if components_start != -1 and components_end != -1:
            components_json = componentsResponse[components_start + 14:components_end].strip()
            components_data = json.loads(components_json)
        else:
            components_data = {"components": []}  # Handle case where component tags are not found
        
        components = components_data["components"]

        components_string = ', '.join([component['name'] for component in components])

        best_practices = self.long_term_memory.get_best_practices(components_string)
        project_preferences = self.long_term_memory.get_project_preferences(components)

        self.working_memory.store_best_practices(best_practices)
        self.working_memory.store_project_preferences(project_preferences)

        style_prompt = stylePrompt(components, self.working_memory)

        response = use_claude(style_prompt)
        
        # Extract CSS code from the response
        css_start = response.find('<css>')
        css_end = response.find('</css>')
        if css_start != -1 and css_end != -1:
            css_code = response[css_start + 5:css_end].strip()
        else:
            css_code = ""  # Handle case where CSS tags are not found
        
        self.working_memory.css_code = css_code;

        if self.style_callback:
            self.style_callback(css_code, self.client_sid);

        return;


    
    def load_actions_from_file(self, filename):
        """Load actions from a text file"""
        with open(filename, 'r') as file:
            content = file.read()
        return content

    def reset(self):
        """Reset the agent to its initial state"""
        self.working_memory = WorkingMemory()
        self.long_term_memory = LongTermMemory()
        self.decision_loop_running = False
        self.decision_thread = None
        print("Agent has been reset to its initial state.")

    def select_action(self, best_action):
        """Decides to either select the highest-scoring action or reject all actions"""

        prompt = f"""
        You are an intelligent agent. You have access to your current working memory, and the actions available to you. 

        You will be given an input, access to your current working memory, and the selected best action to take. 

        Your choice is to decide to either execute the action or reject it. If you execute the action, that means that it is the best action to take at this stage.
        If you reject the action, new actions will be proposed and evaluated for this state. 

        If you wish to execute the action, output "<execute>". If you wish to reject the action, output "<reject>". 
        First output about what that action would do and entail, and then output the choice. 

        {actions_instructions}

        # Working Memory
        {self.working_memory.print()}

        # Selected Action
        {best_action}
        """

        response = use_claude(prompt);

        if "<execute>" in response:
            return best_action
        else:
            return None
    
    def evaluate_actions(self, actions): 
        """Evaluates the proposed actions and assigns them a score based on their relevance"""

        prompt = f"""
        You are an intelligent agent. You have access to your current working memory, and the actions available to you. 

        You will be given an input, access to your current working memory, and a list of proposed actions.

        Your job is to, one by one, evaluate each proposed action based on how helpful it would be at the moment, given the working memory and everything you know about the actions.

        Once you have evaluated each action, give them a score out of 10 based on your evaluation, and output the final list of actions with their scores in the following format:

        {{
            "action 1": "score 1",
            "action 2": "score 2",
            "action 3": "score 3",
            ...
        }}

        Please note that for the scores, you should just output the number as a plain integer, not a fraction, decimal, or sentence.

        {actions_instructions}


        Please evaluate each action carefully first, writing down your evaluation for each action. Then finally output the final list with the scores. 

        # Working Memory
        {self.working_memory.print()}

        # Actions
        {', '.join(actions)}
        """

        response = use_claude(prompt);

        # Find the JSON-like part in the response
        start = response.find('{')
        end = response.find('}') + 1
        if start != -1 and end != -1:
            proposed_actions = response[start:end]
            
            # Separate the last character '}' from the rest, strip whitespaces from the rest
            before_closing_brace = proposed_actions[:-1].rstrip()  # Strip everything except the last character
            if before_closing_brace[-1] == ',':  # Check if there's a comma before the closing brace
                before_closing_brace = before_closing_brace[:-1]  # Remove the comma

            proposed_actions = before_closing_brace + '}'  # Add the closing brace back

        else:
            proposed_actions = "{}"  # Return empty object if no brackets found

        print("SCORED ACTIONS: ", proposed_actions)
        return json.loads(proposed_actions)
    
    
    def propose_actions(self):
        """Use OpenAI API to select the best action based on memory"""

        # Construct the user prompt with proposed actions and memory context
        prompt = f"""
        You are an intelligent agent with access to your current working memory and a set of available actions. Your task is to propose up to five potential actions based on the given input. Here is your current working memory:

        <working_memory>
        {self.working_memory.print()}
        </working_memory>

        Important constraints and instructions:

        1. Do not generate new knowledge or information on your own. You are prone to hallucinations and must not make any assumptions.
        2. Use only the provided actions to acquire new knowledge.
        3. Consider how to provide the best eventual output based on the given input.
        4. Choose actions that will help you reach that output.

        Available actions:
        {actions_instructions}

        Each action is represented as a string. Your task is to propose up to five actions that you could potentially take at this step. These actions are not to be taken in order; one of the proposed actions will be selected and executed at this stage.

        Before providing your final output, use the <action_analysis> tags to think through your action selection process. Consider the following:
        - For each potential action:
        1. How does it relate to the information in your working memory?
        2. What are the potential outcomes of this action?
        3. How relevant and priority is this action given the current context?
        - Which actions are most likely to lead to a productive outcome?
        - Are there any actions that might be redundant or less useful given the current context?

        After your analysis, ensure that youprovide your final chosen actions in a JSON format within <final> tags. 
        
        Here's an example of the expected output structure:
        <final>
        {{
            "actions": ["action_1 'parameter'", "action_2 'parameter'", "action_3 'parameter'"]
        }}
        </final>

        Remember, you must propose at least one action and no more than five actions. Each action should be a string that matches the format of the available actions provided to you.

        Now, begin your action analysis:

        """

        # Call OpenAI API to determine the action
        response = use_claude(prompt);

        
        start = response.find('{')
        end = response.find('}') + 1
        if start != -1 and end != -1:
            proposed_actions = json.loads(response[start:end])["actions"]
        else:
            proposed_actions = "{}"  # Return empty array if no brackets found

        print("PROPOSED ACTIONS: ", proposed_actions)
        return proposed_actions

        
    
    def execute_action(self, action):
        """Executes the selected action. This will simply do whatever the action is supposed to do, and then store the action in the working memory"""

        isFinal = False
        # get the first word of the action
        action_name = action.split()[0]

        print("EXECUTING ACTION: ", action)

        if (action_name == "style"):
            self.style_code(self.working_memory.html_code, self.working_memory.css_code, "external", False)

        elif action_name == "record":
            self.working_memory.observations.append(action[6:])
            isFinal = True

        elif action_name == "screenshot":
            self.screenshot_callback()

        elif action_name == "finish":

            # TODO: Implement the learning process here

            isFinal = True

        print(f"Executing action: {action}")

        self.working_memory.store_action(action)

        return isFinal
    
    def make_decision(self):
        """Main decision-making loop"""
        self.decision_loop_running = True
        while self.decision_loop_running:
            selected_action = None
            n = 0
            while selected_action is None and n < 3:
                proposed_actions = self.propose_actions()
                scored_actions = self.evaluate_actions(proposed_actions)

                best_action = max(scored_actions, key=lambda x: int(scored_actions[x]))

                print("BEST ACTION: ", best_action)
                selected_action = self.select_action(best_action)
                n += 1

            if selected_action is None:
                print("Couldn't select an action to pick - must fix something")
                break

            print("FINAL SELECTED ACTION: ", selected_action)
            is_final = self.execute_action(selected_action)
            
            if is_final:
                self.decision_loop_running = False

            print("WORKING MEMORY NOW: ", self.working_memory.print())
            
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    def receive_input(self, html_code, css_code, user_input, client_sid):
        """Receive HTML code from the user"""
        self.working_memory.html_code = html_code
        self.working_memory.css_code = css_code
        
        # Handle both single inputs and arrays
        if isinstance(user_input, list):
            self.working_memory.observations.extend(user_input)
        else:
            self.working_memory.observations.append(user_input)
        
        self.client_sid = client_sid
        if not self.decision_loop_running:
            self.decision_thread = threading.Thread(target=self.make_decision)
            self.decision_thread.start()