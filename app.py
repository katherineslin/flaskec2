from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#import os

app = Flask(__name__)

# app.config.update(
#     dict(
#         DEBUG=True,
#         SECRET_KEY="development key",
#         USERNAME="admin",
#         PASSWORD="default",
#         SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.root_path, "data.db"),
#     )
# ) 
# app.config.from_envvar("FLASKR_SETTINGS", silent=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@flaskdb.c9y0e04oggmv.us-east-1.rds.amazonaws.com/flaskaws'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "development key"

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

# db.init_app(app)


# @app.cli.command("initdb")
# def initdb_command():
#     """Creates the database tables."""
#     db.create_all()
#     print("Initialized the database.")

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add/', methods =['POST'])
def insert_book():
    if request.method == 'POST':
        book = Book(
            title= request.form.get('title'),
            author= request.form.get('author'),
            price= request.form.get('price')
        )
        db.session.add(book)
        db.session.commit()
        flash('added a new book')
    return redirect(url_for('index'))

@app.route('/update/', methods =['POST'])
def update():
    if request.method == 'POST':
        my_data = Book.query.get(request.form.get('id'))
        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.price = request.form['price']
        db.session.commit()
        flash('updated book')
    return redirect(url_for('index'))


@app.route('/delete/<id>/', methods =['GET', 'POST'])
def delete(id):
    my_data = Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('deleted book')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
