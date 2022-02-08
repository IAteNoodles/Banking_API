#A class which can be used to access account apis.
#This class is filled with only the base apis. Other features maybe added in future.
import mariadb

from Banking_.API.Accounts import Account
connector = mariadb.connect(user='User', password='User@Bank', database='Banking')
connection = connector.cursor()
class User:
    def __init__(self, user_id, password):
        from Hashing import sha3
        password = sha3(password)
        connection.execute("SELECT * FROM User WHERE ID = %s AND Password = %s", (user_id, password))
        if connection.fetchone() is None:
            return "Username or password is incorrect"
        
        self.user_id = user_id
        self.hash = password
        
        #Fetching the accounts linked to this user.
        connection.execute("SELECT * FROM Accounts WHERE User_ID = %s", (user_id))
        self.accounts = connection.fetchone()
        self.current_account: Account
    
    def login_account(self, account_id):
        """
        Logs in to an account.
        """
        
        print("Accounts related to this user are\n:")
        index = 1
        #Provides a list of the accounts linked to this user.
        for account in self.accounts:
            print(index+": " + account)
            index+=1
        
        #Asks the user to enter the account number to login.
        relative_account = int(input("Enter the account number to login: "))
        if relative_account > self.accounts or relative_account < 1:
            return "Invalid account number"
        
        #Asks the user to enter the password to login.
        password = input("Enter the password to login: ")
        
        print("Logging in...")
        
        #Checks if the account and password are correct.
        current_account = Account(self.accounts[relative_account-1], password)
        #Creates an account object with the given account number.         
        
        print("Logged in to account: " + account_id)
        
    def logout_account(self):
        """
        Logs out of the current account.
        """
        print("Logging out...")
        self.current_account = None
        print("Logged out.")
        
    def create_account(self, password):
        """
        Creates an account application, which will be sent to the bank for approval.
        
        Args:
            password: The password to be used for the account.
        
        Returns:
            The account number of the account created.
        """
        
        print("Generating account application for you...")
        from Hashing import sha3
        password = sha3(password)
        account_id = self.user_id + "-" + str(len(self.accounts)+1)
        connection.execute("INSERT INTO Account_Applications (ID, User_ID, Password, CreationTime) VALUES (%s, %s, %s, NOW())", (account_id, self.user_id, password))
        connector.commit()
        print("Account application sent to the bank for approval.\nYour account number is: " + account_id)
        
