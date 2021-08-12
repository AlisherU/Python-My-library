from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bs4 import BeautifulSoup
import requests

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
    finished_reading = db.Column(db.String(50))
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
        book.finished_reading = request.form['finished_reading']

        try:
            db.session.commit()
            return redirect("/books")
        except:
            return "Could not update the book. Please try again."
    else:
        return render_template("updatebook.html", book=book)

# Scaping  a book data
all_books = []
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
def get_page(url):
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def get_links(soup):
    links =[]
    listings = soup.find_all('a',{'class':'a-link-normal a-text-normal'})
    for link in listings:
        bk_lnk = link.get('href')
        base_url = 'https://www.amazon.co.jp'
        cmplt_lnk = base_url+ bk_lnk
        links.append(cmplt_lnk)
    return links

def get_info(links):
    for link in  links:
        res = requests.get(link, headers=HEADERS)
        book_data = BeautifulSoup(res.text, 'html.parser')

        book_link = link
        title = book_data.find(id="productTitle")
        if(title):
            title = title.text.strip()
        else:
            title =""
        price = book_data.find(class_="a-size-base a-color-price a-color-price")
        if(price):
            price = price.text.strip()
        else:
            price = ""
        author = book_data.find(class_="author notFaded")
        if(author):
            author = author.a.text.strip()
        book = {'title':title, "price":price, "author":author, "link":book_link}
        all_books.append(book)


@app.route('/store')
def store():
    URL = ('https://www.amazon.co.jp/-/en/s?k=programming+book+python&qid=1628584207&ref=sr_pg_1')

    try:
        all_links = get_links(get_page(URL))
        get_info(all_links)
    except:
        return "Could not get the book info"

    return render_template("scrape.html", books=all_books)


if __name__ == '__main__':
    app.run(debug=True)

# Headers for request
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
URL = ('https://www.amazon.co.jp/-/en/s?k=programming+book+python&qid=1628584207&ref=sr_pg_1')


# all_links = get_links(get_page(URL))
# get_info(all_links)
# print(all_books)


# url_single = 'https://www.amazon.co.jp/-/en/Eyal-Wirsansky/dp/1838557741/ref=sr_1_18?dchild=1&keywords=programming+book+python&qid=1628662698&sr=8-18'
# res = requests.get(url_single,headers=HEADERS)
# data = BeautifulSoup(res.text, 'html.parser')
# price = data.find(class_="a-size-base a-color-price a-color-price").text.strip()
# title = data.find(class_="centerColumn").span.text.strip()
# author = data.find(class_="author notFaded").a.text.strip()
# print(author)



    # https://www.youtube.com/watch?v=VHi9pL0UJn8