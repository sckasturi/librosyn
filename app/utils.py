from requests import get
from bs4 import BeautifulSoup
from pymongo import MongoClient
from random import sample

client = MongoClient()
user_agent = {'User-agent': 'Mozilla/5.0'}

def zipdist(zip1, zip2):
    key = "xrRYz3NfwfqrytVGxJOhVT71VOagMfvjHmihq6wWlWoTpjAX2ofYhn0dbbtYrYh8"
    r = get("http://www.zipcodeapi.com/rest/%s/distance.json/%s/%s/mile" % (key, zip1, zip2))
    return r.json()["distance"]

def bookinfo(title, author):
    info = get("http://www.isbnsearch.org/search", params={"s":title})
    soup = BeautifulSoup(info.text, 'html.parser')
    p = soup.find_all('p', limit=4)
    a = soup.find_all('a', limit=4)
    isbns = soup.find_all(class_='isbn')
    book = {
        "title": a[2].string,
        "author": p[3].string.split(': ')[1],
	    "image": soup.img['src'].replace("75", "250"),
        "isbn": isbns[0].string.split(': ')[1],
        "desc": finddesc(isbns[1].string.split(': ')[1]),
        "isbn10": isbns[1].string.split(': ')[1]
    }
    return book

def finddesc(isbn):
    info = get('http://www.amazon.com/gp/product/%s' % isbn, headers = user_agent)
    soup = BeautifulSoup(info.text, 'html.parser')
    desc = soup.find_all('noscript')[1].getText().strip()
    desc = (desc[:500] + "...") if len(desc) > 500 else desc
    return desc

def get_books():
    db = client.librosyn
    books = []
    book_list = db.books.find()
    for i in book_list:
        books.append(i)
    return sample(books, 5)
