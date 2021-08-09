from datetime import timezone
from flask import Flask, render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mylib.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Database tables
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    language = db.Column(db.String(100))
    finished_reading = db.Column(db.Boolean, default=False)
    purchase_date = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return  '<Book %r>' % self.id


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



if __name__ == '__main__':
    app.run(debug=True)