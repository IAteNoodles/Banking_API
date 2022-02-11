#This class will test if all the APIs are working as intended.
from random import randbytes
import sys
from People import generate

print("Checking mariadb connector is configured...")
import mariadb
try:
    connector = mariadb.connect(user="People", passwd="People@Bank", database="Banking")
    connection = connector.cursor()
except mariadb.Error as e:
    print("Test failed: mariadb connector is not configured.")
    raise SystemExit("Error %d: %s" % (e.args[0], e.args[1]))

print("Test passed: mariadb connector is configured.")
connection.execute("Delete from People where Name in ('Charles', 'Winnie', 'Micheal')")
connection.execute("insert into `Staff` values ('fbc97453079eabefaffadcaed7ceaf2c155feffef07869043ef7ad84b9c69a8e','75a908fc-8b41-11ec-8e4d-d61a00b1794b','a1eb8cee0626bd9891f4f1ae76a6bf11b96100fbce774e8b48634f67e6756812d1763fe1ff4593b6ee1e9e5c4b350f1a1fad9bf87e927f850197d6c2c2248f74',2)")
connector.commit()
#Checking that People clas is working as intended.
list_of_people: tuple = ("Charles",
                  "Winnie",
                  "Micheal")
                  #""""Charlie",
                  #"William",
                  #"Bertie",
                  #"Juan",
                  #"Iva",
                  #"Adelaide",
                  #"Ada",
                  #"Daniel",
                  #"Christina",
                  #"Lilly",
                  #"Isaiah",
                  #"Marguerite",
                  #"Gary")"""

print("Inserting into the database using the People.generate() function")
list_of_ids = []
for person in list_of_people:
    list_of_ids.append(generate(person))


print("Checking that the people have been added to the People table.")

print(list_of_people)
connection.execute("SELECT * FROM People where Name in {}".format(list_of_people))
connection.fetchall()
if connection.rowcount == len(list_of_people):
    print("Test passed: People table is correctly populated.")
else:
    print("Test failed: People table is not correctly populated.")
    sys.exit(1)
    
print("Test passed: People APIs are working as intended.")

#Checking the Staff APIs are working as intended.

test_user = {
    "staff_id":"75a908fc-8b41-11ec-8e4d-d61a00b1794b",
    "passwd":"IAteNoodles",
    "type":"Admin"
    }

print("Connecting with ROOT@Bank...")
from Staffs import Staff, Manager, Admin

test_user["object"] = Admin(test_user["staff_id"], test_user["passwd"])

print("Checking the staff type...")
if test_user["object"].get_type() == test_user["type"]:
    print("Test passed: Staff type is correct.")
else:
    print("Test failed: Staff type is incorrect.")
    sys.exit(1)

print("Adding a new admin (BANKING@ADMIN) to the database...")

print("Creating a new record in the People table...")
new_admin_people_id = generate("BANKING@ADMIN")
print("The private key for BANKING@ADMIN is stored in /__KEYS folder. Please save it somewhere secure and delete it.")

print("Creating a random password for the new admin...")
new_admin_password = randbytes(16).hex()
print("Password for BANKING@ADMIN is " + new_admin_password)
from hashlib import sha3_512 as sha3
hash_passwd = sha3(new_admin_password.encode()).hexdigest()
new_admin_staff_id = randbytes(18).hex()
test_user["object"].add_staff(new_admin_people_id, new_admin_staff_id, hash_passwd, 2)

print("Added a new admin (BANKING@ADMIN) to the database.")

print("DestroyingROOT@BANK connection...")
del test_user["object"]

print("Connecting with BANKING@ADMIN...")
new_admin_connection = Admin(new_admin_staff_id, new_admin_password)

print("Checking if BANKING@ADMIN is an admin...")
if new_admin_connection.get_type() == "Admin":
    print("Test passed: BANKING@ADMIN is an admin.")
else:
    print("Test failed: BANKING@ADMIN is not an admin")
    sys.exit(1)

print("Addming a bunch of users to the Bank...")

random_user_info = dict()
for id in list_of_ids:
    random_user_id = randbytes(18).hex()
    random_user_password = randbytes(16).hex()
    random_user_info[random_user_id] = random_user_password
    new_admin_connection.add_user(id, random_user_id, sha3(random_user_password.encode()).hexdigest())
    print("Added user " + id + " to the Bank with id: " + random_user_id +" and password: " + random_user_password)

print("Test passed: Admin is an able to add users to the Bank.")

print("Checking if BANKING@ADMIN is able to change applications...")
print("Creating a new application...")
account_info = dict()
applications = list()
for user in random_user_info:
    print("Creating an application for " + user)
    from Users import User
    user_connection = User(user, random_user_info[user])
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Checking if there exists an account with the user")
    if not user_connection.check_account():
        print("User has no accounts registered. Creating a new account application...")
        password = randbytes(16).hex()
        application_id, account_id  = user_connection.create_account(password)
        print("Created an application for " + user)
        print("Application id: " + application_id)
        print("Account id: " + account_id)
        print("Password: " + password)
        applications.append(application_id)
        account_info[account_id] = password

print("Accepting all the applications...")
no_of_applications_accepted = 0
for application in applications:
    print("Accepting application " + application)
    
    if not new_admin_connection.change_application(application, True):
        print("BANKING@ADMIN is not able to accept application " + application)
    else:
        print("Application " + application + " accepted.")
        no_of_applications_accepted += 1
        
print("BANKING@ADMIN accepted %d/%d applications" % (no_of_applications_accepted, len(applications)))
if len(applications) - no_of_applications_accepted > 5:
    print("Test failed: BANKING@ADMIN is not able to accept all the applications.")
    sys.exit(1)

print("Test passed: BANKING@ADMIN is able to accept the applications.")
if len(applications) - no_of_applications_accepted != 0:
    #Prints the amount of applications not accepted as error.
    sys.stderr("Waring: %d/%d applications not accepted." % (len(applications) - no_of_applications_accepted, len(applications)))   

print("Addming a bunch of staffs to the Bank...")    

count  = 0
for id in list_of_ids:
    staff_id = randbytes(18).hex()
    password = randbytes(16).hex()
    hash_passwd = sha3(password.encode()).hexdigest()
    type_staff = 0 if count % 2 == 0 else 1
    status = new_admin_connection.add_staff(id, staff_id, hash_passwd, type_staff)   
    if not status:
        sys.stderr("BANKING@ADMIN is not able to add staff " + id)
    else:
        print("Added staff " + id + " with id: " + staff_id + ", type: ", type_staff, ", and password: " + password)
        count += 1

if len(list_of_ids) - count > 5:
    print("Test failed: BANKING@ADMIN is not able to add all the staffs.")
    sys.exit(1)

print("Test passed: BANKING@ADMIN is able to add the staffs.")
if len(list_of_ids) - count != 0:
    sys.stderr("Waring: %d/%d staffs not added." % (len(list_of_ids) - count, len(list_of_ids)))

    
print("Removing ROOT@BANK from the database...")
if new_admin_connection.remove_staff(test_user["staff_id"]):
    print("Removed ROOT@BANK from the database.")
    print("Test passed: BANKING@ADMIN is able to remove ROOT@BANK (Admin).")
else:
    print("Failed to remove ROOT@BANK from the database")
    print("Test failed: BANKING@ADMIN is not able to remove ROOT@BANK (Admin).")
    
print("--------------------------------------------------------------------------------")
print("Test passed: Staff APIs are working as intended.")
