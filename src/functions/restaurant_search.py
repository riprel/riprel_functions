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

    loc = (51.5070858, -0.0936576)
    type = 'restaurant'
    language = 'en-GB'
    region = 'GB'
    radius = 5000

    # Override defaults based on request args
    request_args = request.args
    if request_args and 'lat' in request_args and 'long' in request_args:
        loc = (request_args['lat'], request_args['long'])

    if request_args and 'search' in request_args:
        name = request_args['search']
    else:
        name = 'restaurant'

    print('location is ', loc)
    print('search query is', name)
    result = client.places(name, location=loc, radius=radius, min_price=0, max_price=4, open_now=True, type=type)

    print(result)

    hits = []
    if result and ('status' in result) and result['status'] == 'OK' :
        hits = [{"name" : r['name'], "address" : r['formatted_address'], "rating" : r['rating']} for r in result['results']]

    return 'Hello {}!'.format(escape(json.dumps(hits)) )


if __name__ == "__main__":
    # Local testing
    from src.utils.local_func_runner import run_func_local
    run_func_local(restaurant_search)
