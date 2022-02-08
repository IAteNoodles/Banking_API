#This class is used to access the staff apis.
#This class is filled with only the base apis. Other features maybe added in future.
import mariadb
connector = mariadb.connect(user="Admin", passwd="Admin@Bank", database="Banking")
connection = connector.curson()
class Staff:
    
    def __init__(self, staff_id, password):
        from Hashing import sha3
        password = sha3(password)
        connection.execute("SELECT * FROM Staff WHERE ID = %s AND Password = %s", (staff_id, password))
        #Checks if there is a user with the given ID and password.
        if connection.fetchone() is None:
            return "Username or password is incorrect"
        
        self.username = staff_id
        self.password = password
        #Fetches the staff type from the database.
        connection.execute("SELECT `Type` FROM Staff WHERE ID = %s", (staff_id))
        
    def add_user(self, user_id, hashed_passwd):
        """
        Inserts a user into the user table with the hashed password.
        """
        connection.execute("INSERT INTO User (ID, Password) VALUES (%s, %s)", (user_id, hashed_passwd))
        connector.commit()
        
    def change_application(self, application_id):
        """
        
        Commits changes to the application.
        
        Args:
            application_id(int): The application ID.
            
        Returns:
            True if the actions were executed successfully, else False.
        """
        
        #Fetches the application from the database and prints the details.
        connection.execute("SELECT * FROM Account_Application WHERE ID = %")
        details=connection.fetchone()
        
        #Print the details of the application. 1st column is the application_id, 2nd is the user_id, 3rd is the account_id, 4th is the hash of the password, 5th is the time of the creation.
        print("Application ID: " + application_id)
        print("User ID: " + str(details[1]))
        print("Account ID: " + str(details[2]))
        print("Created at: " + str(details[4]))
        
        #Asks if the staff wants to accept the application.
        try:
            choice = bool(input("Accept application? (y/n): "))
        except ValueError:
            print("Invalid input")
            return False
        
        def delete_application():
            """
            Deletes the application.
            """
            connection.execute("DELETE FROM Account_Application WHERE ID = %s", (application_id))
            connector.commit()
            
        if choice:
            #If yes, the application is accepted.
            #Creates a new account in the Accounts table with the hashed password
            print("Accepting application...")
            print("Creating new account...")
            connection.execute("INSERT INTO Accounts (ID, Password) VALUES (%s, %s)", (details[1], details[2]))
            print("Account created.")
            delete_application()
            print("Deleting application...")
            print("Application deleted.")
            return True
        else:
            #If no, the application is rejected.
            delete_application()
            print("Rejecting application...")
            print("Application deleted.")
            return True
        
class Manager(Staff):
    def __init__(self, user_id, password):
        super(Manager, self).__init__(user_id, password)
        self.type = 1
        
    def add_staff(self, staff_id, hashed_passwd, staff_type):
        """
        Inserts a staff into the staff table with the hashed password.
        
        Args:
            staff_id: ID of the staff.
            hashed_passwd: Hash of the staff's password.
            staff_type: Type of the staff (Admin: 2 | Manager:1 | Staff:0)
        """
        if staff_type > self.type:
            return "You are not authorized to add this staff"
        
        connection.execute("INSERT INTO Staff (ID, Password, `Type`) VALUES (%s, %s, %s)", (staff_id, hashed_passwd, staff_type))
        connector.commit()
        
class Admin(Manager):
    def __init__(self, user_id, password):
        super(Admin, self).__init__(user_id, password)
        self.type = 2
        
    def remove_staff(self, staff_id):
        """
        Removes a staff from the staff table.
        
        Args:
            staff_id: ID of the staff.
        """
        connection.execute("DELETE FROM staff WHERE ID = %s", (staff_id))
        connector.commit()
