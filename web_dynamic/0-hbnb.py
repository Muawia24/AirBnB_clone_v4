#!/usr/bin/python3
'''
starts a Flask web application
'''


from flask import Flask, render_template
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models import storage
import uuid
app = Flask(__name__)


@app.route('/0-hbnb/', strict_slashes=False)
def hbnb():
    """display a HTML page like 8-index.html from static"""
    states = storage.all("State").values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all("Amenity").values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    cache_id= uuid.uuid4()

    return render_template('0-hbnb.html', states=st_ct,
                           amenities=amenities, cache_id=cache_id)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
