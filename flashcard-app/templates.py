format_instructions = """
Format Instructions:
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
# This JSON Schema represents the format I want you to follow to generate your answer. Only return the json object in the specified format.


template_v1 = """
A text will be passed to you. Using the text, generate {question_count} practice questions about the text. 

{format_instructions}

Text: {text}
"""

template_v1_1 = """
A text will be passed to you. Using the text, generate {question_count} practice questions about the text. 

{format_instructions}

Text: {text}
"""