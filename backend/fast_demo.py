from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from os import environ as environment_variables

import json
import pyrebase
from pyrebase.pyrebase import Database, PyreResponse
from urllib3.contrib.appengine import HTTPError
load_dotenv()

'''
    Features to add
    1) Access specific article
    2) Access most recent n articles
    3) Push article to list
'''

API_KEY = environment_variables["FIREBASE_API_KEY"]

API_CONFIG = {
  "apiKey": API_KEY,
  "authDomain": "disinfopractice.firebaseapp.com",
  "databaseURL": "https://disinfopractice-default-rtdb.firebaseio.com",
  "projectId": "disinfopractice",
  "storageBucket": "disinfopractice.firebasestorage.app",
  "messagingSenderId": "834128285827",
  "appId": "1:834128285827:web:486cffa240652d86550bb6",
  "measurementId": "G-KNXV99Q533"
}

app = FastAPI()
firebase = pyrebase.initialize_app(API_CONFIG)
db = firebase.database()

def get_country_articles(db: Database, country: str) -> Database:
    return db.child("countries").child(country).child("articles")

# url/articles/?country={ country }&name={ name }
@app.get("/articles/")
async def get_specific_article(name: str, country: str = "USA"):
    global db
    articles = get_country_articles(db, country)
    art = articles.child(name).get().val()
    if art is None:
        return {}
    return art

# url/articles/?country={ country }&name={ name }
@app.get("/recent/?country={ country }&n={ n }")
async def get_last_n_articles(n: int, country: str = "USA"):
    #
    #   TODO:
    #       Implement bounds checking
    #
    global db
    articles = iter( get_country_articles(db, country).get() )
    recent_articles = {}
    for i in range( n ):
        art: PyreResponse = next(articles)
        recent_articles[str(i)] = art.val()
    return recent_articles

# TODO:
#   Implement pushing to database
@app.post("/usa/articles/{article_data}")
async def post_article():
    raise HTTPException(status_code=501, detail="pushing to database not yet implemented")
