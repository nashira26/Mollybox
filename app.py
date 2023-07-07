import bcrypt
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = ?", username)

        if len(rows) == 0:
            # No matching user found
            return render_template("login.html", error="User not found")

        hashed_password = rows[0]["hash"]

        if bcrypt.checkpw(password.encode(), hashed_password):
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # flash logged in message
            flash("You've logged in.")

            # Redirect user to home page
            return redirect("/")
        else:
            # Redirect user to home page
            return render_template("login.html", error="Wrong password.")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # flash logged out message
    flash("You've logged out.")

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # user reached via post
    if request.method == "POST":

        # get username
        username = request.form.get("username")

        # get password
        password = request.form.get("password")

        # get confirmed password
        con_password = request.form.get("confirmation")

        # Validate input
        if not username or not password or not con_password:
            return render_template("register.html", error="Please fill in all fields.")

        if password != con_password:
            return render_template("register.html", error="Passwords do not match.")

        if len(password) < 8:
            return render_template("register.html", error="Password length must be atleast 8 characters")

        if len(password) > 15:
            return render_template("register.html", error="Password length must not exceed 15 characters")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # register user into db
        db.execute("INSERT INTO users (name, hash) VALUES(?, ?)",
                   username, hashed_password)
        id = db.execute("SELECT id FROM users WHERE name=?", username)[0]["id"]
        session["user_id"] = id

        # create a wishlist table for user
        table_name = "wish" + str(session["user_id"])
        db.execute(f"CREATE TABLE {table_name}(wish_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, seq_no INTEGER NOT NULL, movie TEXT NOT NULL, year INTEGER, genre TEXT, actors TEXT, rating INTEGER NOT NULL, comments TEXT)")

         # flash message
        flash("You've registered successfully.")

        # redirect to login
        return redirect("/login")
    else:
        #user reached via get
        return render_template("register.html")

@app.route("/")
@login_required
def index():
    """Show portfolio of schedules"""

    #extract user's ratings details
    user_rating = db.execute("SELECT * FROM ratings WHERE id=?", session["user_id"])

    #display the schedules table
    return render_template("index.html", user_rating=user_rating)

#create a new rating
@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == 'POST':

        #user reached via post
        movie = request.form.get("movie")
        year = request.form.get("year")
        genre = request.form.get("genre")
        actors = request.form.get("actors")
        rate = request.form.get("rate")
        comments = request.form.get("comments")

        rows = db.execute("SELECT * FROM ratings WHERE id=? AND movie=?", session["user_id"], movie)

        if len(rows) != 0:
            flash("Rating already exists.")
            return redirect("/")

        username = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])[0]["name"]

        #register rate details
        db.execute("INSERT INTO ratings (id, username, movie, year, genre, actors, rating, comments) VALUES(?,?,?,?,?,?,?,?)",
                   session["user_id"], username, movie, year, genre, actors, rate, comments)


        #extract user's ratings details
        user_rating = db.execute("SELECT * FROM ratings WHERE id=?", session["user_id"])

        flash("Added rating successfully")

        #display the srating table
        return render_template("index.html", user_rating=user_rating)

    else:
        #user reached via get
        return render_template("new.html")

#open existing rate as editable
@app.route("/edit", methods=["GET","POST"])
@login_required
def edit():
    if request.method == "POST":
        no = request.form.get("seq_no")
        # Fetch the rating record based on seq_no
        user_rating = db.execute("SELECT * FROM ratings WHERE seq_no=?", no)

        if len(user_rating) == 0:
            # No matching rating found
            flash("Rating not found.")
            return redirect("/")

        movie = request.form.get("movie")
        year = request.form.get("year")
        genre = request.form.get("genre")
        actors = request.form.get("actors")
        rate = request.form.get("rate")
        comments = request.form.get("comments")

        if not movie:
            flash("Please provide a movie name.")
            return redirect("/")

        # Update the rating details
        db.execute("UPDATE ratings SET movie=?, year=?, genre=?, actors=?, rating=?, comments=? WHERE seq_no=?",
                       movie, year, genre, actors, rate, comments, no)

        flash("Rating updated successfully.")

        return redirect("/")
    else:
        no = request.args.get("seq_no")
        user_rating = db.execute("SELECT * FROM ratings WHERE seq_no=?", no)

    # If the request method is GET or no rating is found, render the edit form
        return render_template("edit.html", user_rating=user_rating[0])

#delete a rating
@app.route("/delete", methods=["POST"])
@login_required
def delete():
    #user reached via post
    no = request.form.get("seq_no")
    db.execute("DELETE FROM ratings WHERE id=? AND seq_no=?", session["user_id"], no)
    flash("Rating deleted.")
    return redirect("/")


@app.route("/display")
@login_required
def display():
    all_ratings = db.execute("SELECT * FROM ratings")
    return render_template("display.html", ratings=all_ratings)

@app.route("/wish", methods=["GET","POST"])
@login_required
def wish():
    if request.method == "POST":
        table_name = "wish" + str(session["user_id"])
        no = request.form.get("seq_no")

        rows = db.execute(f"SELECT * FROM {table_name} WHERE seq_no=?", no)
        if len(rows) != 0:
            flash("Already added to wishlist!")
            return redirect("/wish")

        #update wishlist
        wished = db.execute("SELECT * FROM ratings WHERE seq_no=?", no)[0]
        db.execute(f"INSERT INTO {table_name} (seq_no, movie, year, genre, actors, rating, comments) VALUES(?,?,?,?,?,?,?)",
                   wished["seq_no"], wished["movie"], wished["year"], wished["genre"], wished["actors"], wished["rating"], wished["comments"])

        flash("Wishlist updated!")

        return redirect("/wish")

    #user gets through
    else:
        table_name = "wish"+str(session["user_id"])
        return render_template("wish.html", wishes=db.execute(f"SELECT * FROM {table_name}"))

@app.route("/remove", methods=["POST"])
@login_required
def remove():
    table_no = "wish" +str(session["user_id"])
    db.execute(f"DELETE FROM {table_no} WHERE wish_id=?", (request.form.get("wish_no"),))
    flash("Wishlist updated")
    return redirect("/wish")

