from flask import Flask, render_template, request, session, redirect
from flask.helpers import url_for
from helpers import status, project_name, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '845ef897fd747e417dcd0266df0df23b'

# Global variables
types = [{"name":"income", "color":"success"}, {"name":"expense", "color":"danger"}] # Types list
keys = ["id", "type", "category", "sum", "date", "details"] # Tables headers
actions = ["add", "delete"] # Categories actions list

@app.route('/')
def opening_page():
    return render_template('opening_page.html', title='opening_page'.title(), project_name=project_name)

@app.route("/home")
def home():
    # User is logged in
    if 'username' in session:

        is_data = False # Checker if any data exists
        user_data = {} # Storage dictionary

        # Get user data
        for type in types:
            user_data[type["name"]] = (db.execute("SELECT * FROM ? WHERE type=? ORDER BY date DESC",
                                       session["username"], type["name"]))

            # Check if there is existing data
            if len(user_data[type["name"]]) != 0:
                is_data = True    

        # No existing data
        if not is_data:
            return render_template("home.html", title="home".title(), project_name=project_name,
                                    username=session['username'], user_data=None)

        # Existing data
        else:
            totals = {} # Storage dictionary
            # Get financial balance of each category
            for category in session["categories"]:
                amount = db.execute("SELECT SUM(sum) AS sum FROM ? WHERE category=?",
                                               session["username"], category)[0]["sum"]
                # Category has no financial balance
                if not amount:
                    continue
                # Category has financial balance, round results to 2 decimal points
                else:
                    totals[category] = round(amount, 2)

            return render_template("home.html", title="home".title(), project_name=project_name,
                                    username=session['username'], user_data=user_data,
                                    keys=keys[2:7], len_keys=len(keys[2:7]) + 1,
                                    categories= session["categories"], types=types, totals=totals)

    # User is not logged in
    else:
        return render_template("home.html", title="home".title(), project_name=project_name, username=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variables
        username = request.form.get("username")
        password = request.form.get("password")
        passwordConfirmation = request.form.get("passwordConfirmation")

        # Look for username
        if not username:
            return status("Must have username", "error")

        # Look for password
        elif not password:
            return status("Must have password", "error")

        # Look for password confirmation
        elif not passwordConfirmation:
            return status("Must confirm password", "error")

        # Query database for username
        rows = db.execute("SELECT username FROM users WHERE username=?", username)

        # Check if username alredy taken
        if len(rows) != 0:
            return status("Username already taken", "error")

        # validate password confirmation
        elif passwordConfirmation != password:
            return status("Passwords don't match", "error")

        # Input is valid
        else:

            # Add user data to database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                        username, generate_password_hash(password, method="pbkdf2:sha256"))

            # Create personal databases for user
            db.execute("CREATE TABLE ? (id INTEGER, type TEXT NOT NULL, category TEXT NOT NULL, sum FLOAT NOT NULL, date DATE NOT NULL, details TEXT NOT NULL, PRIMARY KEY(id))", username)
            db.execute("CREATE TABLE ? (list TEXT)", username + "_categories")

            return status("All is good! " + username + " is registered", "success")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('register.html', title='register'.title(), project_name=project_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variables
        username = request.form.get("username")
        password = request.form.get("password")

        # Look for username
        if not username:
            return status("Must have username", "error")

        # Look for password
        elif not password:
            return status("Must have password", "error")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username=?", username)

        # Check if username and password valid and match
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return status("Invalid username and/or password", "error")

        # Input is valid
        else:
            # Set session variables
            session["username"] = username
            session["categories"] = []

            # Get user categories from database
            categories = db.execute("SELECT * FROM ?", session["username"] + "_categories")

            # Add user categories to session variable
            if len(categories) != 0:
                for category in categories:
                    session["categories"].append(category["list"])

            return home()

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html', title='Log in', project_name=project_name)

@app.route('/logout')
def logout():
    # Clear session completely
    session.clear()
    return home()

@app.route('/add', methods=['GET', 'POST'])
def add():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variables
        category = request.form.get("category")
        sum = float(request.form.get("sum"))
        date = request.form.get("date")
        details = request.form.get("details")

        # Look for category
        if not category or category not in session["categories"]:
            return status("Must have valid category", "error")

        # Look for sum
        if not sum:
            return status("Must have sum", "error")
        
        # Determine type by sum
        if sum < 0 :
            type = "expense"

        else:
            type = "income"

        # Look for date
        if not date:
            return status("Must have date", "error")

        # input is valid
        # Insert data into user database
        db.execute("INSERT INTO ? (type, category, sum, date, details) VALUES(?, ?, ?, ?, ?)",
                    session["username"], type, category, sum, date, details)

        return redirect(url_for('home'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        today = datetime.today().date() # Today's date for defult date field
        return render_template('add.html', title='add'.title(), project_name=project_name,
                                categories=session["categories"], today=today)

@app.route('/delete')
def delete():
    row = request.args.get("row") # Set variable from received data
    
    # row is convertable to an int
    try:
        # Convert row
        int(row)

        # Delete row from database
        db.execute("DELETE FROM ? WHERE id=?", session["username"], row)
        
        # Redirect back to homepage
        return redirect(url_for("home"))
    
    # row isn't convertible to an int
    except:
        
        return status("Invalid row number","error")

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    row = request.args.get("row") # Set variable from received data
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # variables
        category = request.form.get("category")
        sum = float(request.form.get("sum"))
        date = request.form.get("date")
        details = request.form.get("details")

        # Look for category
        if not category or category not in session["categories"]:
            return status("Must have valid category", "error")

        # Look for sum
        if not sum:
            return status("Must have sum", "error")

        # Determine type by sum
        if sum < 0:
            type_ = "expense"
        else:
            type_ = "income"

        # Look for date
        if not date:
            return status("Must have date", "error")

        # input is valid
        # Update data in user database
        db.execute("UPDATE ? SET type=?, category=?, sum=?, date=?, details=? WHERE id=?",
                    session["username"], type_, category, sum, date, details, row)

        return redirect(url_for('home'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # row is convertable to an int
        try:
            # Convert row
            row = int(row)
            
            # Get row data
            row_data = db.execute("SELECT * FROM ? WHERE id=?", session['username'], row)[0]

            # Send row data to edit
            return render_template('edit.html', title='edit'.title(), project_name=project_name,
                                    categories=session["categories"], row_data=row_data, row=row)

        # row isn't convertible to an int
        except:
            # Return error
            return status("Invalid row number","error")

@app.route('/categories', methods=['GET', 'POST'])
def categories():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variables
        action = request.form.get("action")
        category = request.form.get("category")

        # look for action
        if not action or action not in actions:
            return status("Must have valid action", "error")

        # look for category
        if not category:
            return status("Must have valid category", "error")

        # Add category
        if action == "add":

            # Check if category already exists
            if category in session["categories"]:
                return status("Category already exists", "error")

            # input is valid
            # Insert data into user database
            db.execute("INSERT INTO ? (list) VALUES(?)", session["username"] + "_categories", category)

            # Update session list
            session["categories"].append(category)
            session.modified = True

            return redirect(url_for('home'))

        else:
            # Check if category exists
            if category not in session["categories"]:
                return status("Category does not exists", "error")

            # input is valid
            # Delete data from user database
            db.execute("DELETE FROM ? WHERE list=?", session["username"] + "_categories", category)

            # Update session list
            session["categories"].remove(category)
            session.modified = True

            return redirect(url_for('home'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('categories.html', title='categories'.title(), project_name=project_name, actions=actions,
                                categories=session["categories"])


# open with "python application.py"
if __name__ == '__main__':
    app.run(debug=True)
