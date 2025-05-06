<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $db = new SQLite3('database.sqlite');
    $stmt = $db->prepare("UPDATE notes SET content = :content WHERE id = :id");
    $stmt->bindValue(':content', $_POST['content'], SQLITE3_TEXT);
    $stmt->bindValue(':id', $_POST['id'], SQLITE3_INTEGER);
    $stmt->execute();
}
header("Location: index.php");
exit;
