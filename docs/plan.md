- Create question generation mechanism
- Create an ability to persist flashcards, and save to a location. Potentially, anki. 
- Create a separate chatbot, and provide a command that allows for executing creation of the flashcard creation mechanism. 

## Flow
- User open up main page and chat window. User uploads a certain PDF, and this PDF is persisted. 
- User clicks on PDF. The user is given several configurability options such as number of questions, temperature. The user is also given the option to add extra instructions for the LLM when making the question. 
- User has option to either separate pages by section themselves, or they can allow this to be automated. User can give a title to the sections that they split up. 
- For each section, user can select "generate". 
- The questions are created and returned to the user, filed under that PDF -> section. 
- The user is given the option to either regenerate the question, or to update the configurability, and regenerate. They can then choose "save" if they like the questions provided. 
- A deck is then made that the user can use, for that section. They can modify the deck by deleting, editing, or adding personal flashcards. 

## Flow V1
- User Creates a Flashcard Category and Deck
- User adds a summary of the deck which is fed inside of prompt
- User adds specifications on top of the deck summary 
- Previous questions in a deck are passed to LLM, LLM is told not to repeat the questions
- Number of questions to be generated is presented to the LLM 
- LLM generates a structured response to query
- These are presented to the user in a response. The user can either regenerate with new specifications, save all responses, or save specific responses. 
- When user clicks "save" on one of the questions, it is saved. The other questions are left in tentative mode. If "regenerate" is hit, or save current is clicked, then the other questions are cleared. 
- The user can edit, reorder, the flashcard questions. 

## Future additions
- Within a deck, questions can be assigned "tags". 

## Components:
### Question Answerer
- Usea section of a PDF to 