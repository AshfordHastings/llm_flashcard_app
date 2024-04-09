# llm_interface.py

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from domain.flashcard_manager import Flashcard, Deck
 

format_instructions_question_json_1 = """
Consider the following JSON Schema based on the 2020-12 specification:
```json
{
"title": "Practice Questions and Answers",
"description": "A list of practice questions and answers generated from the text.",
"type": "array",
"items": {
    "type": "object",
    "properties": {
        "question": {
            "type": "string",
            "description": "The question generated from the text."
        },
        "answer": {
            "type": "string",
            "description": "The answer to the question."
        }
    }
}
```

Please directly output the JSON object, with no additional text, markdown, or formatting outside the JSON structure. The output should be ready for JSON parsing as-is. For example:

[
  {
    "question": "Sample question?",
    "answer": "Sample answer."
  }
]
"""

template_v1 = """
### Instruction ###
You are a tutor who is creating flashcards for an advanced student. 
Based on the following instructions, generate {question_count} practice questions.
The answer should be detailed and informative, providing a clear explanation of the concepts involved. It should be 5-7 sentences long and cover the main points of the topic.

Instructions:
{instructions}

Format Instructions:
{format_instructions}

"""

class LLMQA:
    def __init__(self, model:BaseChatModel=None, template=None, format_instructions=None):
        """
        Initializes the LLM interface with the necessary API key.
        """
        self.model = model if model else ChatOpenAI(model="gpt-4")
        self.template = template if template else template_v1
        self.format_instructions = format_instructions if format_instructions else format_instructions_question_json_1

    def generate_questions(self, instructions:str, num_questions:int=1):
        """
        Generates a set of questions for a given deck.

        Parameters:
        - deck_summary: A string containing the summary of the deck.
        - specifications: Additional specifications for question generation.
        - previous_questions: A list of strings containing previous questions to avoid repetition.
        - num_questions: The number of questions to generate.

        Returns:
        A list of generated questions.
        """
        prompt = self._build_prompt()

        parser = JsonOutputParser()
        chain = (
            prompt |
            self.model |
            parser
        )  
        response = chain.invoke({"instructions": {instructions}, "question_count": str(num_questions)})
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
