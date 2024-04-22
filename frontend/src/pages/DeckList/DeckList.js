import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './DeckList.css';
import Deck from '../../components/Deck/Deck';
import { fetchDecks, saveEditedDeck, saveNewDeck, deleteDeck } from '../../services/deckService';

const DeckList = ({ onDeckSelected }) => {
  const [decks, setDecks] = useState([]);

  useEffect(() => {
    // Fetch all decks
    fetchDecks().then(setDecks).catch(console.error);
  }, []);


  const handleSaveDeck = async (deck) => {
    if (deck.isDraft) {
        try {
            const addedDeck = await saveNewDeck(deck);
            setDecks(cur => {
                return [
                    addedDeck, 
                    ...cur.filter(f => f.id !== deck.id)
                ];
            });
            // handleToggleEdit(addedDeck)
        } catch (error) {
            console.error("Error adding new deck:", error);
        }
    } else {
        try {
            const updatedDeck = await saveEditedDeck(deck);
            setDecks(decks.map(f => f.id === updatedDeck.id ? updatedDeck : f));
            // handleToggleEdit(updatedDeck)
        } catch (error) {
            console.error("Error saving flashcard:", error);
        }
    }
}

const handleDeleteDeck = async (deck) => {
  if (deck.isDraft) {
      setDecks(decks.filter(f => f.id !== deck.id))
  } else {
      try {
          await deleteDeck(deck.id);
          setDecks(decks.filter(f => f.id !== deck.id));
      } catch (error) {
          console.error("Error deleting deck:", error);
      }
  }
};

const handleCancelDeck = (deck) => {
  if (deck.isDraft) {
      setDecks(decks.filter(f => f.id !== deck.id))
  } else {
      handleToggleEdit(deck)
  }
}

const handleToggleEdit = (deck) => {
  setDecks(cur => cur.map(f => f.id === deck.id ? {...f, isEditing: !f.isEditing} : f)) 
}

const handleAddDeck = () => {
  setDecks(current => [...current, { id: -Date.now(), name: "", isDraft: true, isEditing: true }]);
};
  

  return (
    <div className='deck-list'>
      <h1>Decks</h1>
      {decks.map(deck => (
        <Deck 
            key={deck.id}
            deck={deck}
            onSaveDeck={handleSaveDeck}
            onDeleteDeck={handleDeleteDeck}
            onCancelDeck={handleCancelDeck}
            onToggleEdit={handleToggleEdit}
            onDeckSelected={onDeckSelected}
        />
      ))}
      <div className='add-icon' onClick={handleAddDeck}>+</div>
    </div>
  
);

};




export default DeckList;
