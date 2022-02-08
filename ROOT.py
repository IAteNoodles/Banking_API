#This is not meant to be used directly. USE IT WITH CARE.
#Create staffs and users.


import mariadb



connector = mariadb.connect(user='IAteNoodles', password='CrazyxNoob@69', database='Banking')
connection = connector.cursor()
print ("Creating staffs and users...")
#We fetch the ID from table People.
connection.execute("SELECT ID FROM People")
for row in connection.fetchall():
    #We get the uuid and set it to the staff id.
    connection.execute("SELECT UUID()")
    staff_id = connection.fetchone()[0]
    password = input("Enter Password: ")
    #We hash the password.
    from hashlib import sha3_512 as sha3
    password = sha3(password.encode()).hexdigest()
    #We insert the staff id and password into the database.
    connection.execute("INSERT INTO Staff (`People ID`,`ID`, `Password`, `Type`) VALUES (%s, %s, %s, 2)", (row[0], staff_id, password))
    connector.commit()
    print("Staff created: " + staff_id)