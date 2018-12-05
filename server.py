from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection_copy import connectToMySQL
app = Flask(__name__)
app.secret_key = "Keep it secret, keep it safe."
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result():
    mysql = connectToMySQL('survey')

    if len(request.form['username']) < 3:
        flash("Name must be at least three characters")
    if len(request.form['location']) < 1:
        flash("You must select a Dojo location")
    if len(request.form['favorite']) < 1:
        flash("You must select a favorite language")
    if len(request.form['comments']) > 180:
        flash("Your comments cannot exceed 180 characters")

    if '_flashes' in session.keys():
        return redirect('/')
    else:

        query = "INSERT INTO survey (name, gender, location, favorite, comments, created_at, updated_at) VALUES (%(name)s, %(gender)s, %(location)s, %(favorite)s, %(comments)s, NOW(), NOW());"

        data = {
            "name": request.form['username'],
            "gender": request.form['radio_select'],
            "location": request.form['location'],
            "favorite": request.form['favorite'],
            "comments": request.form['comments']
        }
        user_id = mysql.query_db(query, data)
        session['id'] = user_id

        return redirect('/show')

@app.route('/show')
def show_user():
    mysql = connectToMySQL('survey')

    query = " SELECT * FROM survey WHERE id=%(id)s"

    data = {
        "id": session['id']
    }

    user = mysql.query_db(query, data)

    return render_template('result.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)