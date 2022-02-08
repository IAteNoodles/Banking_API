#A class which can be used to access account apis.
#This class is filled with only the base apis. Other features maybe added in future.
import mariadb
connector = mariadb.connect(user='Account',host = "localhost", password='Account@Bank', database='Banking')
connection = connector.cursor()
class Account:
    def __init__(self, account_id, password):
        from hashlib import sha3_512 as sha3
        password = sha3(password.encode()).hexdigest()
        connection.execute("SELECT * FROM Accounts WHERE ID = %s AND Password = %s", (account_id, password))
        #Checks if there is a account with the given ID and password.
        if connection.fetchone() is None:
            return "ID or password is incorrect"

        self.account_id = account_id
        self.hash = password    
        
        #Fetches account balance from the database.
        connection.execute("SELECT Balance FROM Accounts WHERE ID = '%s'" % self.account_id)
        self.balance = connection.fetchone()[0]
        
    def get_balance(self):
        """
        
        Fetches the account's balance from the database, and updates the balance attribute.
                
        Retuns: The current balance of the account.
        """
        connection.execute("SELECT balance FROM Accounts WHERE ID = %s", (self.account_id))
        self.balance = connection.fetchone()[0]
        return self.balance
            
    
    def commit_transaction(self, amount, mode):
        """
        
        Commits a transaction to the account's account in the database.
        
        Args:
            amount(int): The amount.
            mode(int): The transaction mode. (Deposit:1 or Withdraw:0)
        
        Retuns:
            True if the transaction was successful, along with new balance.
            False if the transaction was unsuccessful, along with the error message.
        """
        #Check if the account has entered a valid mode.
        if mode == 1:
            balance = self.balance + amount
        elif mode == 0:
            balance = self.balance - amount
        else:
            print("Invalid mode\nValid modes are: 0 for withdraw, 1 for deposit")
            return False, "Invalid transaction mode"
        
        #Check if the account has enough money to make the transaction.
        if balance < 0:
            print("Your account balance is: " + str(self.balance))
            print("After this transaction your balance would be: " + str(self.balance - amount))
            print("You do not have enough money to make this transaction.")
            return False, "Insufficient funds"
        
        #Commits the transaction to the database.
        connection.execute("UPDATE Accounts SET Balance = %s WHERE ID = %s", (balance, self.account_id))
        connector.commit()
        self.balance = balance
        return True, "New balance: %s" % self.balance
    
#---------------------------------------------------------------- END OF CLASS -----------------------------------------------------------------#
        
        
        