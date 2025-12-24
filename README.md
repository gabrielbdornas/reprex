# Pluggy API Usage

Some finds about pluggy API.

- The `pluggy.authentication.create_api_key` function needs pluggy app `client_id` and `client_secret`.
- When you create plyggy account you get access to its panel. To create an app just go to the `Aplications` tab and select `New`.
- Selecting `Preview in Demo` you're going to be redirect to a new panel, where it is possible to connect bank accounts.
- All accont connected creates a new `item_id`.
- This `item_it` will be used to list all accounts (BANK, CREDIT) related to this `item_id`.
- The `pluggy.accounts.list_accounts` function needs the `item_id` to retrieve accounts (BANK, CREDIT) information.
- The `pluggy.transactions.list_transactions` functions needs the `account_id` to list accounts (BANK, CREDIT) transactions.
- Transactions:
    - All transactions have unique identifiers.
    - Credit Transactions:
        - Paid bills have `creditCardMetadata.billId` metadata created.
        - The available `status` metadata are `POSTED` and `PENDING`, meaning paid and not paid respectivaly.
        - The `providerId` could be another identifier, been just the last two digits differents for installment purchases.
        - Installment bills have:
            - `date` metadata with:
                - The date (month) when that installment will be pay (when it isn't the first).
                - The purchase date when it is the first.
            - The `creditCardMetadata.installmentNumber` metadata give the installment number to
            - The `providerId` metadata is almost identical from the second transactions to the last, been just the last two digits differents, or equal to the installment number. The first transactions doesn't follow this role.
            - The `creditCardMetadata.purchaseDate` metadata is another identifier because it will be almost impossible to be similar to olher transactions.
- I need a table with:
    - account_name: `accounts['results'][i]['name']`.
    - account_type: `accounts['results'][i]['subtype']`.
    - transaction_id: `transaction['results'][i]['id']`.
    - description: `transaction['results'][i]['description']`.
    - amount: `transaction['results'][i]['amount']`.
    - date: `transaction['results'][i]['date']`.
    - purchase_date: `transaction['results'][i]['creditCardMetadata']['purchaseDate']` (if it exists).
    - total_installments: `transaction['results'][i]['creditCardMetadata']['totalInstallments']` (if it exists).
    - installment_number: `transaction['results'][i]['creditCardMetadata']['installmentNumber']` (if it exists).
    - status: `transaction['results'][i]['status']`.
    - provider: `transaction['results'][i]['provider']`
