# Bank App

## Overview

The Bank App simplifies managing your transactions by allowing you to effortlessly import CSV files into your accounts. By default, you will have 2 empty demo accounts:

- Debit
- Credit (with a credit limit up to -3,000)

Once imported, the data is securely stored in the database, ensuring the safety of your financial records.

### CSV Format

To import your data successfully, adhere to the following CSV structure:

Table view:

<table>
  <thead>
    <th>date</th>
    <th>description</th>
    <th>amount</th>
  </thead>
  <tbody>
    <tr>
      <td>
        2023-04-01
      </td>
      <td>
        income
      </td>
      <td>
        100000
      </td>
    </tr>
  </tbody>
</table>

Raw view:

date,description,amount</br>
2023-04-01,income,100000

Please ensure that the date format is as shown above. Other formats are not supported.

## Features

The Bank App offers the following features:

- Import transactions from CSV files into your accounts.
- Store and manage your transaction history in the database.
- Query your bank account to retrieve the balance on a specific date.
- Retrieve transactions within a specified date range.

## Installation

###### standard

Ensure you have Python 3.11.4 or above installed.

1. Clone this repository.
2. Navigate to the project directory.
3. Install dependencies: `pip install -r requirements.txt`

###### docker

`sudo docker pull parseltongist/bank_app`

## Usage

1. Prepare your transaction data in the required CSV format.
2. Run the Bank App using the provided command: `python3 bank_app` or `sudo docker run -it parseltongist/bank_app` if using Docker.
3. Follow the on-screen prompts to import your transactions and manage your accounts.

<details>
  <summary>
    <h2>
      Demo files
    </h2>
  </summary>
  Either version you chose, you can play with the following test file paths for upload:

`bank_app/tests/test_data/valid/transactions_1.csv`</br>
`bank_app/tests/test_data/valid/transactions_2.csv`</br>
`bank_app/tests/test_data/valid/transactions_3.csv`</br>

</details>
