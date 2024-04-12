import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DeckList = ({ onDeckSelected }) => {
  const [decks, setDecks] = useState([]);

  useEffect(() => {
    // Fetch all decks
    fetchDecks()
  }, []);

  const fetchDecks = () => {
    axios.get('/api/decks/')
      .then(response => {
            const decksWithFlags = response.data.value.map(deck => (
              {
                ...deck,
                isDraft: false,
                isEditing: false
              }
            ))
            setDecks(decksWithFlags)
      })
      .catch(error => console.error("There was an error fetching the decks:", error));
  }

  const handleDeckDeleted= (deleteDeck) => {
    axios.delete(`/api/decks/${deleteDeck.id}`
    ).then(
      setDecks((prevDecks) => prevDecks.filter(deck => deck.id !== deleteDeck.id))
    ).catch(error => console.error("There was an error deleting the deck:", error));
  }

  const handleAddDeckDraft = () => {
    setDecks(prevDecks => {
        return [...prevDecks, {
            id: -Date.now(),
            name: "",  
            isDraft: true,
            isEditing: true
        }]
    })
  }

  const handleToggleDeckEdit = (deck) => {
    setDecks(prevDecks => {
        return prevDecks.map(d => {
            if (d.id === deck.id) {
                return {
                    ...d,
                    isEditing: !d.isEditing
                }
            }
            return d
        })
    })
  }

  return (
    <div className='deck-list'>
      <h2>Decks</h2>
      {decks.map(deck => {
        return deck.isDraft ? (
          <div></div>
        ) :
        deck.isEditing ? (
          <DeckEditor
            key={deck.id} 
            deck={deck} 
            onDeckDeleted={handleDeckDeleted} 
            onDeckSelected={onDeckSelected}
            onToggleDeckEdit={handleToggleDeckEdit}
          />
        ) : (
          <DeckReader 
            key={deck.id} 
            deck={deck} 
            onDeckDeleted={handleDeckDeleted} 
            onDeckSelected={onDeckSelected}
            onToggleDeckEdit={handleToggleDeckEdit}
          />
        )
      }
        )}
      {/* {<CreateDeck onDeckCreated={handleDeckCreated} />} */}
      <div className='add-icon' onClick={handleAddDeckDraft}>+</div>
    </div>
  
);

  // return (
  //   <div className='deck-list'>
  //     <h2>Decks</h2>
  //     {decks.map(deck => <Deck 
  //       key={deck.id} 
  //       deck={deck} 
  //       onDeckDeleted={handleDeckDeleted} 
  //       onDeckSelected={onDeckSelected} />)}
  //     {/* {<CreateDeck onDeckCreated={handleDeckCreated} />} */}
  //     <div className='add-icon' onClick={handleAddDeckDraft}>+</div>
  //   </div>
    
  // );
};


const DeckReader = ({ deck, onDeckSelected, onDeckDeleted, onToggleDeckEdit }) => {

  // const deleteDeck = (e) => {
  //   e.stopPropagation(); // Prevents the click event from bubbling up the DOM tree to the parent element
  //   axios
  //     .delete(`/api/decks/${deck.id}`)
  //     .then(() => {
  //       onDeckDeleted(deck.id)
  //     })
  //     .catch(error => console.error("There was an error deleting the deck:", error));
  // }

  const handleDeckDeleted = (e, deck) => {
    e.stopPropagation();
    onDeckDeleted(deck);
  }

  const handleToggleDeckEdit = (e, deck) => {
    e.stopPropagation();
    onToggleDeckEdit(deck);
  }

  return (
    <div className="deck"  onClick={!deck.isEditing ? (() => onDeckSelected(deck)) : null } >
      <div className="deck-name">
        <h3>{deck.name}</h3>
        {/* Display flashcards here */}
        {/* Add button or form to add new flashcard */}
        <div className="icons">
          <span className="edit-icon" onClick={(e) => handleToggleDeckEdit(e, deck) }>✎</span>
          <span className="delete-icon" onClick={(e) => handleDeckDeleted(e, deck) }>✖</span>
        </div>
      </div>
    </div>
  );
};

const DeckEditor = ({ deck, onDeckSelected, onDeckDeleted, onToggleDeckEdit }) => {
  const [deckName, setDeckName] = useState(deck?.name ?? '');

  // const deleteDeck = (e) => {
  //   e.stopPropagation(); // Prevents the click event from bubbling up the DOM tree to the parent element
  //   axios
  //     .delete(`/api/decks/${deck.id}`)
  //     .then(() => {
  //       onDeckDeleted(deck.id)
  //     })
  //     .catch(error => console.error("There was an error deleting the deck:", error));
  // }

  const handleDeckDeleted = (e, deck) => {
    e.stopPropagation();
    onDeckDeleted(deck);
  }

  const handleToggleDeckEdit = (e, deck) => {
    e.stopPropagation();
    onToggleDeckEdit(deck);
  }

  return (
    <div className="deck"  onClick={!deck.isEditing ? (() => onDeckSelected(deck)) : null } >
      <div className="deck-name">
        <h3>{deck.name}</h3>
        {/* Display flashcards here */}
        {/* Add button or form to add new flashcard */}
        <div className="icons">
          <span className="edit-icon" onClick={(e) => handleToggleDeckEdit(e, deck) }>✎</span>
          <span className="delete-icon" onClick={(e) => handleDeckDeleted(e, deck) }>✖</span>
        </div>
      </div>
    </div>
  );
};

export default DeckList;
