import mysql.connector
import random


#connection = mysql.connector.connect(user = 'root', database = 'bank', password = 'password123')

#cursor = connection.cursor()

def createAccount(nameFromGUI, pinFromGUI):
    connection = mysql.connector.connect(user = 'root', database = 'bank', password = 'password123')
    cursor = connection.cursor()
    name = nameFromGUI
    pin = pinFromGUI
    account_number = generateAccountNumber()  # Generate a unique account number
    balance = 0.0  # Initial balance for new account

    # Insert account details into the database
    insert_query = "INSERT INTO bank_data (name, account_number, pin, balance) VALUES (%s, %s, %s, %s)"
    account_data = (name, account_number, pin, balance)

    cursor.execute(insert_query, account_data)
    connection.commit()

    print(f"Account created successfully! Account Number: {account_number}")
    cursor.close()
    connection.close()

def generateAccountNumber():
    return ''.join(str(random.randint(0, 9)) for _ in range(8))

def depositFunds(account_numberFromGUI, amountFromGUI):
    connection = mysql.connector.connect(user = 'root', database = 'bank', password = 'password123')
    cursor = connection.cursor()
    account_number = account_numberFromGUI
    amount = float(amountFromGUI)

    # Update the balance in the database
    update_query = "UPDATE bank_data SET balance = balance + %s WHERE account_number = %s"
    cursor.execute(update_query, (amount, account_number))
    connection.commit()

    # get da new balance 
    check_balance_query = "SELECT balance FROM bank_data WHERE account_number = %s"
    cursor.execut(check_balance_query, (account_number,))
    updated_balance = cursor.fetchone()[0]
    print("Deposit successful!")
    print(f"Your new balance ${updated_balance:.2f}")
    cursor.close()
    connection.close()

def withdrawFunds(account_numberFromGUI, amountFromGUI):
    connection = mysql.connector.connect(user = 'root', database = 'bank', password = 'password123')
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

            #get data from da table 
            cursor.execute(check_balance_query, (account_number,))
            updated_balance = cursor.fetchone()[0]
            print("Withdrawal successful!")
            print(f"Remaining balance ${updated_balance:.2f} ")
        else:
            print("Insufficient funds for withdrawal.")
    else:
        print("Account not found.")
    cursor.close()
    connection.close()

def displayAccountInfo(account_numberFromGUI):
    connection = mysql.connector.connect(user = 'root', database = 'bank', password = 'password123')
    cursor = connection.cursor()
    account_number = account_numberFromGUI

    #Look through the bank data and find the correct account
    check_account_query = "SELECT * FROM bank_data WHERE account_number = %s and Pin = %s"
    #Execute the SQL query with parameters
    cursor.execute(check_account_query, (account_number))
    #Fetch the respective row
    account_data = cursor.fetchone()

    if account_data:
        #Pull all informatoin in the table, table is setup with name, accountNum, Pin, balance
        account_info = { 'Name': account_data[0],
                         'Account Number': account_data[1],
                         'Pin': account_data[2],
                         'Balance': account_data[3]}
        print("Account information")
        for key, value in account_info.items():
            print(f"{key}: {value}")
    else:
        print("Wrong pin or account number")
    cursor.close()
    connection.close()

def deleteAccount(nameFromGUI, account_numberFromGUI, pin_numberFROMGUI):
    connection = mysql.connector.connect(user = 'root', database = 'bank', password = 'password123')
    cursor = connection.cursor()
    name = nameFromGUI
    account_number = account_numberFromGUI
    pin_number = pin_numberFROMGUI

    double_check = input("Are you sure you want to delete your account? (Y/N): ")

    if double_check.upper() == "Y":
        # Define the SQL query to delete the account based on name, account number, and PIN
        delete_account_query = "DELETE FROM bank_data WHERE name = %s AND account_number = %s AND pin = %s"

        try:
            # Execute the delete query with the specified parameters
            cursor.execute(delete_account_query, (name, account_number, pin_number))
            connection.commit()

            if cursor.rowcount > 0:
                print("Account deleted successfully.")
            else:
                print("No account found matching the provided details.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    else:
        print("Account deletion cancelled.")
    cursor.close()
    connection.close()

def accountLookUp(nameFromGUI, pinFromGUI):
    connection = mysql.connector.connect(user = 'root', database = 'bank', password = 'password123')
    cursor = connection.cursor()
    name = nameFromGUI
    pin = pinFromGUI

    #Find the account based on name and pin
    find_account_query = "SELECT * FROM bank_data WHERE name = %s AND pin = %s"
    #Execute the SQL query with parameters
    cursor.execute(find_account_query, (name, pin))
    #Fetch the account data
    account_data = cursor.fetchone()

    if account_data:
        #Pull all informatoin in the table, table is setup with name, accountNum, Pin, balance
        account_info = { 'Name': account_data[0],
                         'Account Number': account_data[1],
                         'Pin': account_data[2],
                         'Balance': account_data[3]}
        print("Account information")
        for key, value in account_info.items():
            print(f"{key}: {value}")
    else:
        print("Wrong name or pin")

    cursor.close()
    connection.close()

