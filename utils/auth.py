import hashlib
import datetime

# Hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

