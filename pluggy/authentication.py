import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_api_key():
    """
    Create an API key for Pluggy authentication.
    See https://docs.pluggy.ai/reference/auth-create
    Returns:
        str: The API key as a string.
    """
    client_id = os.environ.get('PLUGGY_CLIENT_ID')
    client_secret = os.environ.get('PLUGGY_CLIENT_SECRET')
    url = 'https://api.pluggy.ai/auth'
    payload = {
        'clientId': client_id,
        'clientSecret': client_secret,
    }
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()['apiKey']
