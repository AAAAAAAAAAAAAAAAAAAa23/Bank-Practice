import mysql.connector
import random

connection = mysql.connector.connect(user='root', database='bank', password='password123')
cursor = connection.cursor()

# Function to create a new bank account in the database
def createAccount(nameFromGUI, pinFromGUI,account_numFromGUI):
    connection = mysql.connector.connect(user='root', database='bank', password='password123')
    cursor = connection.cursor()
    name = nameFromGUI
    pin = pinFromGUI
    account_number = account_numFromGUI  # Generate a unique account number
    balance = 0.0  # Initial balance for new account

    # Insert account details into the database
    insert_query = "INSERT INTO bank_data (name, account_number, pin, balance) VALUES (%s, %s, %s, %s)"
    account_data = (name, account_number, pin, balance)

    cursor.execute(insert_query, account_data)
    connection.commit()

    print(f"Account created successfully! Account Number: {account_number}")
    cursor.close()
    connection.close()

# Function to generate a random 8-digit account number
def generateAccountNumber():
    return ''.join(str(random.randint(0, 9)) for _ in range(8))

# Function to deposit funds into an existing bank account
def depositFunds(account_numberFromGUI, amountFromGUI):
    connection = mysql.connector.connect(user='root', database='bank', password='password123')
    cursor = connection.cursor()
    account_number = account_numberFromGUI
    amount = float(amountFromGUI)

    # Update the balance in the database
    update_query = "UPDATE bank_data SET balance = balance + %s WHERE account_number = %s"
    cursor.execute(update_query, (amount, account_number))
    connection.commit()

    # Fetch and display the updated balance
    check_balance_query = "SELECT balance FROM bank_data WHERE account_number = %s"
    cursor.execute(check_balance_query, (account_number,))  # Typo: should be cursor.execute
    updated_balance = cursor.fetchone()[0]
    print("Deposit successful!")
    print(f"Your new balance ${updated_balance:.2f}")
    cursor.close()
    connection.close()

# Function to withdraw funds from an existing bank account
def withdrawFunds(account_numberFromGUI, amountFromGUI):
    connection = mysql.connector.connect(user='root', database='bank', password='password123')
    cursor = connection.cursor()
    account_number = account_numberFromGUI
    amount = float(amountFromGUI)

    # Check if there's enough balance to withdraw
    check_balance_query = "SELECT balance FROM bank_data WHERE account_number = %s"
    cursor.execute(check_balance_query, (account_number,))
    result = cursor.fetchone()

    if result:
        current_balance = result[0]
        if current_balance >= amount:
            # Update the balance in the database
            update_query = "UPDATE bank_data SET balance = balance - %s WHERE account_number = %s"
            cursor.execute(update_query, (amount, account_number))
            connection.commit()

            # Fetch and display the updated balance
            cursor.execute(check_balance_query, (account_number,))
            updated_balance = cursor.fetchone()[0]
            print("Withdrawal successful!")
            print(f"Remaining balance ${updated_balance:.2f}")
        else:
            print("Insufficient funds for withdrawal.")
    else:
        print("Account not found.")
    cursor.close()
    connection.close()

# Function to display account information based on account number
def displayAccountInfoN(account_numberFromGUI):
    connection = mysql.connector.connect(user='root', database='bank', password='password123')
    cursor = connection.cursor()
    account_number = account_numberFromGUI

    # Look up the account details in the database
    check_account_query = "SELECT * FROM bank_data WHERE account_number = %s"
    cursor.execute(check_account_query, (account_number,))  # Typo: should be (account_number,)
    account_data = cursor.fetchone()

    if account_data:
        # Extract account information from the database
        account_info = {
            'Name': account_data[0],
            'Account Number': account_data[1],
            'Pin': account_data[2],
            'Balance': account_data[3]
        }
        print("Account information")
        for key, value in account_info.items():
            print(f"{key}: {value}")
    else:
        print("Account not found.")
    cursor.close()
    connection.close()

# Function to delete an account from the database
def deleteAccount(nameFromGUI, account_numberFromGUI, pin_numberFROMGUI):
    connection = mysql.connector.connect(user='root', database='bank', password='password123')
    cursor = connection.cursor()
    name = nameFromGUI
    account_number = account_numberFromGUI
    pin_number = pin_numberFROMGUI

    double_check = input("Are you sure you want to delete your account? (Y/N): ")


    #Delete the account from the database
    delete_account_query = "DELETE FROM bank_data WHERE name = %s AND account_number = %s AND pin = %s"

    try:
        cursor.execute(delete_account_query, (name, account_number, pin_number))
        connection.commit()

        if cursor.rowcount > 0:
            print("Account deleted successfully.")
        else:
            print("No account found matching the provided details.")
    except mysql.connector.Error as err:
            print(f"Error: {err}")

    cursor.close()
    connection.close()

# Function to look up account based on name and PIN
def accountLookUp(nameFromGUI, pinFromGUI):
    connection = mysql.connector.connect(user='root', database='bank', password='password123')
    cursor = connection.cursor()
    name = nameFromGUI
    pin = pinFromGUI

    # Find the account based on name and pin
    find_account_query = "SELECT * FROM bank_data WHERE name = %s AND pin = %s"
    cursor.execute(find_account_query, (name, pin))
    account_data = cursor.fetchone()

    if account_data:
        # Extract account information from the database
        account_info = {
            'Name': account_data[0],
            'Account Number': account_data[1],
            'Pin': account_data[2],
            'Balance': account_data[3]
        }
        print("Account information")
        for key, value in account_info.items():
            print(f"{key}: {value}")
    else:
        print("Account not found.")
    cursor.close()
    connection.close()
