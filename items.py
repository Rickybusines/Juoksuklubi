import db

def add_item(title, length, pace, description, user_id):
    sql = """INSERT INTO items (title, description, length, pace, user_id)
        VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, length, pace, user_id])