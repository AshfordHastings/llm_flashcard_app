import React, { useState } from 'react';
import axios from 'axios';
import './CreateDeck.css';

const CreateDeck = ({ onDeckCreated }) => {
    const [deckName, setDeckName] = useState(''); // Set initial state

    const handleSubmit = (event) => {
        event.preventDefault(); // Prevents a page reload

        axios.post(
            '/api/decks/',
            {
                name: deckName
            }
        ).then(
            response => {
                onDeckCreated(response.data.value);
                setDeckName('');
            }
        ).catch(
            error => {
                console.error("There was an error fetching the deck: ", error)
            }
        );
    };

    return (
        <form onSubmit={handleSubmit} className="create-deck-form">
            <input 
                type="text"
                value={deckName}
                onChange={(e) => setDeckName(e.target.value)}
                placeholder="Enter new deck name."
                required
            />
            <button type="submit" className='create-deck-button'>Create Deck</button>
        </form>
    );
};

export default CreateDeck;