from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

'''
def encript_data(psw:str):
    salt1 = bcrypt.gensalt()
    return salt1





CODIFICAR
import bcrypt

passwd = b'invulnerablepassword'

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)

print(salt)
print(hashed)

DECODIFICAR
to_test =  b'invulnerablepassword'
hashed = b'$2b$12$9g2Rx2PmjcDboBZKEAEmNOguvxZM9jTbzSxW1SyzR1Nj63Q918bli'
if bcrypt.checkpw(passwd, hashed):
    return True
else:
    return False
'''