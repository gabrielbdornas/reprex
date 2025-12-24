import requests
from authentication import create_api_key

def list_accounts(item_id: str):
    """
    List accounts associated with a specific item ID in Pluggy.
    See https://docs.pluggy.ai/reference/accounts-list
    Args:
        item_id (str): The ID of the item to list accounts for.
                       This ID can be obtained from the bank account connected at Pluggy application.
    Returns:
        dict: The response containing the list of accounts.
    """
    api_key = create_api_key()
    url = f'https://api.pluggy.ai/accounts?itemId={item_id}'

    headers = {
        'accept': 'application/json',
        'X-API-KEY': api_key
    }

    response = requests.get(url, headers=headers)
    return response.json()
