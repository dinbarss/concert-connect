CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    artist TEXT NOT NULL,
    venue TEXT NOT NULL,
    event_date TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    section TEXT,
    row TEXT,
    seat TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE ticket_categories (
    ticket_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Insert some categories
INSERT INTO categories (name) VALUES 
    ('K-pop'), 
    ('J-pop'), 
    ('Anime'), 
    ('Rock'), 
    ('Pop');
