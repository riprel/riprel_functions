import googlemaps
from flask import escape
import json


def get_place_data(request):
    """get_place_data.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """

    print('setting up defaults')

    #setting up Defaults
    key = 'AIzaSyDTbR7fIIdPycA3IoyMWDMrYjIMsVyMOWs'
    client = googlemaps.Client(key)
    location = (51.5070858,-0.0936576)
    type = 'restaurant'
    language = 'en-GB'
    region = 'GB'
    radius = 5000



    request_args = request.args
    if request_args and 'lat' in request_args and 'long' in request_args:
        loc = (request_args['lat'],request_args['long'])
    else:
        loc = location

    if request_args and 'search' in request_args:
        name = request_args['search']
    else:
        name = 'restaurant'


    print('location is ', loc)
    print('searhc query is', name)
    result = client.places(name,location=loc,
                          radius=radius,
                          min_price=0, max_price=4, open_now=True,
                          type=type)

    print(result)

    hits = []
    if result and ('status' in result) and result['status'] == 'OK' :
        hits = [{"name" : r['name'], "address" : r['formatted_address'], "rating" : r['rating']} for r in result['results']]

    return 'Hello {}!'.format(escape(json.dumps(hits)) )


#for local test
if __name__ == "__main__":
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/')
    def index():
        return get_place_data(request)

    app.run('127.0.0.1', 8000, debug=True)