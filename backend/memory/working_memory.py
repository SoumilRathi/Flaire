"""
Basically there are types of things that we will store in the working memory. First is obviously the history of observations and final outputs within
         a particular episode. This should be an array of the messages, since the only observations rn are messages. 
            Generalize this for the final platform.
         
        Another thing is the history of actions that we have taken. This can just be an array of sentences lmao. 

        And the final thing is the retrieved long term memory. 
            This should be stored in an interesting way. This can be divided into 3 categories: 
                - Episodic: Past experiences as sentences
                - Semantic: General world knowledge as sentences
                - Procedural: Procedural rules or sentences


                But the thing is, each of those should be represented as a map, with each time someone retrieves a memory, 
                the request gets stored as the key and the retrieved memory gets stored as the value.
"""


class WorkingMemory:
    def __init__(self):
        """Initialize working memory with different categories"""
        self.observations = []  # History of observations and final outputs
        self.actions = []  # History of actions taken
        self.html_code = ""
        self.css_code = ""
        self.best_practices = []
        self.project_preferences = []
    
    def store_observation(self, observation):
        """Store an observation or final output"""
        self.observations.append(observation)

    def store_action(self, action):
        """Store an action taken"""
        self.actions.append(action)

    def store_best_practices(self, best_practices):
        """Store best practices"""
        self.best_practices = (best_practices)

    def store_project_preferences(self, project_preferences):
        """Store project preferences"""
        self.project_preferences = project_preferences

    def clear(self):
        """Clear working memory"""
        self.observations = []  # History of observations and final outputs
        self.actions = []  # History of actions taken
        self.html_code = ""
        self.css_code = ""
        self.best_practices = []
        self.project_preferences = []

    def print(self): 
        """Return a formatted string of the contents of working memory"""
        return f"""## Observations
        {self.observations if self.observations else "No observations recorded yet."}

        ## Actions Taken
        {self.actions if self.actions else "No actions taken yet."}

        ## Project Preferences
        {", ".join(self.project_preferences) if self.project_preferences else "No project preferences recorded yet."}

        {f"## Best Practices\n        {' '.join(self.best_practices)}" if self.best_practices else ""}

        ## HTML Code
        {self.html_code if self.html_code else "No HTML code recorded yet."}

        ## CSS Code
        {self.css_code if self.css_code else ""}

        """

    def reset_after_style(self):
        self.best_practices = []
        self.project_preferences = []