
#The interface to interact with the apis.
def work_as_user(user_id, password):
    from Users import User
    import mariadb
    connector = mariadb.connect(
        user="User",passwd="User@Bank",database="Banking")
    connection = connector.cursor()
    
    #Creates a new user object.
    current_login_object=User(user_id, password)
    print("Welcome to the User Portal")
    print("Your the following user:" + current_login_object.user_id)
    print("Options avaliable to you are:")
    print("1. Log in to one of your accounts")    
    print("2. Create a new account")
    print("3. Delete a account")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        current_login_object.login_account()
        if current_login_object.current_account == None:
            return "Please make sure that you have an account. If you already have submitted an account, please wait for the application to be verified."

        
        print("You have successfully logged in to account: ", current_login_object.current_account)
        print("Your balance is: " + str(current_login_object.current_account.balance))
        print("Options avaliable to you are:")
        print("1. Withdraw money")
        print("2. Deposit money")
        print("3. Fetch balance")
        print("To log out of the current account press anything else.")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            amount = int(input("Enter the amount to withdraw: "))
            current_login_object.current_account.commit_transaction(amount,0)
        elif choice == 2:
            amount = int(input("Enter the amount to deposit: "))
            current_login_object.current_account.commit_transaction(amount,1)
        elif choice == 3:
            current_login_object.current_account.get_balance()
        else:
            current_login_object.logout_account()
            
    elif choice == 2:
        current_login_object.create_account(input("Password: "))
    elif choice == 3:
        current_login_object.delete_account()
    else:
        print("Logging out...")
        del current_login_object
        print("Goodbye! The user portal is now closed.")
        return
        
    
def work_as_staff(staff_id, password):
    
    #Imports the Staff, Manager and Admin classes.
    from Staffs import Staff, Manager, Admin
    import mariadb
    connector = mariadb.connect(
    user="Staff", passwd="Account@Bank", database="Banking")
    connection = connector.cursor()
    #Checks the type of the staff and creates a new instance of the appropriate staff class.
    connection.execute("SELECT Type FROM Staff WHERE ID = '%s'" % staff_id)
    staff_type = connection.fetchone()[0]
    if staff_type == 0:
        current_login_object = Staff(staff_id, password)
    elif staff_type == 1:
        current_login_object = Manager(staff_id, password)
    elif staff_type == 2:
        current_login_object = Admin(staff_id, password)
    else:
        print("Invalid staff type")
        return "Exiting..."
    
    #Closes the connection and deletes the connector.
    connector.close()
    del connector, connection
    
    
    print("Welcome to the Staff Portal")
    print("Your the following staff:" + current_login_object.user_id + "of type:" + str(current_login_object.get_type()))
    print("Options avaliable to you are:")
    
    no_choice = 2
    print("1. Create a user")
    print("2. Change an application")
    
    #Checks if the current_login_object is instance of Manager.
    if current_login_object.type >=1:
        print("3. Add a staff")
        no_choice+=1
        #Checks if the current_login_object is instance of Admin.
        if current_login_object.type==2:
            print("4. Remove a staff")
            no_choice+=1
    
    print("To log out of the current staff press anything else.")
    
    while(True):
        choice = input("Please enter your choice: ")
    
        #Uses if elif else to call the appropriate function.
        if choice == "1":
            #WORKS
            people_id = input("Enter the people ID: ") #Varchar(64)
            user_id = input("Please enter the user id: ") #Varchar(36) - UUID
            hashed_passwd = input("Please enter the hashed password: ") #Varchar(128)
            current_login_object.add_user(people_id, user_id, hashed_passwd)
        elif choice == "2":
            application_id = input("Please enter the application id: ")
            current_login_object.change_application(application_id)
        elif choice == "3":
            #WORKS
            people_id = input("Enter the people ID: ") #Varchar(64)
            staff_id = input("Please enter the staff id: ")
            hashed_passwd = input("Please enter the hashed password: ")
            staff_type = int(input("0: Staff, 1: Manager, 2: Admin:\nEnter the staff type: "))
            current_login_object.add_staff(people_id, staff_id, hashed_passwd, staff_type)
        elif choice == "4":
            #WORKS
            staff_id = input("Please enter the staff id: ")
            current_login_object.remove_staff(staff_id)
        
        else:
            print("Logging out...")
            del current_login_object
            print("Goodbye! The staff portal is now closed.")

         # ----------------------------------------------------------------END OF STAFF PORTAL---------------------------------------------------------------------------------
        
    
if __name__ == '__main__':
    print("Welcome to the Bank API")
    print("Enter the number of the function you want to use:")
    print("1: Help")
    print("2: Login")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print("Help:")
        print("This is the help page of the Bank API.")
        #TODO: Add more help pages.
    elif choice == 2:
        print("This is the User login page")
        print("Are you a user? (y/n)")
        choice = input("Enter your choice: ")
        if choice == "y":
            user_id = "d53e3ba4-89c0-11ec-8eb3-d71f150f0903"#input("Enter your id: ")
            password = "1"#input("Enter your password: ")
            from Users import User
            work_as_user(user_id, password)
        elif choice == "n":
            #To access the login page of a staff, one must know the secret key provided only to the staff. StaffHere@BankingAPI
            secret = "d9811afaf579ac04dcfd9951a520f8b15c911a943bd845a1f2080f9e0d31410061556e6559dccd2926751c8cb61ec2dd8a90e30a1edef8b330767ec28dbfff2a"
            key = input("Enter the secret key")
            from hashlib import sha3_512 as sha3
            key = sha3(key.encode()).hexdigest()
            if True:#key == secret:
                print("This is the staff login page")
                staff_id = "c66377e6-883d-11ec-8f55-d92738a284b2"#input("Enter your id: ") #Varchar(36) - UUID
                password = "1"#input("Enter your password: ") #Varchar(128)
                work_as_staff(staff_id, password)
            else:
                print("Invalid secret key")
                print("Exiting...")
        else:
            print("Invalid choice")
            print("Exiting...")