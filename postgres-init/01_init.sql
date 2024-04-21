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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deck_id INTEGER NOT NULL,
    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE
);

-- CREATE TABLE IF NOT EXISTS flashcard_orders (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     flashcard_id INT,
--     deck_id INT,
--     position FLOAT,
--     FOREIGN KEY (flashcard_id) REFERENCES flashcards(id),
--     FOREIGN KEY (deck_id) REFERENCES Dedeckscks(id)
-- );

-- psql -h localhost -p 5432 -U postgres -d flashcard_db
-- \dt - list tables
-- \d decks - describe decks table
-- SELECT * FROM decks;
-- \dn - list schemas