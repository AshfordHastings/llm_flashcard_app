-- Create the "decks" table
CREATE TABLE IF NOT EXISTS decks (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    summary TEXT
);

-- Create the "flashcards" table
CREATE TABLE IF NOT EXISTS flashcards (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    deckId INTEGER NOT NULL,
    FOREIGN KEY (deckId) REFERENCES decks(id) ON DELETE CASCADE
);
