import random
import json
import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from memory.working_memory import WorkingMemory
from memory.lt_memory import LongTermMemory
from helper_functions import sort_actions_by_priority, actions_instructions, use_claude
from promptStrings import componentPrompt, stylePrompt, memoryPrompt
import threading
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key='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')

class Agent:
    def __init__(self):
        """Initialize the agent with working and long-term memory and OpenAI API key"""
        self.reply_callback = None 
        self.style_callback = None
        self.screenshot_callback = None
        self.finish_callback = None
        self.working_memory = WorkingMemory()
        self.long_term_memory = LongTermMemory()
        self.client_sid = None
        self.project_id = None
        self.images = []
        self.css_type = "css"
        self.can_edit_classes = False
        # self.actions_instructions = self.load_actions_from_file("actions.txt")
        self.decision_loop_running = False
        self.decision_thread = None
        self.screenshot_received = asyncio.Event()
        self.client_connected = True


    def reply(self, message):
        if (self.client_connected):
            if self.reply_callback:
                # Remove quotes from the message before sending
                message = message.strip("'")
                self.reply_callback(message, self.client_sid, self.project_id)
        else:
            self.working_memory.observations.append("Client disconnected, cannot reply!")

    def style_code(self, html, css, css_type, edit_classes):
        """Styles the code based on the css_type"""
        component_prompt = componentPrompt(self.working_memory, self.can_edit_classes)

        componentsResponse = use_claude(component_prompt)

        components_start = componentsResponse.find('<final_output>')
        components_end = componentsResponse.find('</final_output>')
        if components_start != -1 and components_end != -1:
            components_json = componentsResponse[components_start + 14:components_end].strip()
            print("COMPONENTS JSON: ", components_json)
            components_data = json.loads(components_json)
        else:
            components_data = {"components": []}  # Handle case where component tags are not found
        
        components = components_data["components"]

        components_string = ', '.join([component['name'] for component in components])

        best_practices = self.long_term_memory.get_best_practices(components_string)
        project_preferences = self.long_term_memory.get_project_preferences(components, self.project_id)

        self.working_memory.store_best_practices(best_practices)
        self.working_memory.store_project_preferences(project_preferences)

        style_prompt = stylePrompt(components, self.working_memory, self.css_type, self.can_edit_classes)

        response = use_claude(user_prompt=style_prompt, images=self.images)

        print("STYLE RESPONSE: ", response, style_prompt)

        # Find updated html code if that's there
        html_start = response.find('<html>')
        html_end = response.find('</html>')
        html_code = None
        if html_start != -1 and html_end != -1:
            html_code = response[html_start + 6:html_end].strip()
            self.working_memory.html_code = html_code;
        
        # Extract CSS code from the response
        css_start = response.find('<css>')
        css_end = response.find('</css>')
        if css_start != -1 and css_end != -1:
            css_code = response[css_start + 5:css_end].strip()
        else:
            css_code = ""  # Handle case where CSS tags are not found
        
        self.working_memory.css_code = css_code;

        if self.style_callback:
            self.style_callback(css_code, self.client_sid, self.project_id, html_code);


        self.working_memory.reset_after_style();

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
        response = use_claude(prompt, images=self.images);

        
        start = response.find('{')
        end = response.find('}') + 1
        if start != -1 and end != -1:
            proposed_actions = json.loads(response[start:end])["actions"]
        else:
            proposed_actions = "{}"  # Return empty array if no brackets found

        print("PROPOSED ACTIONS: ", proposed_actions)
        print("REASONING: ", response)
        return proposed_actions

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

        response = use_claude(prompt, images=self.images);


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

        return json.loads(proposed_actions)


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

        response = use_claude(prompt, images=self.images);

        if "<execute>" in response:
            return best_action
        else:
            print(response);
            return None
    

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

        elif action_name == "screenshot":
            if self.client_connected:
                self.screenshot_callback(self.client_sid, self.project_id)
                isFinal = True
            else:
                self.working_memory.observations.append("Unable to access screenshots at the moment.")

        elif action_name == "reply":
            self.reply(action[5:])
        
        elif action_name == "finish":
            self.learn()
            if self.finish_callback:
                self.finish_callback(self.client_sid, self.project_id)
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
                continue

            print("FINAL SELECTED ACTION: ", selected_action)
            is_final = self.execute_action(selected_action)
            
            if is_final:
                self.decision_loop_running = False

            print("WORKING MEMORY NOW: ", self.working_memory.print())
            
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    
    def learn(self):
        """Learns from the working memory and updates the long term memory"""
        prompt = memoryPrompt(self.working_memory)
        response = use_claude(prompt)

        # Extract the memory updates from the response
        start = response.find('<memory_update>')
        end = response.find('</memory_update>')
        if start != -1 and end != -1:
            memory_update_json = response[start + len('<memory_update>'):end].strip()
            # Remove the "memory_update: " prefix if it exists
            memory_update_json = memory_update_json.replace('"memory_update":', '').strip()
            try:
                memory_updates = json.loads(memory_update_json)
                if isinstance(memory_updates, list):
                    self.long_term_memory.add_project_preferences(memory_updates, self.project_id)
                    print("Memory updates:", memory_updates)
                else:
                    print("Memory updates is not a list.")
            except json.JSONDecodeError:
                print("Failed to parse memory updates JSON.")
        else:
            print("No memory updates found in the response.")
        print("MEMORY UPDATE: ", response)
        return
    
    
    def receive_input(self, html_code, css_code, texts, images, css_type, edit_classes, client_sid, project_id):
        """Receive full user input"""

        self.working_memory.html_code = html_code
        self.working_memory.css_code = css_code
        self.images = images
        self.css_type = css_type
        self.can_edit_classes = edit_classes
        self.working_memory.can_edit_classes = edit_classes
        self.working_memory.css_type = css_type
        # Handle both single inputs and arrays
        if isinstance(texts, list):
            self.working_memory.observations.extend(texts)
        else:
            self.working_memory.observations.append(texts)
        
        self.client_sid = client_sid
        self.project_id = project_id
        if not self.decision_loop_running:
            self.decision_thread = threading.Thread(target=self.make_decision)
            self.decision_thread.start()

    def receive_screenshot(self, screenshot):
        self.images.append({"image": screenshot, "text": "Screenshot"})
        self.screenshot_received.set()
        if not self.decision_loop_running:
            self.decision_thread = threading.Thread(target=self.make_decision)
            self.decision_thread.start()

    def set_client_disconnected(self):
        self.client_connected = False

    def set_client_connected(self):
        self.client_connected = True
