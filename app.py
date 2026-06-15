import sqlite3
import secrets
from flask import Flask
from flask import redirect, render_template, request, abort, session
from datetime import date
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import config
import db
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_tickets = users.get_tickets(user_id)
    return render_template("user.html", user=user, tickets=user_tickets)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if not result:
        return render_template("login.html", error="Väärä tunnus tai salasana")

    password_hash = result[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        return render_template("login.html", error="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("register.html", error="Syöttämäsi salasanat eivät täsmää. Yritä uudelleen.")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("login.html", error="Tunnus on jo varattu")
    
    # Redirect to login after registration and pass a success message
    return redirect("/login?registered=1")

# Ticket search
@app.route("/")
def index():
    search_query = request.args.get('search', '')  # Get search parameter from URL
    
    db_conn = sqlite3.connect("database.db")
    db_conn.row_factory = sqlite3.Row
    
    if search_query:
        # Search in artist, venue, and description
        tickets = db_conn.execute('''
            SELECT t.id, t.user_id, t.artist, t.venue, t.event_date, t.price, t.description, u.username 
            FROM tickets t 
            JOIN users u ON t.user_id = u.id 
            WHERE t.artist LIKE ? OR t.venue LIKE ? OR t.description LIKE ?
            ORDER BY t.created_at DESC
        ''', [f'%{search_query}%', f'%{search_query}%', f'%{search_query}%']).fetchall()
    else:
        # Show all tickets if no search
        tickets = db_conn.execute('''
            SELECT t.id, t.user_id, t.artist, t.venue, t.event_date, t.price, t.description, u.username, c.name as category_name
            FROM tickets t 
            JOIN users u ON t.user_id = u.id 
            LEFT JOIN categories c ON t.category_id = c.id
            ORDER BY t.created_at DESC
        ''').fetchall()
    
    db_conn.close()
    count = len(tickets)
    return render_template("index.html", count=count, tickets=tickets, search_query=search_query)

@app.route("/new_ticket")
def new_ticket():
    if "username" not in session:
        return redirect("/login")
    categories = db.query("SELECT id, name FROM categories", [])
    return render_template("new_ticket.html", categories=categories)

@app.route("/send", methods=["POST"])
def send():
    if "username" not in session:
        return redirect("/login")
    check_csrf()

    artist = request.form["artist"]
    venue = request.form["venue"]
    event_date = request.form["event_date"]
    price = request.form["price"]
    description = request.form["description"]
    category_id = request.form["category_id"]

    if event_date < str(date.today()):
        return render_template("new_ticket.html", error="Et voi valita mennyttä päivämäärää")
    
    db_conn = sqlite3.connect("database.db")
    user = db_conn.execute("SELECT id FROM users WHERE username = ?", [session["username"]]).fetchone()
    
    if not user:
        db_conn.close()
        return render_template("login.html", error="Käyttäjää ei löytynyt")
    
    user_id = user[0]
    
    db_conn.execute("INSERT INTO tickets (user_id, artist, venue, event_date, price, category_id, description) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   [user_id, artist, venue, event_date, price, category_id, description])
    db_conn.commit()
    db_conn.close()
    return redirect("/")

# Delete ticket
@app.route("/delete/<int:ticket_id>", methods=["POST"])
def delete_ticket(ticket_id):
    if "username" not in session:
        return redirect("/login")
    check_csrf()

    db_conn = sqlite3.connect("database.db")
    
    # Check if the ticket belongs to the logged-in user
    user = db_conn.execute("SELECT id FROM users WHERE username = ?", [session["username"]]).fetchone()
    if user:

        db_conn.execute("DELETE FROM tickets WHERE id = ? AND user_id = ?", [ticket_id, user[0]])
        db_conn.commit()
    
    db_conn.close()
    return redirect("/")

# Edit ticket
@app.route("/edit/<int:ticket_id>")
def edit_ticket(ticket_id):
    if "username" not in session:
        return redirect("/login")

    db_conn = sqlite3.connect("database.db")
    db_conn.row_factory = sqlite3.Row
    # If you only need basic info for editing:
    ticket = db_conn.execute("""
        SELECT id, user_id, artist, venue, event_date, price, section, row, seat, description, category_id
        FROM tickets 
        WHERE id = ?
    """, [ticket_id]).fetchone()
    
    user = db_conn.execute("SELECT id FROM users WHERE username = ?", [session["username"]]).fetchone()
    
    # Check if the ticket belongs to the logged-in user
    if not ticket or not user or ticket['user_id'] != user[0]:
        db_conn.close()
        return render_template("login.html", error="Ei oikeutta muokata tätä lippua")
    
    categories = db.query("SELECT id, name FROM categories", [])

    db_conn.close()
    return render_template("edit.html", ticket=ticket, categories=categories)

@app.route("/update/<int:ticket_id>", methods=["POST"])
def update_ticket(ticket_id):
    if "username" not in session:
        return redirect("/login")
    check_csrf()

    artist = request.form["artist"]
    venue = request.form["venue"]
    event_date = request.form["event_date"]
    price = request.form["price"]
    description = request.form["description"]
    category_id = request.form["category_id"]

    db_conn = sqlite3.connect("database.db")
    db_conn.row_factory = sqlite3.Row
    user = db_conn.execute("SELECT id FROM users WHERE username = ?", [session["username"]]).fetchone()
    ticket = db_conn.execute("SELECT user_id FROM tickets WHERE id = ?", [ticket_id]).fetchone()

    # the date can't be in the past
    if event_date < str(date.today()):
        db_conn.close()
        return render_template("edit.html", error="Et voi valita mennyttä päivämäärää", ticket=ticket)
    
    if user and ticket and ticket["user_id"] == user[0]:
        db_conn.execute('''
            UPDATE tickets 
            SET artist=?, venue=?, event_date=?, price=?, description=?, category_id=?
            WHERE id=?
        ''', [artist, venue, event_date, price, description, category_id, ticket_id])
        db_conn.commit()
    
    db_conn.close()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)