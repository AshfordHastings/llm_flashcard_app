import React, { useState, useEffect } from 'react'
import './Deck.css'

const Deck = ({ deck, onSaveDeck, onCancelDeck, onDeleteDeck, onToggleEdit, onDeckSelected }) => {

    if (deck.isEditing) {
        return (
            <DeckEditor
                deck={deck}
                onSaveDeck={onSaveDeck}
                onCancelDeck={onCancelDeck}
                onDeleteDeck={onDeleteDeck}
            />
        );
    } else {
        return (
            <DeckReader
                deck={deck}
                onToggleEdit={onToggleEdit}
                onDeleteDeck={onDeleteDeck}
                onDeckSelected={onDeckSelected}
            />
        );
    }
};

const DeckReader = ({ deck, onToggleEdit, onDeleteDeck, onDeckSelected }) => {
    const handleDeckSelected = (deck) => {
        onDeckSelected(deck)
    }

    const handleToggleEdit = (e, deck) => {
        e.stopPropagation()
        onToggleEdit(deck)
    }


    const handleDeleteDeck = (e, deck) => {
        e.stopPropagation()
        onDeleteDeck(deck)
    }

    return (
        <div className='deck' id={deck.id} onClick={!deck.isEditing ? (() => handleDeckSelected(deck)) : null } >
            <div className="name">
                <summary>{deck.name}</summary>
                <div className='icons'>
                    <span className="edit-icon" onClick={(e) => handleToggleEdit(e, deck)}>✎</span>
                    <span className="delete-icon" onClick={(e) => handleDeleteDeck(e, deck)}>✖</span>
                </div>
            </div>
        </div>
    );
};

const DeckEditor = ({ deck, onSaveDeck, onCancelDeck, onDeleteDeck }) => {
    const [name, setName] = useState(deck.name);

    const handleSaveDeck = () => {
        onSaveDeck({
            ...deck,
            name
        });
    };

    const handleCancelDeck = () => {
        setName(deck.name)
        onCancelDeck(deck)
    }

    return (
        <div className='deck'>
            <div className='name'>
                <div className='editable-section'>
                    <textarea 
                        className="edit-name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>
                {/* <div className="icons">
                    <span className="edit-icon" onClick={() => onToggleEdit(Deck)}>✎</span>
                    <span className="delete-icon" onClick={() => onDeleteDeck(Deck)}>✖</span>
                </div> */}
            </div>
            <div className='action-buttons'>
                <button className='save-btn' onClick={handleSaveDeck}>Save</button>
                <button className='cancel-btn' onClick={handleCancelDeck}>Cancel</button>
                <button className='delete-btn' onClick={() => onDeleteDeck(Deck)}>Delete</button>
            </div>
        </div>
    )
};

export default Deck