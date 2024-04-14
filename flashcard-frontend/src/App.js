import React, { useState} from 'react';
import './AppStyles.css';
import  DeckList from './pages/DeckList/DeckList';
import DeckPage from './pages/DeckPage/DeckPage';

function App() {
  const [currentPage, setCurrentPage] = useState('deckList');
  const [currentDeck, setCurrentDeck] = useState(null);

  const handleDeckSelected = (deck) => {
    window.history.pushState({ page: 'DeckPage' }, 'DeckPage', '/deckpage');
    setCurrentDeck(deck);
    setCurrentPage('Deck');
  }

  const handleBack = () => {
    setCurrentDeck(null)
    setCurrentPage('DeckList')
  }

  return (
    <div className="App">
      <h1>Flashcard App</h1>
      {(() => { 
        switch (currentPage) {
        case 'DeckList':
          return <DeckList onDeckSelected={handleDeckSelected} />;
        case 'Deck':
          return <DeckPage deck={currentDeck} onBack={handleBack} />;
        default:
          return <DeckList onDeckSelected={handleDeckSelected} />;
      }})()}
    </div>
  );
}

export default App;
