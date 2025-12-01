import sqlite3
from flask import Flask
from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import session
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

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
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    # Redirect to login after registration
    return redirect("/login")

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
            SELECT t.id, t.user_id, t.artist, t.venue, t.event_date, t.price, t.description, u.username 
            FROM tickets t 
            JOIN users u ON t.user_id = u.id 
            ORDER BY t.created_at DESC
        ''').fetchall()
    
    db_conn.close()
    count = len(tickets)
    return render_template("index.html", count=count, tickets=tickets, search_query=search_query)

@app.route("/new")
def new():
    if "username" not in session:
        return redirect("/login")
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    if "username" not in session:
        return redirect("/login")
    
    artist = request.form["artist"]
    venue = request.form["venue"]
    event_date = request.form["event_date"]
    price = request.form["price"]
    description = request.form["description"]
    
    db_conn = sqlite3.connect("database.db")
    user = db_conn.execute("SELECT id FROM users WHERE username = ?", [session["username"]]).fetchone()
    
    if not user:
        db_conn.close()
        return "Käyttäjää ei löytynyt"
    
    user_id = user[0]
    
    db_conn.execute("INSERT INTO tickets (user_id, artist, venue, event_date, price, description) VALUES (?, ?, ?, ?, ?, ?)", 
                   [user_id, artist, venue, event_date, price, description])
    db_conn.commit()
    db_conn.close()
    return redirect("/")

# FIX 4: Add delete function
@app.route("/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    if "username" not in session:
        return redirect("/login")
    
    db_conn = sqlite3.connect("database.db")
    
    # Check if the ticket belongs to the logged-in user
    user = db_conn.execute("SELECT id FROM users WHERE username = ?", [session["username"]]).fetchone()
    if user:
        db_conn.execute("DELETE FROM tickets WHERE id = ? AND user_id = ?", [ticket_id, user[0]])
        db_conn.commit()
    
    db_conn.close()
    return redirect("/")

# FIX 4: Add edit function
@app.route("/edit/<int:ticket_id>")
def edit_ticket(ticket_id):
    if "username" not in session:
        return redirect("/login")
    
    db_conn = sqlite3.connect("database.db")
    db_conn.row_factory = sqlite3.Row
    # If you only need basic info for editing:
    ticket = db_conn.execute("""
        SELECT id, user_id, artist, venue, event_date, price, section, row, seat, description
        FROM tickets 
        WHERE id = ?
    """, [ticket_id]).fetchone()
    user = db_conn.execute("SELECT id FROM users WHERE username = ?", [session["username"]]).fetchone()
    
    # Check if the ticket belongs to the logged-in user
    if not ticket or not user or ticket['user_id'] != user[0]:
        db_conn.close()
        return "Ei oikeutta muokata tätä lippua"
    
    db_conn.close()
    return render_template("edit.html", ticket=ticket)

@app.route("/update/<int:ticket_id>", methods=["POST"])
def update_ticket(ticket_id):
    if "username" not in session:
        return redirect("/login")
    
    artist = request.form["artist"]
    venue = request.form["venue"]
    event_date = request.form["event_date"]
    price = request.form["price"]
    description = request.form["description"]
    
    db_conn = sqlite3.connect("database.db")
    user = db_conn.execute("SELECT id FROM users WHERE username = ?", [session["username"]]).fetchone()
    
    if user:
        db_conn.execute('''
            UPDATE tickets 
            SET artist=?, venue=?, event_date=?, price=?, description=?
            WHERE id=? AND user_id=?
        ''', [artist, venue, event_date, price, description, ticket_id, user[0]])
        db_conn.commit()
    
    db_conn.close()
    return redirect("/")
    
    # Check ownership before updating
    ticket = db_conn.execute("SELECT user_id FROM tickets WHERE id = ?", [ticket_id]).fetchone()
    if ticket and user and ticket[0] == user[0]:
        db_conn.execute('''
            UPDATE tickets 
            SET artist=?, venue=?, event_date=?, price=?, description=?
            WHERE id=?
        ''', [artist, venue, event_date, price, description, ticket_id])
        db_conn.commit()
    
    db_conn.close()
    return redirect("/")
