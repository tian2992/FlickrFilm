import os
import re
from flask import Flask
from flask import render_template

app = Flask(__name__)

import flickrapi

USER_ID = "12983620@N00"
API_KEY = "70ee1002979542fbca5710bba213f39b"
flickr = flickrapi.FlickrAPI(API_KEY)

def build_url(photo, size):
    return "http://farm{0}.static.flickr.com/{1}/{2}_{3}_{4}.jpg".format(photo.get('farm'),photo.get('server'),
           photo.get('id'),photo.get('secret'),size)

def fetchRolls():
    photos = flickr.walk(user_id=USER_ID,tags="film",extras="tags")
    rolls = {}
    for p in photos:
        tags = p.get('tags').split()
        for tag in tags:
            if re.search(r'roll\d+',tag):
                roll_int = int(tag[4::])
                try:
                    rolls[roll_int].add(p)
                except KeyError:
                    rolls[roll_int] = set()
                    rolls[roll_int].add(p)
    return rolls

@app.route('/')
def index():
    rolls = fetchRolls()
    return render_template('index.html',film=rolls,user=USER_ID,url_builder=build_url)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


