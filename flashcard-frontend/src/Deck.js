import React from 'react';
import axios from 'axios';

const Deck = ({ deck, onDeckDeleted, onDeckSelected }) => {
  // Add functions for handling deck operations (view, add, delete flashcards)
  // Example for adding a flashcard to this deck:
  // const addFlashcard = () => {
  //   const question = prompt("Enter the flashcard question:");
  //   const answer = prompt("Enter the flashcard answer:");
  //   const deck_id = deck.id

  //   axios.post(
  //     `/api/decks/${deck.id}/flashcards/`, 
  //     [{
  //       deck_id: deck_id,
  //       question: question,
  //       answer: answer 
  //     }]
  //   )
  //   .then(() => {
  //     // Refresh the deck's flashcards or update the state to show the new flashcard
  //   })
  //   .catch(error => console.error("There was an error adding the flashcard:", error));
  // };

  const deleteDeck = (e) => {
    e.stopPropagation(); // Prevents the click event from bubbling up the DOM tree to the parent element
    axios
      .delete(`/api/decks/${deck.id}`)
      .then(() => {
        onDeckDeleted(deck.id)
      })
      .catch(error => console.error("There was an error deleting the deck:", error));
  }

  return (
    <div className="deck" onClick={(() => onDeckSelected(deck) )}>
      <div className="deck-name">
        <h3>{deck.name}</h3>
        {/* Display flashcards here */}
        {/* Add button or form to add new flashcard */}
        <div className="icons">
          <span className="edit-icon">≈</span>
          <span className="delete-icon" onClick={(() => deleteDeck() )}>x</span>
        </div>
      </div>
    </div>
  );
};

export default Deck;
