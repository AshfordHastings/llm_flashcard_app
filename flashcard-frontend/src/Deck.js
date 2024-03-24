import React from 'react';
import axios from 'axios';

const Deck = ({ deck }) => {
  // Add functions for handling deck operations (view, add, delete flashcards)
  // Example for adding a flashcard to this deck:
  const addFlashcard = () => {
    const question = prompt("Enter the flashcard question:");
    const answer = prompt("Enter the flashcard answer:");

    axios.post(`/api/decks/${deck.id}/flashcards`, { question, answer })
      .then(() => {
        // Refresh the deck's flashcards or update the state to show the new flashcard
      })
      .catch(error => console.error("There was an error adding the flashcard:", error));
  };

  return (
    <div>
      <h3>{deck.name}</h3>
      {/* Display flashcards here */}
      {/* Add button or form to add new flashcard */}
      <button onClick={addFlashcard}>Add Flashcard</button>
    </div>
  );
};

export default Deck;
