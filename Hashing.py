"""
Testing
"""
class A:
    def __init__(self):
        self.x=1
    
    def b():
        return self.x
def sha256(data: str):
    """
    Abhijit -> 1bea44bfa1f9e9dc7c6c1bafcb680429b7167a0433255cb53403034514a2331b
    `echo -n "Abhijit" | sha256sum`
    """
    # Hash a single string with hashlib.sha256
    import hashlib
    hashed_string = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return hashed_string
    
def sha3(data: str):
    """
    sha3 Hashes the input using the SHA3 algorithm. Also known as keccak.


    Args:
        data (str): The input string to be hashed.

    Returns:
        str: Hash of the input string.
    """
    from Crypto.Hash import keccak
    hash = keccak.new(digest_bits=512)
    hash.update(data.encode())
    return hash.hexdigest()  # Hashes the password without salt

print(sha3("StaffHere@BankingAPI"))
print(sha3("Abhijit"))