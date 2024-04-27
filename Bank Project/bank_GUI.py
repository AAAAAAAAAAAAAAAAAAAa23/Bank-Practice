import mysql
import tkinter as tk
from tkinter import messagebox
import bank  # Import banking functions from bank.py

# Establish a connection to the database
connection = mysql.connector.connect(user='root', database='bank', password='password123')
cursor = connection.cursor()

# Function to create a new account
def createAccount():
    # Function to handle account submission
    def submitAccount():
        name = name_entry.get()
        pin = pin_entry.get()
        account_number = bank.generateAccountNumber()

        bank.createAccount(name, pin,account_number)
        

        messagebox.showinfo("Account Created", f"Account created successfully! Account Number: {account_number}")

    # Create a new window for account creation
    create_window = tk.Toplevel(root)
    create_window.title("Create New Account")

    # Labels and entry fields for name and PIN
    tk.Label(create_window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(create_window, text="PIN (4-digit):").grid(row=1, column=0, padx=10, pady=5)

    name_entry = tk.Entry(create_window)
    pin_entry = tk.Entry(create_window, show="*")

    name_entry.grid(row=0, column=1, padx=10, pady=5)
    pin_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to submit account details
    submit_button = tk.Button(create_window, text="Create Account", command=submitAccount)
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

# Function to deposit funds into an account
def depositFunds():
    # Function to handle deposit submission
    def submitDeposit():
        account_number = account_entry.get()
        amount = float(amount_entry.get())

        bank.depositFunds(account_number, amount)

        messagebox.showinfo("Deposit Successful", "Deposit successful!")

    # Create a new window for deposit
    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit Funds")

    # Labels and entry fields for account number and amount
    tk.Label(deposit_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(deposit_window, text="Amount:").grid(row=1, column=0, padx=10, pady=5)

    account_entry = tk.Entry(deposit_window)
    amount_entry = tk.Entry(deposit_window)

    account_entry.grid(row=0, column=1, padx=10, pady=5)
    amount_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to submit deposit
    submit_button = tk.Button(deposit_window, text="Deposit", command=submitDeposit)
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

# Function to withdraw funds from an account
def withdrawFunds():
    # Function to handle withdrawal submission
    def submitWithdraw():
        account_number = account_entry.get()
        amount = float(amount_entry.get())

        bank.withdrawFunds(account_number, amount)

        messagebox.showinfo("Withdrawal Successful", "Withdrawal successful!")

    # Create a new window for withdrawal
    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw Funds")

    # Labels and entry fields for account number and amount
    tk.Label(withdraw_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(withdraw_window, text="Amount:").grid(row=1, column=0, padx=10, pady=5)

    account_entry = tk.Entry(withdraw_window)
    amount_entry = tk.Entry(withdraw_window)

    account_entry.grid(row=0, column=1, padx=10, pady=5)
    amount_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to submit withdrawal
    submit_button = tk.Button(withdraw_window, text="Withdraw", command=submitWithdraw)
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

# Function to display account information
def displayAccountInfo():
    # Function to show account information
    def showAccount():
        account_number = account_entry.get()

        account_info = bank.displayAccountInfoN(account_number)

        if account_info:
            messagebox.showinfo("Account Information", 
                                f"Name: {account_info[0]}\nAccount Number: {account_info[1]}\nPIN: {account_info[2]}\nBalance: ${account_info[3]:.2f}")
        else:
            messagebox.showwarning("Account Not Found", "Account not found.")

    # Create a new window for account information
    info_window = tk.Toplevel(root)
    info_window.title("Display Account Information")

    # Label and entry field for account number
    tk.Label(info_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)

    account_entry = tk.Entry(info_window)
    account_entry.grid(row=0, column=1, padx=10, pady=5)

    # Button to display account information
    submit_button = tk.Button(info_window, text="Display", command=showAccount)
    submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

# Function to look up account information
def accountLookUp():
    # Function to show account information
    def showAccount():
        name = name_entry.get()
        pin = pin_entry.get()

        account_info = bank.getAccountInfo(name, pin)

        if account_info:
            messagebox.showinfo("Account Information", 
                                f"Name: {account_info[0]}\nAccount Number: {account_info[1]}\nPIN: {account_info[2]}\nBalance: ${account_info[3]:.2f}")
        else:
            messagebox.showwarning("Account Not Found", "No account found matching the provided details.")

    # Create a new window for account lookup
    lookup_window = tk.Toplevel(root)
    lookup_window.title("Account Look Up")

    # Labels and entry fields for name and PIN
    tk.Label(lookup_window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(lookup_window, text="PIN:").grid(row=1, column=0, padx=10, pady=5)

    name_entry = tk.Entry(lookup_window)
    pin_entry = tk.Entry(lookup_window)

    name_entry.grid(row=0, column=1, padx=10, pady=5)
    pin_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to look up account
    submit_button = tk.Button(lookup_window, text="Look Up Account", command=showAccount)
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

# Function to delete an account
def deleteAccount():
    # Function to confirm account deletion
    def confirmDelete():
        name = name_entry.get()
        account_number = account_entry.get()
        pin_number = pin_entry.get()

        result = bank.deleteAccount(name, account_number, pin_number)

        if result:
            messagebox.showinfo("Account Deleted", "Account deleted successfully.")
        else:
            messagebox.showwarning("Account Not Found", "No account found matching the provided details.")

    # Create a new window for account deletion
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Account")

    # Labels and entry fields for name, account number, and PIN
    tk.Label(delete_window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(delete_window, text="Account Number:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(delete_window, text="PIN:").grid(row=2, column=0, padx=10, pady=5)

    name_entry = tk.Entry(delete_window)
    account_entry = tk.Entry(delete_window)
    pin_entry = tk.Entry(delete_window)

    name_entry.grid(row=0, column=1, padx=10, pady=5)
    account_entry.grid(row=1, column=1, padx=10, pady=5)
    pin_entry.grid(row=2, column=1, padx=10, pady=5)

    # Button to delete account
    submit_button = tk.Button(delete_window, text="Delete Account", command=confirmDelete)
    submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

# Function to close the bank connection
def closeBank():
    bank.cursor.close()
    bank.connection.close()

# Create the main GUI window
root = tk.Tk()
root.title("Banking System")

# Set protocol to close connection when main window is closed
root.protocol("WM_DELETE_WINDOW", closeBank())

# Create buttons for different banking operations
tk.Button(root, text="Create New Account", command=createAccount).pack(pady=10)
tk.Button(root, text="Deposit Funds", command=depositFunds).pack(pady=10)
tk.Button(root, text="Withdraw Funds", command=withdrawFunds).pack(pady=10)
tk.Button(root, text="Display Account Information", command=displayAccountInfo).pack(pady=10)
tk.Button(root, text="Delete Account", command=deleteAccount).pack(pady=10)
tk.Button(root, text="Look Up Account", command=accountLookUp).pack(pady=10)

# Start the main event loop
root.mainloop()
