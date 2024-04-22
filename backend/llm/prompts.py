# Format Templates

format_instructions_qa_v1 = """
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
format_instructions_answer_json_1 = """
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
format_instructions_q_v1 = """
Consider the following JSON Schema based on the 2020-12 specification:
```json
{
"title": "Practice Questions",
"description": "A list of practice questions generated from the text.",
"type": "array",
"items": {
    "type": "object",
    "properties": {
        "question": {
            "type": "string",
            "description": "The question generated from the text."
        }
    }
}
```

Please directly output the JSON object, with no additional text, markdown, or formatting outside the JSON structure. The output should be ready for JSON parsing as-is. For example:

[
  {
    "question": "Sample question?"
  }
]
"""

format_instructions_map = {
    "question_v1": format_instructions_q_v1,
    "answer_v1": format_instructions_answer_json_1,
    "answer_v2_advanced": format_instructions_answer_json_1

}

def get_format_instructions(name):
    return format_instructions_map[name]


# Question templates
question_template_v1 ="""
Based on the specifications, generate {num_questions} practice questions. Do not repeat the existing questions in the deck. Avoid redundancy not only in wording but in the conceptual content of the questions.

Specifications:
{specifications}

Existing Questions:
{previous_questions}

Format Instructions:
{format_instructions}
"""

question_template_map = {
    "question_v1": question_template_v1
}

# Answer templates

answer_template_v1 = """
### Instruction ###
You are a tutor who is creating an answer to a practice question. The answer should be detailed and informative, providing a clear explanation of the concepts involved. It should be 5-7 sentences long and cover the main points of the topic.

Example:
Question: What is the difference between authentication and authorization?
Answer: Authentication is the process of verifying the identity of a user or system, often through mechanisms like passwords, tokens, or biometric data. Authorization occurs post-authentication and defines access levels or permissions granted to the authenticated entity, controlling which resources or operations they can access. While authentication validates identity (who you are), authorization determines access rights (what you are allowed to do). Authentication mechanisms include OAuth, JWT for stateless authentication, and multi-factor authentication for enhanced security. Authorization can be implemented via ACLs (Access Control Lists), RBAC (Role-Based Access Control), or ABAC (Attribute-Based Access Control), depending on the granularity of access control required.

Practice Question: 
{question}

Format Instructions:
{format_instructions}
"""

answer_template_v2_advanced = """
### Instruction ###
You are a tutor who is creating an answer to a practice question for an advanced student. Te answer should be detailed and informative, providing a clear explanation of the concepts involved. Include examples and practical applications where possible.


Practice Question: 
{question}

Format Instructions:
{format_instructions}
"""


answer_templates_map = {
    "answer_v1": answer_template_v1,
    "answer_v2_advanced": answer_template_v2_advanced
}

prompt_template_map = {
    **question_template_map,
    **answer_templates_map
}

def get_prompt(name):
    return prompt_template_map[name]
