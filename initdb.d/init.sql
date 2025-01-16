CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
