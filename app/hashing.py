from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"],deprecated = "auto" )

class Hash():
    def hashing(password):
        hashed_password = pwd_cxt.hash(password)
        return hashed_password
    
    def verify(plain_password,Hashpassword):
        return pwd_cxt.verify(plain_password,Hashpassword)
    
        