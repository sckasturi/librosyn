from app import app
from flask import jsonify, request, render_template, redirect
from pymongo import MongoClient
from json import loads as json
from bson.objectid import ObjectId
from app import utils

client = MongoClient()

@app.route('/submit', methods = ['GET'])
def submit_book():
    return render_template("submit.html", books = utils.get_books())

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
    return render_template("book.html", book = bookinfo, books = utils.get_books())
