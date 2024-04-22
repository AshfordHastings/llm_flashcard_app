import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';


// Fetch all decks
export const fetchDecks = async () => {
    const response = await axios.get(`/api/decks`);
    return response.data.value.map(deck => ({
        ...deck,
        isDraft: false,
        isEditing: false
    }));
};

// Save edited flashcard
export const saveEditedDeck = async (editedDeck) => {
    const response = await axios.put(`/api/decks/${editedDeck.id}`, {
        name: editedDeck.name
    });
    return {
        ...response.data.value,
        isEditing: false  // Ensuring to reset the editing flag
    };
};

// Save new flashcard
export const saveNewDeck = async (newDeck) => {
    const response = await axios.post(`/api/decks/`, {
        name: newDeck.name,
    });
    return {
        ...response.data.value,
        isDraft: false,
        isEditing: false
    };
};

export const deleteDeck = async (deckId) => {
    await axios.delete(`/api/decks/${deckId}`);
}


