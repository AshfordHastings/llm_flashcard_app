# llm_interface.py

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
 

format_instructions_question_json_1 = """
Consider the following JSON Schema based on the 2020-12 specification:
```json
{
"title": "Answer to Practice Question",
"description": "The practice answer generated for a given question.",
"type": "object",
"properties": {
    "answer": {
        "type": "string",
        "description": "The answer to the question."
    }
    
}
```

Please directly output the JSON object, with no additional text, markdown, or formatting outside the JSON structure. The output should be ready for JSON parsing as-is. For example:

{
"answer": "Sample answer."
}

"""

template_v1 = """
### Instruction ###
You are a tutor who is creating an answer to a practice question based on the following specifications. The answer should be detailed and informative, providing a clear explanation of the concepts involved. It should be 5-7 sentences long and cover the main points of the topic.

Example:
Question: What is the difference between authentication and authorization?
Answer: Authentication is the process of verifying the identity of a user or system, often through mechanisms like passwords, tokens, or biometric data. Authorization occurs post-authentication and defines access levels or permissions granted to the authenticated entity, controlling which resources or operations they can access. While authentication validates identity (who you are), authorization determines access rights (what you are allowed to do). Authentication mechanisms include OAuth, JWT for stateless authentication, and multi-factor authentication for enhanced security. Authorization can be implemented via ACLs (Access Control Lists), RBAC (Role-Based Access Control), or ABAC (Attribute-Based Access Control), depending on the granularity of access control required.

Specifications:
{specifications}

Practice Question: 
{question}

Format Instructions:
{format_instructions}

"""

class QuestionAnswerer:
    def __init__(self, model:BaseChatModel=None, template=None, format_instructions=None):
        """
        Initializes the LLM interface with the necessary API key.
        """
        self.model = model if model else ChatOpenAI(model="gpt-4")
        self.template = template if template else template_v1
        self.format_instructions = format_instructions if format_instructions else format_instructions_question_json_1

    def generate_answer(self, question:str, specifications:str=""):
        
        prompt = self._build_prompt()

        parser = JsonOutputParser()
        chain = (
            prompt |
            self.model |
            parser
        )  
        response = chain.invoke({"question": question, "specifications": specifications})
        return response

    def _build_prompt(self):
        """
        Builds a prompt for the LLM based on input parameters.

        Parameters are the same as for generate_questions method.

        Returns:
        A string prompt for the LLM.
        """

        prompt = ChatPromptTemplate.from_template(
            template=self.template,
            partial_variables={
                "format_instructions": self.format_instructions
            }
        )
        return prompt

# Example usage (replace YOUR_API_KEY with an actual OpenAI API key)
# llm_interface = LLMInterface('YOUR_API_KEY')
# questions = llm_interface.generate_questions(
#     deck_summary="A brief overview of Python programming.",
#     specifications="Focus on basic syntax, data types, and control structures.",
#     previous_questions=["What is a variable in Python?"],
#     num_questions=5
# )
# print(questions)
