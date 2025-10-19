import db

def add_item(title, length, pace, description, user_id, day_time):
    sql = """INSERT INTO items (title, description, length, pace, user_id, day_time)
        VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, length, pace, user_id, day_time])

def get_items():
    sql = """SELECT items.id, 
                    items.title, 
                    items.length, 
                    items.pace,
                    items.day_time,
                    users.username,
                    users.id AS user_id
                    FROM items
                    JOIN users ON items.user_id = users.id
                    GROUP BY items.id
                    ORDER BY items.id DESC"""
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    items.pace,
                    items.length,
                    items.day_time,
                    users.username,
                    users.id AS user_id
            FROM items, users
            WHERE items.user_id = users.id AND
                    items.id = ?"""
    result = db.query(sql, [item_id])
    return result [0] if result else None

def update_item(item_id, title, length, pace, description, day_time):
    sql = """ UPDATE items SET title = ?,
                                length = ?,
                                pace = ?,
                                description = ?,
                                day_time = ?
                                WHERE id = ?"""
    db.execute(sql, [title, length, pace, description, day_time, item_id])

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

def add_attendance(item_id, user_id):
    sql = """INSERT INTO attendances (item_id, user_id)
        VALUES (?, ?)"""
    db.execute(sql, [item_id, user_id])

def get_attendance(item_id):
    sql = """SELECT attendances.item_id, users.id AS users_id, users.username
            FROM attendances
            JOIN users ON attendances.user_id = users.id
            WHERE attendances.item_id = ? """
    rows = db.query(sql, [item_id])
    return [dict(row) for row in rows]

def has_attended(item_id, user_id):
    sql = "SELECT 1 FROM attendances WHERE item_id = ? AND user_id = ?"
    result = db.query(sql, [item_id, user_id])
    return len(result) > 0

def cancel_attendance(item_id, user_id):
    sql = "DELETE FROM attendances WHERE item_id = ? AND user_id = ?"
    db.execute(sql, [item_id, user_id])