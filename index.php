<?php
$db = new SQLite3('database.sqlite');
$db->exec("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)");

$notes = $db->query("SELECT * FROM notes");
?>

<!DOCTYPE html>
<html>
<head><title>Simple Notes</title></head>
<body>
    <h1>Notes</h1>

    <form action="create.php" method="POST">
        <input type="text" name="content" placeholder="Write a note" required>
        <button type="submit">Add</button>
    </form>

    <ul>
        <?php while ($row = $notes->fetchArray(SQLITE3_ASSOC)) : ?>
            <li>
                <?= htmlspecialchars($row['content']) ?>
                <form action="delete.php" method="POST" style="display:inline;">
                    <input type="hidden" name="id" value="<?= $row['id'] ?>">
                    <button type="submit">Delete</button>
                </form>
                <form action="update.php" method="POST" style="display:inline;">
                    <input type="hidden" name="id" value="<?= $row['id'] ?>">
                    <input type="text" name="content" placeholder="New content" required>
                    <button type="submit">Update</button>
                </form>
            </li>
        <?php endwhile; ?>
    </ul>
</body>
</html>
