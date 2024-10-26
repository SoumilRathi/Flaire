import datetime
from firebase import firestore
from sentence_transformers import SentenceTransformer
from mongodb import client
from numpy import dot
from numpy.linalg import norm
from firebase import db
import numpy as np


model = SentenceTransformer('all-mpnet-base-v2')


class LongTermMemory:
    def __init__(self):
        """Initialize long-term memory as dictionaries of sentences"""
        self.episodic = [];
        self.semantic = [];
        self.procedural = [];

    def get_best_practices(self, query):
        """Get the best practices relating to a given query"""

        db = client.css
        coll = db.best_practices

        segment_embedding = model.encode(query);

        segment_embedding = segment_embedding.tolist();

        resultsList = [];

        results = coll.aggregate([
            {
                "$vectorSearch": {
                    "index": "embedding",
                    "path": "embedding",
                    "queryVector": segment_embedding,
                    "limit": 6,
                    "numCandidates": 41
                }
            }
        ])

        for result in results:
            resultsList.append(result['text']);

        return resultsList;

    def add_project_preferences(self, preferences, project_id):
        """Add the project preferences to the long term memory"""

        projectRef = db.collection("projects").document(project_id)

        newPreferences = []

        for preference in preferences:
            newPreferences.append({
                "text": preference,
                "embedding": model.encode(preference).tolist()
            })

        projectRef.update({
            "preferences": firestore.ArrayUnion(newPreferences)
        })

    def get_project_preferences(self, components, project_id):
        """Get the project preferences relating to a given components"""

        """
        Alright so we have a decent list of components. 

        The way we can do this is: 
    
        For each component: 
            Take the name from each component. 
            Find the project preferences within 0.5 similarity of that name
                Do you want to link to firebase alr? Yep. Actually that takes some work on the frontend as well so lets ignore that for now. 
            Add all the project preferences to a list. 
            Remove duplicates. 
            Return the list. 
        """

        projectRef = db.collection("projects").document(project_id)

        project_data = projectRef.get();

        try:
            all_project_preferences = project_data.get("preferences")
        except:
            all_project_preferences = []
            
        # this is an array of maps, with each object having a string and an embedding.
        selected_project_preferences = []

        if all_project_preferences:
            for component in components:
                component_name = component["name"]
                component_embedding = model.encode(component_name)

                # Vectorize the similarity calculation
                similarities = np.dot(np.array([pref["embedding"] for pref in all_project_preferences]), component_embedding.T)
                norms = np.linalg.norm(np.array([pref["embedding"] for pref in all_project_preferences]), axis=1) * np.linalg.norm(component_embedding)
                cos_sims = similarities / norms

                # Append text from objects for which embeddings are a match (similarity >= 0.5)
                selected_project_preferences.extend([pref["text"] for pref, sim in zip(all_project_preferences, cos_sims) if sim >= 0.5])
        else:
            # If all_project_preferences is empty, no preferences to process
            selected_project_preferences = []

        # Remove duplicates while preserving order
        selected_project_preferences = list(dict.fromkeys(selected_project_preferences))

        return selected_project_preferences

    
    def store_memory(self, memory_type, memory):
        """Store a memory in the appropriate category"""
        if memory_type == 'episodic':
            self.episodic.append({
                "memory": memory,
                "timestamp": datetime.now()
            })
        elif memory_type == 'semantic':
            self.semantic.append({
                "memory": memory,
                "embedding": model.encode(memory)
            })

            # print("MEMORY STORED IN SEMANTIC MEMORY");

            # print(self.semantic);
        elif memory_type == 'procedural':
            self.procedural.append(memory)
        else:
            raise ValueError("Invalid memory type. Must be 'episodic', 'semantic', or 'procedural'.")


    def retrieve_memory(self, memory_type, memory_request):
        """Retrieve a memory from long term memory"""

        if memory_type == "semantic":

            # Get the embedding of the memory request
            memory_request_embedding = model.encode(memory_request)

            # Create a dictionary to store the similarity scores for each memory
            similarity_scores = {}

            # Calculate the similarity scores for each memory in the semantic memory
            for memory in self.semantic:
                cos_sim = (memory_request_embedding @ memory["embedding"].T) / (norm(memory_request_embedding)*norm(memory["embedding"]))
                similarity_scores[memory["memory"]] = cos_sim

            # Filter the memories with similarity scores greater than or equal to 0.5
            filtered_memories = {memory: score for memory, score in similarity_scores.items() if score >= 0.5}

            # Get the top 5 memories with the highest similarity scores
            top_memories = sorted(filtered_memories.items(), key=lambda x: x[1], reverse=True)[:5]

            # Return the top memories
            return top_memories
        
        else:
            return []

        




