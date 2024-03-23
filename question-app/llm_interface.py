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
Based on the following flashcard deck summary and specifications, generate, generate {question_count} practice questions. Do not repeat the existing questions in the deck. Avoid redundancy not only in wording but in the conceptual content of the questions.

Deck Summary:
{deck_summary}

Specifications:
{specifications}

Existing Questions:
{existing_questions}

Format Instructions:
{format_instructions}

"""

class LLMInterface:
    def __init__(self, model:BaseChatModel=None, template=None, format_instructions=None):
        """
        Initializes the LLM interface with the necessary API key.
        """
        self.model = model if model else ChatOpenAI(model="gpt-4")
        self.template = template if template else template_v1
        self.format_instructions = format_instructions if format_instructions else format_instructions_question_json_1

    def generate_questions(self, deck_summary:str, specifications:str="", previous_questions:List[str]=[], num_questions:int=1):
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
        prompt = self._build_prompt(deck_summary, specifications, previous_questions, num_questions)

        parser = JsonOutputParser()
        chain = (
            prompt |
            self.model |
            parser
        )  
        response = chain.invoke({"question_count": str(num_questions)})
        return response
    
    def generate_questions_for_deck(self, deck:Deck, specifications:str="", num_questions:int=1):
        """
        Generates a set of questions for a given deck.

        Parameters:
        - deck: The deck to generate
        - specifications: Additional specifications for question generation.
        - num_questions: The number of questions to generate.

        Returns:
        A list of generated questions.
        """


        prompt = self._build_prompt(deck.summary, specifications, deck.get_previous_questions(), num_questions)

        parser = JsonOutputParser()
        chain = (
            prompt |
            self.model |
            parser
        )  
        response = chain.invoke({"question_count": str(num_questions)})
        return response

    def _build_prompt(self, deck_summary, specifications, previous_questions, num_questions):
        """
        Builds a prompt for the LLM based on input parameters.

        Parameters are the same as for generate_questions method.

        Returns:
        A string prompt for the LLM.
        """

        prompt = ChatPromptTemplate.from_template(
            template=self.template,
            partial_variables={
                #"question_count": str(num_questions),
                "deck_summary": deck_summary,
                "specifications": specifications,
                "existing_questions": "\n-".join(previous_questions),
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