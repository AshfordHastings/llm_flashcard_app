-- Create the "decks" table
CREATE TABLE IF NOT EXISTS decks (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    summary TEXT
);

-- Create the "flashcards" table
CREATE TABLE IF NOT EXISTS flashcards (
    id SERIAL PRIMARY KEY,
    question TEXT,
    answer TEXT,
    deck_id INTEGER NOT NULL,
    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE
);

-- psql -h localhost -p 5432 -U postgres -d flashcard_db
-- \dt - list tables
-- \d decks - describe decks table
-- SELECT * FROM decks;
-- \dn - list schemas