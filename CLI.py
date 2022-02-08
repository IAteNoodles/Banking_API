#The interface to interact with the apis.
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
            user_id = input("Enter your id: ")
            password = input("Enter your password: ")
            from Banking_.API.Users import User
            current_login_object = User(user_id, password)
        elif choice == "n":
            #To access the login page of a staff, one must know the secret key provided only to the staff. StaffHere@BankingAPI
            secret = "d9811afaf579ac04dcfd9951a520f8b15c911a943bd845a1f2080f9e0d31410061556e6559dccd2926751c8cb61ec2dd8a90e30a1edef8b330767ec28dbfff2a"
            key = input("Enter the secret key")
            from hashlib import sha3_512
            key = sha3_512(key.encode()).hexdigest()
            if key == secret:
                print("This is the staff login page")
                staff_id = input("Enter your id: ")
                password = input("Enter your password: ")
                from Banking_.API.Staffs import Staff
                current_login_object = Staff(staff_id, password)
            else:
                print("Invalid secret key")
                print("Exiting...")
        else:
            print("Invalid choice")
            print("Exiting...")