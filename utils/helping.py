from fastapi import Depends,HTTPException, status
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import utils.data_type as data_type
import config.database as database
from jose import JWTError,jwt


SECRET_KEY="d742e68876723b8ba6fae9c1c33c12e5a0023fb6c7a07158daac74fe08c2deeb30060af11979caafdc4afca172184b0138bf6029180e23da80d21e00ed4f7d4d"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = data_type.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    userCollection=database.db.get_collection("users")
    user = userCollection.find_one({"email":token_data.email})
    if user is None:
        raise credentials_exception
    return user