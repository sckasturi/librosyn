from app import app
from flask import request, render_template, redirect
from pymongo import MongoClient
from app.utils import zipdist, get_books

client = MongoClient()

@app.route('/api/read', methods = ['GET'])
def read():
    query = request.args.to_dict()
    db = client.librosyn
    book = db.books.find_one({"title": query["title"].lower()})
    if not book["_id"]:
        return redirect('/books/none')
    return redirect('/books/' + str(book["_id"]) + '/' + str(query["zipcode"]))

@app.route('/')
def find_books():
   db = client.librosyn
   books = db.books.find()[:10]
   return render_template("index.html", books = get_books()) 
