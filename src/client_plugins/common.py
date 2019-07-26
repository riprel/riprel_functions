from src.client_plugins.client_constants import available_clients


def initialise_client(client_to_use):
    try:
        return available_clients[client_to_use]()
    except KeyError as e:
        # TODO: send response client not supported
        raise e
