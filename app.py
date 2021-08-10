import re
from flask import Flask, render_template,request, redirect, url_for
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
    finished_reading = db.Column(db.Boolean)
    purchase_date = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return  '<Book %r>' % self.id


#Create  a  route
@app.route('/')
@app.route('/books')
def books():
    books = Book.query.order_by(Book.created.desc()).all()
    return render_template("books.html", books=books)

# Add a new book
@app.route('/addbook', methods=['POST', 'GET'])
def addbook():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        genre = request.form['genre']
        language = request.form['language']

        book = Book(title=title, description=description, author=author, genre=genre, language=language)

        try:
            db.session.add(book)
            db.session.commit()
            return redirect("/")
        except:
            return "Could not add the book. Please try again."
    else:
        return render_template("addbook.html")

# Delete the book
@app.route('/books/<int:id>/delete')
def delete(id):
    book = Book.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        return redirect("/books")
    except:
        return "Could not delete the book. Please try again."

# Update a book
@app.route('/books/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    book = Book.query.get(id)
    if request.method == "POST":
        book.title = request.form['title']
        book.description = request.form['description']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.language = request.form['language']

        try:
            db.session.commit()
            return redirect("/books")
        except:
            return "Could not update the book. Please try again."
    else:
        return render_template("updatebook.html", book=book)


@app.route('/store')
def store():
    return render_template("store.html")



if __name__ == '__main__':
    app.run(debug=True)