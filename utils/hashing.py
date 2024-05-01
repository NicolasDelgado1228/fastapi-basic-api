from cryptography.fernet import Fernet

key = Fernet.generate_key()
# create a fernet hashing class
fernet = Fernet(key=key)
