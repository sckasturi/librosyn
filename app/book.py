from app import app
from flask import jsonify, request, render_template, redirect
from pymongo import MongoClient
from json import loads as json
from bson.objectid import ObjectId
from random import choice, sample
from app import utils

client = MongoClient()

#todo move to utils.py
def get_books():
    db = client.librosyn
    books = []
    #books_count = 10
    book_list = db.books.find()
    for i in book_list:
        books.append(i)
    #return [{"name": "hi", "desc": "hi", "_id": 1234}]
    return sample(books, 5)

#@app.route('/api/book', methods = ['POST'])
def bookger():
    input_ = request.form.to_dict()
    db = client.librosyn
    #input_["topics"] = input_["topics"].lower().replace(" ", "").split(",")
    #input_["topics"] = json(str(input_["topics"]).lower().replace("'","\""))
    input_["title"] = input_["title"].lower()
    db.books.insert(input_)
    del input_["_id"]
    return redirect("/")

@app.route('/submit', methods = ['GET'])
def submit_book():
    return render_template("submit.html", books = get_books())

@app.route('/book/<uid>')
@app.route('/books/<uid>')
@app.route('/book/<uid>/<zipc>')
@app.route('/books/<uid>/<zipc>')
def show_book(uid, zipc=None):
    db = client.librosyn
    books = []
    book = db.books.find_one({'_id': ObjectId(uid)})
    bookinfo = utils.bookinfo(book["title"], book["author"]) 
    #print(bookinfo)
    if zipc:
        bookinfo["zip"] = utils.zipdist(zipc, book["zipcode"]) 
    else:
        bookinfo["zip"] = "Unknown"
    bookinfo["email"] = book["email"]
    return render_template("book.html", book = bookinfo, books = get_books())
