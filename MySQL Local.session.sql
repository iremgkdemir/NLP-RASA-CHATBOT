CREATE TABLE demo.conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message TEXT,
    bot_response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);