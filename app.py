from flask import Flask, render_template,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mylib.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column('db.Integer', primary_key=True)

#Create  a  route 
@app.route('/')
@app.route('/books')
def books():
    return render_template("books.html")


@app.route('/addbook')
def addbook():
    return render_template("addbook.html")


@app.route('/store')
def store():
    return render_template("store.html")


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User Page:" + name + " - " + str(id)


if __name__ == '__main__':
    app.run(debug=True)