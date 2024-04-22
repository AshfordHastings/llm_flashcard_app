import React, { useState, useEffect } from 'react'
import './SidePanel.css'

import Flashcard from '../Flashcard/Flashcard'
import { generateQuestions } from '../../services/flashcardService'

const SidePanel = ({ deck, prevFlashcards, onToggleSidePanel, onSaveFlashcard }) => {
    const [generatedFlashcards, setGeneratedFlashcards] = useState([])
    const [specifications, setSpecifications] = useState("")
    const [numQuestions, setNumQuestions] = useState(1)

    const handleGenerateFlashcards = async () => {
        try {
            const newFlashcards = await generateQuestions(specifications, numQuestions, prevFlashcards.map(f => f.question));
            setGeneratedFlashcards(newFlashcards)
        } catch (error) {
            console.error("There was an error generating the flashcards:", error)
        }
    }

    const handleSaveFlashcard = (flashcard) => {
        setGeneratedFlashcards(prev => prev.map(f => f.id === flashcard.id ? {...flashcard, isEditing: !f.isEditing } : f ))
    };

    const handleDeleteFlashcard = (flashcard) => {
        setGeneratedFlashcards(prev => prev.filter(f => f.id !== flashcard.id));
    };

    const handleCancelFlashcard = (flashcard) => {
        handleToggleEdit(flashcard)
    }

    const handleToggleEdit = (flashcard) => {
        setGeneratedFlashcards(prev => 
            prev.map(f => f.id === flashcard.id ? { ...f, isEditing: !f.isEditing } : f)
        );
    };

    const handleAddFlashcard = (flashcard) => {
        onSaveFlashcard(flashcard);
        setGeneratedFlashcards(prev => prev.filter(f => f.id !== flashcard.id));
    };

    return (
        <div className="side-panel">
            <textarea id="queryInput" placeholder="Enter your instructions." value={specifications} onChange={(e) => setSpecifications(e.target.value)} />
            <input type="number" id="numQuestions" placeholder="Number of questions" value={numQuestions} onChange={(e) => setNumQuestions(e.target.value)} />
            <button className="generate-btn" onClick={handleGenerateFlashcards}>Generate</button>
            <button className="cancel-generate-btn" onClick={onToggleSidePanel}>Cancel</button>
            <div className="generated-flashcards">
                {generatedFlashcards.map(flashcard => 
                    <div>
                        <Flashcard 
                            key={flashcard.id}
                            flashcard={flashcard}
                            deck={deck} 
                            onSaveFlashcard={handleSaveFlashcard}
                            onDeleteFlashcard={handleDeleteFlashcard}
                            onCancelFlashcard={handleCancelFlashcard}
                            onToggleEdit={handleToggleEdit}
                        />
                        <span className="add-icon" onClick={() => handleAddFlashcard(flashcard)}>+</span>
                    </div>
                )}
            </div>
        </div>
    );
}

export default SidePanel