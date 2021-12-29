from dash_application import dash_app
from flask import render_template

@dash_app.route("/")
def about():
    return render_template('about.html', title='About')
