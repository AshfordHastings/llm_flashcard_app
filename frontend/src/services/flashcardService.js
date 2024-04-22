import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';


// Fetch all flashcards for a specific deck
export const fetchFlashcards = async (deckId) => {
    const response = await axios.get(`/api/decks/${deckId}/flashcards/`);
    return response.data.value.map(flashcard => ({
        ...flashcard,
        isDraft: false,
        isEditing: false
    }));
};

// Save edited flashcard
export const saveEditedFlashcard = async (deckId, editedFlashcard) => {
    const response = await axios.put(`/api/decks/${deckId}/flashcards/${editedFlashcard.id}`, {
        question: editedFlashcard.question,
        answer: editedFlashcard.answer
    });
    return {
        ...editedFlashcard,
        isEditing: false  // Ensuring to reset the editing flag
    };
};

// Save new flashcard
export const saveNewFlashcard = async (deckId, newFlashcard) => {
    const response = await axios.post(`/api/decks/${deckId}/flashcards/`, [{
        question: newFlashcard.question,
        answer: newFlashcard.answer
    }]);
    return {
        ...response.data.value[0],
        isDraft: false,
        isEditing: false
    };
};

// Delete a flashcard
export const deleteFlashcard = async (deckId, flashcardId) => {
    await axios.delete(`/api/decks/${deckId}/flashcards/${flashcardId}`);
};

// Generate questions
// Add to flashcardService.js
export const generateQuestions = async (specifications, numQuestions, previousQuestions) => {
    const response = await axios.post(`/api/llm/questions/generate`, {
        specifications: specifications,
        num_questions: numQuestions,
        previous_questions: previousQuestions
    });
    return response.data.value.map(flashcard => ({
        ...flashcard,
        id: uuidv4(),
        isEditing: false,
        isDraft: true
    }));
};


// Generate an answer
export const generateAnswer = async (question) => {
    const response = await axios.post(`/api/llm/answers/generate`, { question });
    return response.data.value.answer

}
