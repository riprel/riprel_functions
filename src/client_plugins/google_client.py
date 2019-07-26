import googlemaps
from flask import escape
import json
import logging
import os


def init_g_client():
    """
    Function to initialise the Google Places API client to use in the functions.

    :return: instance of the google client
    """
    logging.info('Setting up the client')

    # setting up Defaults
    key = os.getenv('GOOGLE_KEY')
    return googlemaps.Client(key)
