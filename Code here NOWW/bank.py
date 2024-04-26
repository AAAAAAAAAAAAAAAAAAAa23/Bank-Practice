import mysql.connector
import random


connection = mysql.connector.connect(user = 'root', database = 'bank', password = 'password123')

cursor = connection.cursor()

def createAccount():
    name = input("Enter your name: ")
    pin = input("Set your 4-digit PIN: ")
    account_number = generateAccountNumber()  # Generate a unique account number
    balance = 0.0  # Initial balance for new account

    # Insert account details into the database
    insert_query = "INSERT INTO bank_data (name, account_number, pin, balance) VALUES (%s, %s, %s, %s)"
    account_data = (name, account_number, pin, balance)

    cursor.execute(insert_query, account_data)
    connection.commit()

    print(f"Account created successfully! Account Number: {account_number}")

def generateAccountNumber():
    return ''.join(str(random.randint(0, 9)) for _ in range(8))

def depositFunds():
    account_number = input("Enter your account number: ")
    amount = float(input("Enter deposit amount: "))

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

def withdrawFunds():
    account_number = input("Enter your account number: ")
    amount = float(input("Enter withdrawal amount: "))

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

def displayAccontInfo():
    account_number = input("Enter your account number: ")
    pin_number = input("Enter your pin number: ")

    #Look through the bank data and find the correct account
    check_account_query = "SELECT * FROM bank_data WHERE account_number = %s and Pin = %s"
    #Execute the SQL query with parameters
    cursor.execute(check_account_query, (account_number, pin_number))
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

while True:
    print("\nBanking System Menu:")
    print("1. Create Account")
    print("2. Deposit Funds")
    print("3. Withdraw Funds")
    print("4. Display account information")
    print("5. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        createAccount()
    elif choice == '2':
        depositFunds()
    elif choice == '3':
        withdrawFunds()
    elif choice == '4':
        displayAccontInfo()
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")

cursor.close()
connection.close()