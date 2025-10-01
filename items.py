import db

def add_item(title, length, pace, description, user_id):
    sql = """INSERT INTO items (title, description, length, pace, user_id)
        VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, length, pace, user_id])

def get_items():
    sql = "SELECT id, title, length, pace FROM items ORDER BY id DESC"
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
    result = db.query(sql, [item_id])
    return result [0] if result else None

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

def find_item(query):
    sql = """SELECT id, title, length, pace
            FROM items
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])