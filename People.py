#A class to input a new record in the People table.
#First column is a 32 character ID, which is generated automatically using randombits
#Second column is the name
#Third column is the public key to the generated RSA key pair. This private key is not stored in the database, but is returned to the user. 
import os
import pickle
import mariadb


connector = mariadb.connect(user="People", passwd="People@Bank", database="Banking")
connection = connector.cursor()

def generate_keypair(name):
    #Generates a new key pair.
    from Crypto.PublicKey import RSA
    key = RSA.generate(2048)
    private_key = key.export_key() #Generate private key
    public_key = key.publickey().export_key() #Generate public_key
    #Create a file to store the private key.
    file = open(name+"private_key.pem","wb")  
    file.write(private_key)
    if RSA.importKey(private_key).publickey().export_key() == public_key:
        print ("Successfully generated key pair.")
    return public_key.decode("utf-8"),private_key.decode("utf-8") #Decode public and private keys

name = input("Enter your name: ")
#Generate a random 32 character ID
people_id = os.urandom(32).hex()
public_key,private_key = generate_keypair(name) #Generating a new key pair
print(private_key)

#Inserting the new record into the People table.
connection.execute("INSERT INTO People (`ID`,`Name`,`Public Key`) VALUES ('%s','%s','%s')" % (people_id,name,public_key))
connector.commit()