from requests import get
from bs4 import BeautifulSoup

def zipdist(zip1, zip2):
    key = "Eax38iUS77nNRQNbDZNTGEM16WV0CHYhRvk0OeTWmhJd8xpLwdEcRreYo9Z1QXiI"
    r = get("http://www.zipcodeapi.com/rest/%s/distance.json/%s/%s/mile" % (key, zip1, zip2))
    return r.json()["distance"]

def bookinfo(title, author):
    info = get("http://www.isbnsearch.org/search", params={"s":title})
    soup = BeautifulSoup(info.text, 'html.parser')
    p = soup.find_all('p')
    a = soup.find_all('a')
    #if(p[3].string.split(': ')[1].lower() != author.lower()):
    #    return None
    book = {
        "title": a[2].string,
        "author": p[3].string.split(': ')[1],
	"image": soup.img['src'].replace("75", "250"),
	"isbn": soup.find_all('p')[2].string,
        "zip": None,
        "email": None
    }
    return book
