<?php
// Create (or open) the SQLite database
$db = new SQLite3('database.sqlite');

// Create a table named 'notes' with only a content column
$db->exec("CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
)");

echo "Database and table initialized successfully.";
?>

