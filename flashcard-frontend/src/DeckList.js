import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Deck from './Deck';

const DeckList = () => {
  const [decks, setDecks] = useState([]);

  useEffect(() => {
    // Fetch all decks
    axios.get('/api/decks/')
      .then(response => setDecks(response.data.value))
      .catch(error => console.error("There was an error fetching the decks:", error));
  }, []);

  return (
    <div>
      <h2>Decks</h2>
      {decks.map(deck => <Deck key={deck.id} deck={deck} />)}
      {/* Add button to create new deck */}
    </div>
  );
};

export default DeckList;
