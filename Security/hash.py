import bcrypt

passwd = b'58a1b6f3d842f437c57e23a9cb2e1d8467a36b8ea91f18e46bcf240aa2e47a6a'
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)

#print(salt)
#print(hashed)
def encript_data(psw:str):
    salt1 = bcrypt.gensalt()
    return salt1




'''
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