import React, { useState, useEffect } from 'react'

import { fetchFlashcards, saveEditedFlashcard, saveNewFlashcard, deleteFlashcard, generateAnswer, generateQuestions } from './flashcardService'; // API functions are now here

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


export default DeckPage;