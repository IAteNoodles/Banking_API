#This module contains the help text for the program, and the APIs.

def get_help():
    print("----------------------------------------------------------------------------------------------------------------------")
    print("CLI.py: \nThe main command line interface for the APIs. It has an interactive CLI:")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("People.py: \nThis module contains the API for inserting people into the People table.")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Staff.py: \nThis module contains the API for inserting staff into the Staff table")
    print("The module contains three classes: Admin, Manager, and Staff.")
    print("""Staff class is the base class for the other classes and has the following functions:
        __init__(self, user_id, password): Initializes the object with the user_id and password, and sets the object attributes accordingly.
        get_type(self): Returns the type of the user.
        add_user(self, people_id, user_id, hashed_passwd): Adds a user to the database.
            people_id(str): The people ID of the user. Use the ID generated from People.py VARCHAR(64)
            user_id(str): The ID of the user. VARCHAR(36)
            hashed_pass(str): SHA3-512 Hash of the password provided by the user. VARCHAR(128)
        change_application(self, application_id): Commits changes to the application (Accept/Reject). After commiting the changes the application is deleted.
            application_id(str): The ID of the application which was provided to the user while creating the application. VARCHAR(16)""")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("""Manager class inherits from Staff class and has the following new functions:
          add_staff(self, people_id, staff_id, hashed_passwd, staff_type): Adds a staff to the database.
            people_id(str): The people ID of the staff. Use the ID generated from People.py VARCHAR(64)
            staff_id(str): The ID of the staff. VARCHAR(36)
            hashed_pass(str): SHA3-512 Hash of the password provided by the staff. VARCHAR(128)
            staff_type(int): The type of the staff. 0 for Staff, 1 for Manager, 2 for Admin.""")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("""Admin class inherits from Manager class and has the following new functions:
          remove_staff(self,staff_id): Removes a staff from the database.
            staff_id(str): The ID of the staff. VARCHAR(36)""")
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print("Users.py: \nThis module contains the APIs which can be used by the users to interact with their accounts")
    print("""It contains the following functions:
        __init__(self, user_id, password): Initializes the object with the user_id and password, and sets the object attributes accordingly.
            user_id(str): The ID of the user. VARCHAR(36)
            password(str): The password of the user. 
        check_account(self): Checks if the user has an account in the database.
        login_account(self): Logs in the user for the current session. Provides an interactive CLI.
        logout_account(self): Logs out the user from the current session.
        create_account(self, password): Creates a new account in the database.
            password(str): The password of the user.
        delete_account(self): Deletes the user's account from the database. Provides an interactive CLI.
            This function needs the following things to be satisfied:
            1) The user must have at least two accounts.
            2) The user must have the correct password of the account to be deleted.
            3) The user must have the private key for his/her ID.
        """)
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print("Accounts.py: \nThis module contains the APIs which are called when some changes are to be made in the account.")
    print("""It contains the following functions:
          __init__(self, account_id, password): Initializes the object with the account_id and password, and sets the object attributes accordingly
          get_balance(self): Returns the balance of the account.
          commit_transaction(self, amount, mode): Commits the transaction to the database.
            amount(int): The amount to be added/subtracted from the account.
            moude(int): The mode of the transaction. 0 for deposit, 1 for withdrawal.""")
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print("This marks the end of the help page.")
    
if __name__ == '__main__':
    print("This module contains the help text for the program, and the APIs.")
    print("HELP PAGES FOR BANKING MANAGEMENT SYSTEM")
    print("Written by: Abhijit Kumar Singh")
    print("Github Repository: https://github.com/IAteNoodles/Banking_API.git")
    print("Check Readme.md for more information")
    print("Readme is available at: https://github.com/IAteNoodles/Banking_API/blob/master/README.md")
    get_help()
    
    
            
            