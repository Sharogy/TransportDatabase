from cryptography.fernet import Fernet
from database import Database


class Encryption(Database):

    KEY = b'CWX_ONTWIE1zQaPNOUxSG9lAtZfO-4gEQTgSjmULfMU='

    def __init__(self):
        Database.__init__(self)
