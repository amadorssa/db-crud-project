<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $db = new SQLite3('database.sqlite');
    $stmt = $db->prepare("INSERT INTO notes (content) VALUES (:content)");
    $stmt->bindValue(':content', $_POST['content'], SQLITE3_TEXT);
    $stmt->execute();
}
header("Location: index.php");
exit;
