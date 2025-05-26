import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import mysql.connector
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware # <--- ADD THIS IMPORT

# Load env variables
load_dotenv()

# DB config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ai_gateway")

# JWT config
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_TO_SOMETHING_SECURE")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models cost - adjust as needed
MODEL_COSTS = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "claude-3-opus-20240229": {"input": 0.008, "output": 0.024}
}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="AI Gateway with Auth")

# <--- ADD THIS CORS MIDDLEWARE BLOCK AFTER app = FastAPI(...) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"], # Ensure all possible frontend origins are included
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# <--- END CORS MIDDLEWARE BLOCK ---

# Pydantic models
class User(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RequestPayload(BaseModel):
    prompt: str
    model_name: str

# DB helper
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        auth_plugin='mysql_native_password'
    )

# User functions
def get_user_by_username(username: str) -> Optional[UserInDB]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        if row:
            return UserInDB(**row)
        return None
    finally:
        cursor.close()
        conn.close()

def create_user(username: str, email: str, password: str):
    hashed = pwd_context.hash(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )
        conn.commit()
    except mysql.connector.Error as e:
        # More informative error on duplicate username or email
        raise HTTPException(status_code=400, detail="Username or Email already exists")
    finally:
        cursor.close()
        conn.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return User(id=user.id, username=user.username, email=user.email)

# Usage logging
def log_usage(user_id: int, model_name: str, input_tokens: int, output_tokens: int):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO usage_log (user_id, model_name, input_tokens, output_tokens, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, model_name, input_tokens, output_tokens, datetime.utcnow()))
        conn.commit()
    except mysql.connector.Error as e:
        print("DB log usage error:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def calculate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    model_cost = MODEL_COSTS.get(model_name.lower(), {"input": 0.001, "output": 0.002})
    cost = ((input_tokens / 1000) * model_cost["input"]) + ((output_tokens / 1000) * model_cost["output"])
    return round(cost, 6)

# Import your existing model router logic
from backend.services.model_router import route_model

# Import the new dashboard router
from backend.routers import dashboard_router

# Routes
@app.post("/register", summary="Register a new user")
def register(user: UserCreate):
    create_user(user.username, user.email, user.password)
    return {"msg": "User registered successfully"}

@app.post("/token", response_model=Token, summary="Get JWT token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/generate", summary="Generate text (auth required)")
async def generate(payload: RequestPayload, current_user: User = Depends(get_current_user)):
    try:
        content, input_tokens, output_tokens = route_model(payload.model_name, payload.prompt)
        log_usage(current_user.id, payload.model_name, input_tokens, output_tokens)
        cost = calculate_cost(payload.model_name, input_tokens, output_tokens)
        return {
            "response": content.strip(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": cost
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@app.get("/usage", summary="Get usage logs for current user")
def get_usage(current_user: User = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT model_name, input_tokens, output_tokens, timestamp FROM usage_log WHERE user_id = %s ORDER BY timestamp DESC",
        (current_user.id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"usage": rows}

# Include the new dashboard router
app.include_router(dashboard_router.router)