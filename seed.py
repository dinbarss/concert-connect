import random
import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect("database.db")

db.execute("DELETE FROM comments")
db.execute("DELETE FROM ticket_categories")
db.execute("DELETE FROM tickets")
db.execute("DELETE FROM users")

user_count = 1000
ticket_count = 10**6
comment_count = 10**7

artists = [
    "BTS", "BLACKPINK", "TWICE", "Stray Kids", "aespa", "NewJeans",
    "IVE", "Le Sserafim", "Ateez", "Monsta X", "EXO", "SHINee",
    "Red Velvet", "NCT 127", "Enhypen", "TXT", "Seventeen", "Got7",
    "Radwimps", "Yoasobi", "Kenshi Yonezu", "Ado", "Eve", "King Gnu"
]

venues = [
    "Helsinki Ice Hall", "Tampere Arena", "Turku Concert Hall",
    "Olympic Stadium Helsinki", "Hartwall Arena", "Logomo Turku",
    "Oulu Arena", "Jyväskylä Paviljonki", "Lahti Assembly Hall",
    "Tampere Hall"
]

password_hash = generate_password_hash("password123")
for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), password_hash])

for i in range(1, ticket_count + 1):
    user_id = random.randint(1, user_count)
    artist = random.choice(artists)
    venue = random.choice(venues)
    event_date = f"2026-{random.randint(8, 12):02d}-{random.randint(1, 28):02d}"
    price = round(random.uniform(20, 300), 2)
    db.execute("""INSERT INTO tickets (user_id, artist, venue, event_date, price, description)
                  VALUES (?, ?, ?, ?, ?, ?)""",
               [user_id, artist, venue, event_date, price, "ticket" + str(i)])

categories = db.execute("SELECT id FROM categories").fetchall()
category_ids = [c[0] for c in categories]

for ticket_id in range(1, ticket_count + 1):
    chosen = random.sample(category_ids, random.randint(1, min(3, len(category_ids))))
    for cat_id in chosen:
        db.execute("INSERT INTO ticket_categories (ticket_id, category_id) VALUES (?, ?)",
                   [ticket_id, cat_id])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    ticket_id = random.randint(1, ticket_count)
    db.execute("""INSERT INTO comments (ticket_id, user_id, content)
                  VALUES (?, ?, ?)""",
               [ticket_id, user_id, "comment" + str(i)])

db.commit()
db.close()
print(f"Done! Added {user_count} users, {ticket_count} tickets, {comment_count} comments.")