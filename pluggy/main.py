import os
import csv
from dotenv import load_dotenv
from accounts import list_accounts
from transactions import list_transactions

load_dotenv()
# TODO: CONECT OTHER ACCOUNTS.
item_id = os.environ.get('ACCOUNT_ID_ITAU')
accounts = list_accounts(item_id)['results']
transactions = []
for account in accounts:
    account_id = account['id']
    print(f'fetching transactions for account {account['name']} - {account['subtype']}')
    # breakpoint() if account['name'] == 'PERSONNALITE MC BLACK PONTOS' else None
    accounts_list_transactions = list_transactions(account_id)['results']
    for transaction in accounts_list_transactions:
        print(f'fetching transaction id - {transaction['id']}')
        transactions.append({
            'account_id': account_id,
            'acount_name': account['name'],
            'account_type': account['subtype'],
            'transactions_id': transaction['id'],
            'description': transaction['description'],
            'amount': transaction['amount'],
            'date': transaction['date'],
            'purchase_date': transaction['creditCardMetadata']['purchaseDate'] if transaction.get('creditCardMetadata') and transaction['creditCardMetadata'].get('purchaseDate') else None,
            'total_installments': transaction['creditCardMetadata']['totalInstallments'] if transaction.get('creditCardMetadata') and transaction['creditCardMetadata'].get('totalInstallments') else None,
            'installment_number': transaction['creditCardMetadata']['installmentNumber'] if transaction.get('creditCardMetadata') and transaction['creditCardMetadata'].get('installmentNumber') else None,
            'status': transaction['status'],
            'provider': transaction.get('providerId', None),
        })

fieldnames = transactions[0].keys()
with open('transactions.csv', 'w', newline='', encoding='utf-8') as output_file:
    # Create a DictWriter object
    dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

    # Write the header row
    dict_writer.writeheader()

    # Write all the data rows
    dict_writer.writerows(transactions)
