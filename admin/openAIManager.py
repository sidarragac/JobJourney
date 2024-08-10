import os, json
from openai import OpenAI
from dotenv import load_dotenv

class openAIManager():
    load_dotenv(".env")
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def generateRoadmap(self, interest, objective, salary):
        content = f"""Imagine you're an experienced recruiter. You're requested to build a 5 steps, self-study roadmap to be a {objective}. For each step of the roadmap, bring recommendations on how to expand the topic you're suggesting and some material you can provide. Also, provide a job I might apply for after completing this goal. Justify how this roadmap will benefy me on my professional career and finally, after making an analysis, say if {salary} dollars a year as expected salary is a good estimation, or either to high or to low considering the level that can be achieved with this roadmap.

Bring your answer in the following format:
Roadmap to become -what I want to become-:
Step 1. -First step towards the goal-
 remarkable points to complete this step and job suggestion.
(Follow step 1 structure for the rest of steps you will bring)

How this roadmap benefit me
Your opinion about my salary expectations
Bring your response on the given format as a pure json-object format without using /n or any other special character."""
        msg = [
            {"role": "user", "content": content}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=msg,
            response_format={"type": "json_object"}
        )
        print(response.choices[0].message.content)
        formatted = json.loads(response.choices[0].message.content)
        print(formatted)
