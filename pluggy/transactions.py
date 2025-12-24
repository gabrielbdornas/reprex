import requests
from authentication import create_api_key

def list_transactions(account_id: str):
    """
    List transactions associated with a specific account ID in Pluggy.
    See https://docs.pluggy.ai/reference/transactions-list
    args:
        account_id (str): The ID of the account to list transactions for.
                          This ID can be obtained from the accounts module.
    Returns:
        dict: The response containing the list of transactions.
    """
    api_key = create_api_key()
    url = f'https://api.pluggy.ai/transactions?accountId={account_id}'

    headers = {
        'accept': 'application/json',
        'X-API-KEY': api_key
    }

    response = requests.get(url, headers=headers)
    return response.json()

