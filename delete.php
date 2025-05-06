<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $db = new SQLite3('database.sqlite');
    $stmt = $db->prepare("DELETE FROM notes WHERE id = :id");
    $stmt->bindValue(':id', $_POST['id'], SQLITE3_INTEGER);
    $stmt->execute();
}
header("Location: index.php");
exit;
