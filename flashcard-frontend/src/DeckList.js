import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Deck from './Deck';
import CreateDeck from './CreateDeck'

const DeckList = ({ onDeckSelected }) => {
  const [decks, setDecks] = useState([]);

  useEffect(() => {
    // Fetch all decks
    fetchDecks()
  }, []);

  const fetchDecks = () => {
    axios.get('/api/decks/')
      .then(response => setDecks(response.data.value))
      .catch(error => console.error("There was an error fetching the decks:", error));
  }

  const handleDeckCreated = (newDeck) => {
    setDecks((prevDecks) => [...prevDecks, newDeck]);
  }

  const handleDeckDeleted = (deckId) => {
    setDecks((prevDecks) => prevDecks.filter(deck => deck.id !== deckId))
  }


  return (
    <div className='deck-list'>
      <h2>Decks</h2>
      {decks.map(deck => <Deck 
        key={deck.id} 
        deck={deck} 
        onDeckDeleted={handleDeckDeleted} 
        onDeckSelected={onDeckSelected} />)}
      {/* {<CreateDeck onDeckCreated={handleDeckCreated} />} */}
    </div>
  );
};

export default DeckList;
