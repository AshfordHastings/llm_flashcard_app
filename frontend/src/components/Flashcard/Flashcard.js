import React, { useState, useEffect } from 'react'
import './Flashcard.css'

import { generateAnswer } from '../../services/flashcardService';

const Flashcard = ({ flashcard, deck, onSaveFlashcard, onCancelFlashcard, onDeleteFlashcard, onToggleEdit }) => {
    if (flashcard.isEditing) {
        return (
            <FlashcardEditor
                flashcard={flashcard}
                deck={deck}
                onSaveFlashcard={onSaveFlashcard}
                onCancelFlashcard={onCancelFlashcard}
                onDeleteFlashcard={onDeleteFlashcard}
            />
        );
    } else {
        return (
            <FlashcardReader
                flashcard={flashcard}
                onToggleEdit={onToggleEdit}
                onDeleteFlashcard={onDeleteFlashcard}
            />
        );
    }
};

const FlashcardReader = ({ flashcard, onToggleEdit, onDeleteFlashcard }) => {
    return (
        <div className='flashcard' id={flashcard.id}>
            <div className="question">
                <summary>{flashcard.question}</summary>
                <div className='icons'>
                    <span className="edit-icon" onClick={() => onToggleEdit(flashcard)}>✎</span>
                    <span className="delete-icon" onClick={() => onDeleteFlashcard(flashcard)}>✖</span>
                </div>
            </div>
            <details className="answer">
                <summary>Answer</summary>
                <p>{flashcard.answer}</p>
            </details>
        </div>
    );
};

const FlashcardEditor = ({ flashcard, deck, onSaveFlashcard, onCancelFlashcard, onDeleteFlashcard }) => {
    const [question, setQuestion] = useState(flashcard.question);
    const [answer, setAnswer] = useState(flashcard.answer);

    const handleSaveFlashcard = () => {
        onSaveFlashcard({
            ...flashcard,
            question,
            answer
        });
    };

    const handleCancelFlashcard = () => {
        setQuestion(flashcard.question)
        setAnswer(flashcard.answer)
        onCancelFlashcard(flashcard)
    }

    const handleGenerateAnswer = async () => {
        try {
            const generatedAnswer = await generateAnswer(question);
            setAnswer(generatedAnswer);
        } catch (error) {
            console.error("There was an error generating the answer: ", error);
        }
    };

    return (
        <div className='flashcard'>
            <div className='question'>
                <div className='editable-section'>
                    <textarea 
                        className="edit-question"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                    />
                </div>
                {/* <div className="icons">
                    <span className="edit-icon" onClick={() => onToggleEdit(flashcard)}>✎</span>
                    <span className="delete-icon" onClick={() => onDeleteFlashcard(flashcard)}>✖</span>
                </div> */}
            </div>
            <div className='answer'>
                <div className="editable-section">
                    <textarea
                        className="edit-answer"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                    />
                </div>
            </div>
            <div className='action-buttons'>
                <button className='save-btn' onClick={handleSaveFlashcard}>Save</button>
                <button className='cancel-btn' onClick={handleCancelFlashcard}>Cancel</button>
                <button className='delete-btn' onClick={() => onDeleteFlashcard(flashcard)}>Delete</button>
                <button className='generate-btn' onClick={handleGenerateAnswer}>Generate</button>
            </div>
        </div>
    )
};

export default Flashcard