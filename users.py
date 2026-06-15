
import db

def get_user(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_tickets(user_id):
    sql = """SELECT id,
                    artist,
                    venue,
                    event_date,
                    price,
                    section,
                    row,
                    seat,
                    description,
                    created_at
             FROM tickets
             WHERE user_id = ?
             ORDER BY created_at DESC"""
    return db.query(sql, [user_id])
