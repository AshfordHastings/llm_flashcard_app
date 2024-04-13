import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid';

const DeckPage = ({ deck, onBack }) => {
    const [flashcards, setFlashcards] = useState([]);
    const [sidePanelActive, setSidePanelActive] = useState(false);

    useEffect(() => {
        fetchFlashcards()
    }, []);

    useEffect(() => {
        const handlePopState = () => {
            onBack()
        };

        window.addEventListener('popstate', handlePopState);

        return () => {
            window.removeEventListener('popstate', handlePopState);
        }
    }, [onBack])

    const fetchFlashcards = () => {
        axios.get(`/api/decks/${deck.id}/flashcards/`)
            .then(response => {
                const flashcardsWithFlags = response.data.value.map(flashcard => (
                    {
                        ...flashcard,
                        isDraft: false,
                        isEditing: false
                    }
                ))
                setFlashcards(flashcardsWithFlags)
            })
            .catch(error => console.error("There was an error in fetching the Flashcards: ", error))
    }


  const handleSaveEditedFlashcard = (editedFlashcard) => {
    return new Promise((resolve, reject) => {
        axios.put(
            `/api/decks/${deck.id}/flashcards/${editedFlashcard.id}`,
            {
                question: editedFlashcard.question,
                answer: editedFlashcard.answer
            }
        ).then(response =>  {
            const updatedFlashcards = flashcards.map(flashcard => {
                if (flashcard.id === editedFlashcard.id) {
                    return {
                        ...flashcard,
                        ...editedFlashcard, // Overwrites properties from original
                        isEditing: false
                    };
                }
                return flashcard
            });
            setFlashcards(updatedFlashcards);
            resolve(response.data)
        }
        // ).then(data => resolve(data)
        ).catch(error => () => {
            console.error("There was an error saving the flashcard: ", error);
            reject(error);
        });
    });
    }

    const handleSaveNewFlashcard = (newFlashcard) => {
        return new Promise((resolve, reject) => {
            axios.post(
                `api/decks/${deck.id}/flashcards/`, [{
                    question: newFlashcard.question,
                    answer: newFlashcard.answer
                }]
            ).then(response => {
                console.log("New Flashcard creating successfully: ", response.data.value)
                const newFlashcardPersisted = {
                    ...response.data.value[0],
                    isDraft: false,
                    isEditing: false
                };
                setFlashcards(prevFlashcards => {
                    return [newFlashcardPersisted, ...prevFlashcards.filter(flashcard => flashcard.id !== newFlashcard.id)]
                });
                resolve(newFlashcardPersisted)
                
            }).catch(error => () => {
                console.log("There was an error saving the flashcard: :", error);
                reject(error);
            });
        });
        
    }

    const handleDeleteFlashcard = (deletedFlashcard) => {
        axios.delete(
            `/api/decks/${deck.id}/flashcards/${deletedFlashcard.id}`,
            
        ).then(response => {
            setFlashcards((prevFlashcards) => prevFlashcards.filter(flashcard => flashcard.id !== deletedFlashcard.id))
        }).catch(error => console.log("There was an error deleting the flashcard: ", error))
    }

    const handleAddFlashcardDraft = () => {
        setFlashcards(prevFlashcards => {
            return [...prevFlashcards, {
                id: -Date.now(),
                question: "", 
                answer: "", 
                isDraft: true,
                isEditing: true
            }]
        })
    }


    
    const handleCancelNewFlashcard = (newFlashcard) => {
        setFlashcards(prevFlashcards => {
            // return [prevFlashcards.filter(flashcard => flashcard.id !== newFlashcard.id)]
            return prevFlashcards.filter(flashcard => flashcard.id !== newFlashcard.id)
        })
    }

    const handleToggleEdit = (toggleFlashcard) => {
        setFlashcards(prevFlashcards => 
            prevFlashcards.map(flashcard => 
                flashcard.id === toggleFlashcard.id ? {...flashcard, isEditing: !flashcard.isEditing } : flashcard
            )    
        );
    }

    const handleToggleSidePanel = () => {
        setSidePanelActive(!sidePanelActive);
    }

    return (
        <div className='deck-page'>
            <h1>{deck.name}</h1>
            <div className="generate-flashcards-icon" onClick={handleToggleSidePanel}>⚙️</div>
            <div className='flashcards'>
                {flashcards.map(flashcard => <Flashcard 
                    key={flashcard.id}
                    flashcard={flashcard}
                    deck={deck} 
                    onSaveEditedFlashcard={handleSaveEditedFlashcard}
                    onDeleteFlashcard={handleDeleteFlashcard}
                    onSaveNewFlashcard={handleSaveNewFlashcard}
                    onCancelNewFlashcard={handleCancelNewFlashcard}
                    onToggleEdit={handleToggleEdit}
                    />)
                }
                <div className='add-icon' onClick={handleAddFlashcardDraft}>+</div>
            </div>
            {sidePanelActive ? <SidePanel deck={deck} prevFlashcards={flashcards} onToggleSidePanel={handleToggleSidePanel} onSaveNewFlashcard={handleSaveNewFlashcard} /> : null}
        </div>
    );
            };

const SidePanel = ({ deck, prevFlashcards, onToggleSidePanel, onSaveNewFlashcard }) => {
    const [generatedFlashcards, setGeneratedFlashcards] = useState([])
    const [instructions, setInstructions] = useState("")
    const [numQuestions, setNumQuestions] = useState(1)

    const handleGenerateFlashcards = () => {
        axios.post(
            `/api/llm/questions/generate`,
            {
                specifications: instructions,
                num_questions: numQuestions,
                previous_questions: prevFlashcards.map(flashcard => flashcard.question)

            }
        ).then(response =>  {
            const updatedFlashcards = response.data.value.map(flashcard => ({
                ...flashcard,
                id: uuidv4(),
                isEditing: false,
                isDraft: false
            }));
            setGeneratedFlashcards(updatedFlashcards);
        }
        // ).then(data => resolve(data)
        ).catch(error => () => {
            console.error("There was an error generating the flashcards: ", error);
        });
    }

    const handleSaveNewFlashcard = (newFlashcard) => {
        onSaveNewFlashcard(newFlashcard)
        setGeneratedFlashcards(prevFlashcards => prevFlashcards.filter(flashcard => flashcard.id !== newFlashcard.id))
    }
    const handleSaveEditedFlashcard = (editedFlashcard) => {
        const updatedFlashcards = generatedFlashcards.map(flashcard => {
            if (flashcard.id === editedFlashcard.id) {
                return {
                    ...flashcard,
                    ...editedFlashcard, // Overwrites properties from original
                    isEditing: false
                };
            }
            return flashcard
        });
        setGeneratedFlashcards(updatedFlashcards)
    } 

    const handleDeleteFlashcard = (deletedFlashcard) => {
        setGeneratedFlashcards((prevFlashcards) => prevFlashcards.filter(flashcard => flashcard.id !== deletedFlashcard.id))
    } 

    const handleToggleEdit = (toggleFlashcard) => {
        setGeneratedFlashcards(prevFlashcards => 
            prevFlashcards.map(flashcard => 
                flashcard.id === toggleFlashcard.id ? {...flashcard, isEditing: !flashcard.isEditing } : flashcard
            )    
        );
    }

    return (
        <div className="side-panel">
            <textarea id="queryInput" placeholder="Enter your instructions." value={instructions} onChange={(e) => setInstructions(e.target.value)}></textarea>
            <input type="number" id="numQuestions" placeholder="Number of questions" value={numQuestions} onChange={(e) => setNumQuestions(e.target.value)}></input>
            <button className="generate-btn" onClick={handleGenerateFlashcards}>Generate</button>
            <button className="cancel-generate-btn" onClick={onToggleSidePanel}>Cancel</button>
            <div className="generated-flashcards">
                {generatedFlashcards.map(flashcard => 
                <div>
                <Flashcard 
                    key={flashcard.id}
                    flashcard={flashcard}
                    deck={deck} 
                    onSaveEditedFlashcard={handleSaveEditedFlashcard}
                    onDeleteFlashcard={handleDeleteFlashcard}
                    onSaveNewFlashcard={() => null}
                    onCancelNewFlashcard={() => null }
                    onToggleEdit={handleToggleEdit}
                />
                <span className="add-icon" onClick={() => handleSaveNewFlashcard(flashcard)}>+</span>
                </div>
                )}
            </div>
        </div>
    );
}

const Flashcard = ({ flashcard, deck, onSaveEditedFlashcard, onDeleteFlashcard, onSaveNewFlashcard, onCancelNewFlashcard, onToggleEdit,  }) => {

    return (
        <div>
            {
                flashcard.isDraft ? (
                    <FlashcardEditor flashcard={flashcard} deck={deck} onToggleEdit={onToggleEdit} onSaveEditedFlashcard={onSaveNewFlashcard} onDeleteFlashcard={onCancelNewFlashcard} onCancelFlashcard={onCancelNewFlashcard} />
                ) :
                flashcard.isEditing ? (
                    <FlashcardEditor flashcard={flashcard} deck={deck} onToggleEdit={onToggleEdit} onSaveEditedFlashcard={onSaveEditedFlashcard} onDeleteFlashcard={onDeleteFlashcard} onCancelFlashcard={(flashcard) => onToggleEdit(flashcard)} />
                ) : (
                    <FlashcardReader flashcard={flashcard} onToggleEdit={onToggleEdit} onDeleteFlashcard={onDeleteFlashcard}/>
                )}
        </div>
    )
}

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
    )
}

const FlashcardEditor = ({ flashcard, deck, onToggleEdit, onSaveEditedFlashcard, onDeleteFlashcard, onCancelFlashcard }) => {
    const [question, setQuestion] = useState(flashcard?.question ?? '')
    const [answer, setAnswer] = useState(flashcard?.answer ?? '')

    const handleSave = () => {
        console.log("Saving changes to the flashcard")

        onSaveEditedFlashcard({
            ...flashcard,
            question,
            answer
        })
        // .then(() => {
        //     onToggleEdit(flashcard)
        // })

    }

    const handleCancel = () => {
        setQuestion(flashcard.question)
        setAnswer(flashcard.answer)

        onCancelFlashcard(flashcard)
    }

    
    const handleGenerateAnswer = () => {
        axios.post(
            `/api/llm/answers/generate`,
            {
                question: question
            }
        ).then(response => {
            setAnswer(response.data.value.answer)
            
        }).catch(error => console.error("There was an error generating the answer: ", error));
    }

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
                <div className="icons">
                    <span className="edit-icon" onClick={() => onToggleEdit(flashcard)}>✎</span>
                    <span className="delete-icon" onClick={() => onDeleteFlashcard(flashcard)}>✖</span>
                </div>
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
                <button className='save-btn' onClick={handleSave}>Save</button>
                <button className='cancel-btn' onClick={handleCancel}>Cancel</button>
                <button className='generate-btn' onClick={handleGenerateAnswer}>Generate</button>
            </div>
        </div>
    )
}

export default DeckPage;