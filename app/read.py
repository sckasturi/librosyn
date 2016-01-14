from app import app
from flask import jsonify, request, render_template, redirect
from pymongo import MongoClient
from random import choice
from json import loads as json
from app.book import get_books
from app.utils import zipdist
client = MongoClient()

@app.route('/api/read', methods = ['GET'])
def reader():
    query = request.args.to_dict()
    print(query)
    db = client.librosyn
    db.read.insert(query)
    del query["_id"]
    print(query)
    books = []
    query = json(str(query).lower().replace("'", "\""))
    print(query)
    empty_keys = [k for k,v in query.items() if len(v) < 1] 
    for i in empty_keys:
        del query[i]
    for books in db.books.find(query):
        books.append(book)
    if len(books) == 0:
        return redirect('/book/none')
    return redirect('/book/' + str(choice(books)["_id"]))

@app.route('/')
def find_books():
   db = client.librosyn
   books = db.books.find()[:10]
   #for i in db.books.find():
   #    if len(books) == 10:
   #        break
   #    books.append(i)
   return render_template("index.html", books = get_books()) 
