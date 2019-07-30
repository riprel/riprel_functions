import logging
from flask import escape
import json
from src.client_plugins.common import initialise_client


def restaurant_search(request):
    """restaurant_search.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """

    logging.info('Getting restaurant list')

    # First, initialise the API client
    client = 'GOOGLE'
    client = initialise_client(client)

    loc = (51.517242, -0.093809)
    location_type = 'restaurant'
    language = 'en-GB'
    region = 'GB'
    radius = 1000
    min_price = 0
    max_price = 4
    open_now = True

    # Override defaults based on request args
    request_args = request.args
    if request_args and 'lat' in request_args and 'long' in request_args:
        loc = (request_args['lat'], request_args['long'])

    if request_args and 'search' in request_args:
        search_term = request_args['search']
    else:
        search_term = 'restaurant'

    print('location is ', loc)
    print('search query is', search_term)
    result = client.places_nearby(keyword=search_term, location=loc, radius=radius, min_price=min_price, max_price=max_price,
                                  open_now=open_now, type=location_type)

    print(result)

    hits = []
    if result and 'status' in result and result['status'] == 'OK':
        hits = [
            {
                r["place_id"]: {
                    "name": r['name'],
                    "vicinity": r['vicinity'],
                    "loc": r['geometry']["location"],
                    "rating": r['rating'],
                    "num_times_rated": r['user_ratings_total'],
                    "price_level": r["price_level"]
                }
            }
        for r in result['results'] if 'permanently_closed' not in r
        ]

    return json.dumps(hits)


if __name__ == "__main__":
    # Local testing
    from src.utils.local_func_runner import run_func_local
    run_func_local(restaurant_search)
