from flask import render_template
from cs50 import SQL


#project name
project_name = "Budget Manager"

# Sqlite object
db = SQL("sqlite:///project.db")

# status function
def status(message, status):
    return render_template("status.html", title=status, project_name=project_name, message=message, status=status)