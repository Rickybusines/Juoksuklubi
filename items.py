import db

def add_item(title, length, pace, description, user_id):
    sql = """INSERT INTO items (title, description, length, pace, user_id)
        VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, length, pace, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    items.pace,
                    items.length,
                    users.id AS user_id
            FROM items, users
            WHERE items.user_id = users.id AND
                    items.id = ?"""
    return db.query(sql, [item_id])[0]

def update_item(item_id, title, length, pace, description):
    sql = """ UPDATE items SET title = ?,
                                length = ?,
                                pace = ?,
                                description = ?
                                WHERE id = ?"""
    db.execute(sql, [title, length, pace, description, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])