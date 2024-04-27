# llm_interface.py

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from .prompts import get_prompt, get_format_instructions



class LLMQuestionCreator:
    def __init__(self, model:BaseChatModel=None):
        """
        Initializes the LLM interface with the necessary API key.
        """
        self.model = model if model else ChatOpenAI(model="gpt-4")

    def generate_questions(self, specifications:str, num_questions:int=1, previous_questions:List[str]=[], prompt_name="question_v1"):
        prompt_template = get_prompt(prompt_name)
        print(prompt_template)
        format_instructions = get_format_instructions(prompt_name)
        prompt = ChatPromptTemplate.from_template(
            template=prompt_template,
            partial_variables={
                "format_instructions": format_instructions,
            }
        )
        print(f"Prompt: {prompt}")
        print(f"Specifications: {specifications}")
        print(f"Num Questions: {num_questions}")
        print(f"Previous Questions: {previous_questions}")

        parser = JsonOutputParser()

        chain = (
            prompt |
            self.model |
            parser
        )

        response = chain.invoke({"specifications": specifications, "num_questions": str(num_questions), "previous_questions": "\n-".join(previous_questions)})
        return response
    
class LLMAnswerer:
    def __init__(self, model:BaseChatModel=None):
        """
        Initializes the LLM interface with the necessary API key.
        """
        self.model = model if model else ChatOpenAI(model="gpt-4")

    def generate_answer(self, question, prompt_name="answer_v1"):
        prompt = get_prompt(prompt_name)
        format_instructions = get_format_instructions(prompt_name)
        prompt = ChatPromptTemplate.from_template(
            template=prompt,
            partial_variables={
                "format_instructions": format_instructions,
            }
        )

        chain = (
            prompt |
            self.model |
            JsonOutputParser()
        )

        response = chain.invoke({"question": question})
        return response
