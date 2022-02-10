#A class which can be used to access account apis.
#This class is filled with only the base apis. Other features maybe added in future.
from random import randbytes
import mariadb

from Accounts import Account
connector = mariadb.connect(user='User', host="iatenoodles", password='User@Bank', database='Banking')
connection = connector.cursor()
class User:
    def __init__(self, user_id, password):
        from hashlib import sha3_512 as sha3
        password = sha3(password.encode()).hexdigest()
        connection.execute("SELECT * FROM User WHERE ID = '%s' AND Password = '%s'" % (user_id, password))
        if connection.fetchone() is None:
            raise ValueError("Invalid user ID or password")
        
        self.user_id = user_id
        self.hash = password
        
        #Fetches the People ID from the Users table.
        connection.execute("SELECT `People ID` FROM User WHERE `ID` = '%s'" % self.user_id)
        self.people_id = connection.fetchone()[0]
        
        #Fetching the accounts linked to this user.
        connection.execute("SELECT `ID` FROM Accounts WHERE `User ID` = '%s'" % (user_id))
        self.accounts = connection.fetchall()
        self.current_account= None
    
    def check_account(self):
        """
        
        Checks if the user has any accounts, and returns True if so, else returns False.
        """
        if self.accounts is None:
            print("You have no accounts associated with you.")
            print("Please create an account.")
            choice=input("Do you wish to create an account? (y?)")
            if choice == "y":
                self.create_account(input("Password: "))
                print("You can have only one application associated with you at a time. If you will try to create another application, the previous application will be overwritten.")
            else:
                print("NOTE: You can't make any transaction without opening an account first.")
                print("Exiting...")
                print("No account associated with the user.")
                return False
        return True
            
    def login_account(self):
        """
        Logs in to an account.
        """
        #Checks if there is atleast one account associated with this user.
        if not self.check_account():
            return "You have no accounts associated with you."
            
        print("Accounts related to this user are:")
        index = 1
        #Provides a list of the accounts linked to this user.
        for account in self.accounts:
            print(index, ": " + account[0])
            index+=1
        
        #Asks the user to enter the account number to login.
        relative_account = int(input("Enter the account number to login: "))
        if relative_account > len(self.accounts) or relative_account < 1:
            return "Invalid account number"
        
        #Asks the user to enter the password to login.
        password = input("Enter the password to login: ")
        
        print("Logging in...")
        
        #Checks if the account and password are correct.
        self.current_account = Account(self.accounts[relative_account-1][0], password)
        #Creates an account object with the given account number.         

        print("Logged in to account: ", self.accounts[relative_account-1][0])
        
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
        from hashlib import sha3_512 as sha3
        password = sha3(password.encode()).hexdigest()
        #Generates a random account number.
        account_id = randbytes(20).hex()    
        
        #Checks if there is already an application for this account.
        connection.execute("SELECT * FROM Account_Application WHERE Account_ID = '%s'" % account_id)
        if connection.fetchone() is not None:
            print("There is already an application for this account.")
            print("Overwritting previous application...")
            #Update the application with the new password and changes the CreationTime.
            connection.execute("UPDATE Account_Application SET `CreationTime` = NOW(), `Hash` = '%s' WHERE Account_ID = '%s'" % (password, account_id))
            connector.commit()
            print("The previous application has been overwritten.")
            
            return 
        #Generates a 16 character random string for application id.
        application_id = randbytes(8).hex()
        while(True):
                try:
                    connection.execute("INSERT INTO Account_Application (`ID`,`Account_ID`, `User_ID`, `Hash`, `CreationTime`) VALUES ('%s', '%s', '%s', '%s', NOW())" % (application_id, account_id, self.user_id, password))
                except mariadb.IntegrityError:
                    #Fails as the account number is already taken.
                    #Generates a new account number.
                    account_id = randbytes(20).hex()   
                finally:
                    break 
        connector.commit()
        print("Account application sent to the bank for approval.\nYour account number is: " + account_id)
        print("The application id for the account is: " + application_id)

    def delete_account(self):
        if not self.check_account():
            return "You have no accounts associated with you."
        index=1
        accounts = []
        for account_id in self.accounts:
            accounts.append(account_id[0])
            print(index, ": ", account_id[0])
            index+=1
        relative_account = int(input("Enter the account number to delete: "))
        if relative_account > len(accounts) or index-1 < 2:
            print("Invalid account number. You need to have at least 2 accounts for this operation.")
            return "User didn't have enough accounts."
        choice=input("THIS WILL YOUR ACCOUNT, ARE YOU SURE YOU WANT TO DELETE THIS ACCOUNT? (y?)")
        if choice == "n":
            print("Command Aborted...")
            return "Account not deleted."
        print("ALL YOUR FUNDS WILL BE TRANSFERED TO THE FIRST ACCOUNT ASSOCIATED WITH YOU.")
        choice=input("Do you wish to change the account to transfer funds to? (n?)")
        if choice == "y":
            account_number=input("Account number to transfer funds to: ")
            account_id = accounts[account_number-1]
        else:
            account_id = accounts[1] if relative_account == 1 else accounts[0]
        print("Transferring funds from account: " + accounts[relative_account-1] + " to account: " + account_id + "...")
        path_private_key=open(input("Path to private key: "))#"Please enter path of your private key:"))
        #Fetches the public key from the People table, and matches it with the private key.
        from Crypto.PublicKey import RSA
        temp=path_private_key.read()
        #Convert temp to bytes.
        temp=temp.encode('utf-8')
        private_key = RSA.import_key(temp)

        
        #Matches the public key with the private key.
        public_key = private_key.publickey().export_key()
        #TODO check if the private key is correct..
        
        connection.execute("SELECT `Public Key` FROM People WHERE `ID` = '%s'" % self.people_id)
        if connection.fetchone()[0] == public_key:
            print("Invalid private key.")
            print("Command Aborted...")
            return False
        connection.execute("DELETE FROM Accounts WHERE ID = '%s'" % accounts[relative_account-1])
        connector.commit()