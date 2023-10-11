import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    user = db.execute("SELECT username FROM users WHERE id=?", user_id)[0]["username"]  # username
    cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)[0]["cash"]  # user cash balance
    stocks_sum = 0  # variable for total value sum

    # find user data
    user_data = db.execute("SELECT Symbol FROM purchases WHERE user=? GROUP BY Symbol", user)

    # update user data
    for i in user_data:
        symbol = i["Symbol"]

        # number of shares user has
        user_shares_buy = db.execute("SELECT SUM(NumberOfShares) AS number FROM purchases WHERE user=? AND symbol=? AND type=?", user, symbol, "buy")[
            0]["number"]  # number of shares user bought
        user_shares_sell = db.execute("SELECT SUM(NumberOfShares) AS number FROM purchases WHERE user=? AND symbol=? AND type=?", user, symbol, "sell")[
            0]["number"]  # number of shares user sold
        if user_shares_sell == None:  # user hadn't sold stock yet
            user_shares_sell = 0
        user_shares_total = user_shares_buy - user_shares_sell  # total number of shares user currently has

        i["number"] = user_shares_total  # add shares number to the user data

        price = lookup(i["Symbol"])["price"]  # find stock price
        i["price"] = price  # add price to the user data
        i["total_value"] = price*i["number"]  # add total value to the user data
        i["name"] = lookup(i["Symbol"])["name"]  # add name of stock
        stocks_sum += i["total_value"]  # update total value sum

    grand_total = cash + stocks_sum  # all of user money worth
    user_data2 = [x for x in user_data if x["number"] > 0]  # remove stocks with no cuurent share number

    return render_template("index.html", user_data=user_data2, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # no symbol was inserted
        if not symbol:
            return apology("must provide symbol", 400)

        # symbol does not exist
        elif lookup(symbol) == None:
            return apology("symbol does not exist", 400)

        # no shares number was inserted
        elif not shares:
            return apology("must provide number of shares", 400)

        # shares is not all numeric characters
        elif shares.isnumeric() == False:
            return apology("number of shares must be a positive integer", 400)

        # input is valid
        else:
            shares = int(shares)  # shares is a number, convert from str to int
            share_price = lookup(symbol)["price"]  # find share price
            share_total = share_price*shares  # calculate total price of purchase
            user_money = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[
                0]["cash"]  # how much money does the user currently have

            # check if enough money
            # not enough money
            if share_total > user_money:
                return apology("you do not have enough money for this purchase", 400)

            # enough money
            else:

                # add purchase to table purchases
                user_name = str(db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"])
                time = db.execute("SELECT CURRENT_TIMESTAMP")[0]["CURRENT_TIMESTAMP"]
                db.execute("INSERT INTO purchases (user, name, symbol, type, numberofshares, priceforshare, totalprice, timeofpurchase) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           user_name, lookup(symbol)["name"], lookup(symbol)["symbol"], "buy", shares, share_price, share_total, time)

                # update user cash in table users
                cash = float(db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]) - share_total
                db.execute("UPDATE users SET cash=? WHERE id=?", cash, session["user_id"])

                return index()

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]  # username
    user_data = db.execute(
        "SELECT name, symbol, numberofshares, totalprice, type, timeofpurchase FROM purchases WHERE user=? ORDER BY timeofpurchase DESC", user)

    return render_template("history.html", user_data=user_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    symbol = request.form.get("symbol")  # stock symbol

    if request.method == "POST":

        if not symbol:  # symbol was not provided
            return apology("must provide symbol", 400)

        elif lookup(symbol) == None:  # symbol does not exists
            return apology("must provide valid symbol", 400)

        else:
            return render_template("quoted.html", symbol=lookup(symbol))

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password was confirmed
        elif not confirmation:
            return apology("must confirm password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username does not exists and password is correct and confirmed
        if len(rows) != 0:
            return apology("Username already taken", 400)

        elif confirmation != password:
            return apology("password is not confirmed", 400)

        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username,
                       generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        user_name = str(db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"])

        # no symbol was inserted
        if not symbol:
            return apology("must provide symbol", 400)

        # no shares number was inserted
        elif not shares:
            return apology("must provide number of shares", 400)

        # shares number is not a positive integer
        elif not(shares > 0):
            return apology("number of shares must be a positive integer", 400)

        # input is valid
        else:
            share_price = lookup(symbol)["price"]  # current share price
            share_total = share_price*shares  # sale value
            user_shares_buy = db.execute("SELECT SUM(NumberOfShares) AS number FROM purchases WHERE user=? AND symbol=? AND type=?", user_name, symbol, "buy")[
                0]["number"]  # number of shares user bought
            user_shares_sell = db.execute("SELECT SUM(NumberOfShares) AS number FROM purchases WHERE user=? AND symbol=? AND type=?", user_name, symbol, "sell")[
                0]["number"]  # number of shares user sold
            if user_shares_sell == None:  # user hadn't sold stock yet
                user_shares_sell = 0
            user_shares_total = user_shares_buy - user_shares_sell  # total number of shares user currently has
            print(user_shares_sell)
            print(user_shares_total)

            # check if enough shares
            if shares > user_shares_total:
                return apology("you do not have enough shares for this sale", 400)

            else:

                # add sale to table purchases
                time = db.execute("SELECT CURRENT_TIMESTAMP")[0]["CURRENT_TIMESTAMP"]
                db.execute("INSERT INTO purchases (user, name, symbol, type, numberofshares, priceforshare, totalprice, timeofpurchase) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           user_name, lookup(symbol)["name"], lookup(symbol)["symbol"], "sell", shares, share_price, share_total, time)

                # update user cash in table users
                print(float(db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]))
                cash = float(db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]) + share_total
                print(cash)
                db.execute("UPDATE users SET cash=? WHERE id=?", cash, session["user_id"])

                return index()

    else:
        user = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]  # username

        # find user data of symbols
        user_data = db.execute("SELECT Symbol FROM purchases WHERE user=? GROUP BY Symbol", user)

        return render_template("sell.html", user_data=user_data)


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # user
        user = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]  # username
        currentpassword = request.form.get("currentpassword")
        newpassword = request.form.get("newpassword")
        confirmnewpassword = request.form.get("confirmnewpassword")

        # no password was inserted
        if not currentpassword:
            return apology("must provide current password", 403)

        # no new password was inserted
        elif not newpassword:
            return apology("must provide new password", 403)

        # no confirmation of new password was inserted
        elif not confirmnewpassword:
            return apology("must provide confirmation of new password", 403)

        # new password identical to current password
        elif newpassword == currentpassword:
            return apology("new password must be different from current password", 403)

        # confirmation of new password is not identical to new password
        elif confirmnewpassword != newpassword:
            return apology("confirmation of new password must be identical to new password", 403)

        # input is valid
        else:
            # update password in database
            db.execute("UPDATE users SET hash=? WHERE username=?", generate_password_hash(
                newpassword, method='pbkdf2:sha256', salt_length=8), user)

            return index()

    else:
        return render_template("changepassword.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
