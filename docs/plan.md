- Create question generation mechanism
- Create an ability to persist flashcards, and save to a location. Potentially, anki. 
- Create a separate chatbot, and provide a command that allows for executing creation of the flashcard creation mechanism. 

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

## Front End Plan
- Deck List Component:
    - List of Decks in block style
    - Can click on to be taken to Deck Page
- Deck Page
    - List of questions with small line separating them 
    - Details and summary pane containing answer to the question 
    - Discrete edit icon to the right of the question
    - Clicking edit icon brings up an edit component
    - Discrete delete icon to the right of the question - deletes the question / answer
- Edit component
    - Turns the question / answer to textbox looking things
- Create new flashcard
    - Brings up the same component as the edit component, but with a cancel button 

## Flow
- User open up main page and chat window. User uploads a certain PDF, and this PDF is persisted. 
- User clicks on PDF. The user is given several configurability options such as number of questions, temperature. The user is also given the option to add extra instructions for the LLM when making the question. 
- User has option to either separate pages by section themselves, or they can allow this to be automated. User can give a title to the sections that they split up. 
- For each section, user can select "generate". 
- The questions are created and returned to the user, filed under that PDF -> section. 
- The user is given the option to either regenerate the question, or to update the configurability, and regenerate. They can then choose "save" if they like the questions provided. 
- A deck is then made that the user can use, for that section. They can modify the deck by deleting, editing, or adding personal flashcards. 



## Future additions
- Within a deck, questions can be assigned "tags". 

## Routes
- GET decks
- POST decks
- GET decks/id
- DELETE decks/id

- POST decks/id/flashcards
- GET decks/id/flashcards
- PUT /decks/id/flashcards/id - update a flashcard

- POST decks/id/generate

- POST /decks/id/save



## Components:
### Question Answerer
- Usea section of a PDF to 