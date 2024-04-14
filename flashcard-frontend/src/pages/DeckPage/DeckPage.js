import React, { useState, useEffect } from 'react'

import Flashcard from '../../components/Flashcard/Flashcard';
import SidePanel from '../../components/SidePanel/SidePanel';
import { fetchFlashcards, saveEditedFlashcard, saveNewFlashcard, deleteFlashcard } from '../../services/flashcardService'; // API functions are now here


const DeckPage = ({ deck, onBack }) => {
    const [flashcards, setFlashcards] = useState([]);
    const [sidePanelActive, setSidePanelActive] = useState(false);

    // Fetch flashcards on mount
    useEffect(() => {
        fetchFlashcards(deck.id).then(setFlashcards).catch(console.error);
    }, [deck.id]);

    // Setup and cleanup back navigation listener
    useEffect(() => {
        const handlePopState = () => onBack();
        window.addEventListener('popstate', handlePopState);
        return () => window.removeEventListener('popstate', handlePopState);
    }, [onBack]);

    const handleSaveFlashcard = async (flashcard) => {
        if (flashcard.isDraft) {
            try {
                const addedFlashcard = await saveNewFlashcard(deck.id, flashcard);
                setFlashcards(cur => {
                    return [
                        addedFlashcard, 
                        ...cur.filter(f => f.id !== flashcard.id)
                    ];
                });
                // handleToggleEdit(addedFlashcard)
            } catch (error) {
                console.error("Error adding new flashcard:", error);
            }
        } else {
            try {
                const updatedFlashcard = await saveEditedFlashcard(deck.id, flashcard);
                setFlashcards(flashcards.map(f => f.id === updatedFlashcard.id ? updatedFlashcard : f));
                handleToggleEdit(updatedFlashcard)
            } catch (error) {
                console.error("Error saving flashcard:", error);
            }
        }
    }

    const handleDeleteFlashcard = async (flashcard) => {
        if (flashcard.isDraft) {
            setFlashcards(flashcards.filter(f => f.id !== flashcard.id))
        } else {
            try {
                await deleteFlashcard(deck.id, flashcard.id);
                setFlashcards(flashcards.filter(f => f.id !== flashcard.id));
            } catch (error) {
                console.error("Error deleting flashcard:", error);
            }
        }
    };

    const handleCancelFlashcard = (flashcard) => {
        if (flashcard.isDraft) {
            setFlashcards(flashcards.filter(f => f.id !== flashcard.id))
        } else {
            handleToggleEdit(flashcard)
        }
    }

    const handleToggleEdit = (flashcard) => {
        setFlashcards(cur => cur.map(f => f.id === flashcard.id ? {...f, isEditing: !f.isEditing} : f)) 
    }

    const handleAddFlashcard = () => {
        setFlashcards(current => [...current, { id: -Date.now(), question: "", answer: "", isDraft: true, isEditing: true }]);
    };

    const handleToggleSidePanel = () => setSidePanelActive(active => !active);

    return (
        <div className='deck-page'>
            <h1>{deck.name}</h1>
            <div className="generate-flashcards-icon" onClick={handleToggleSidePanel}>⚙️</div>
            <div className='flashcards'>
                {flashcards.map(flashcard => (
                    <Flashcard 
                        key={flashcard.id}
                        flashcard={flashcard}
                        deck={deck}
                        onSaveFlashcard={handleSaveFlashcard}
                        onDeleteFlashcard={handleDeleteFlashcard}
                        onCancelFlashcard={handleCancelFlashcard}
                        onToggleEdit={handleToggleEdit}
                    />
                ))}
                <div className='add-icon' onClick={handleAddFlashcard}>+</div>
            </div>
            {sidePanelActive && (
                <SidePanel 
                    deck={deck} 
                    prevFlashcards={flashcards} 
                    onToggleSidePanel={handleToggleSidePanel} 
                    onSaveFlashcard={handleSaveFlashcard}
                />
            )}
        </div>
    );
};


export default DeckPage;