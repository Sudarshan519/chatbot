import os
from dotenv import load_dotenv
# from fastapi_jwt_auth import AuthJWT
# import pymysql
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    SQLITE_URL: str="sqlite:///ntest.db"#"sqlite:///db/ntest.db"#+aiosqlite
    PROJECT_NAME:str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"
    MONGODB_URI:   str = os.getenv("MONGODB_URI")
    POSTGRES_URL:   str = os.getenv("POSTGRES_URL")
    MAIL_PASS:   str = os.getenv("MAIL_PASS")
    MAIL_UNAME:   str = os.getenv("MAIL_UNAME")
    
    MySQL_USER : str = os.getenv("MYSQL_USER")
    MySQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MySQL_SERVER : str = os.getenv("MySQL_SERVER","localhost")
    # MySQL_PORT : str = os.getenv("MySQL_PORT",3306) # default MySQL port is 5432
    MySQL_DB : str = os.getenv("MYSQL_DB")
    DATABASE_URL =SQLITE_URL# f"mysql+mysqlconnector://{MySQL_USER}:{MySQL_PASSWORD}@{MySQL_SERVER}:{MySQL_PORT}/{MySQL_DB}" #POSTGRES_URL
    # DATABASE_URL = f"mysql+mysqlconnector://{MySQL_USER}:{MySQL_PASSWORD}@{MySQL_SERVER}:{MySQL_PORT}/{MySQL_DB}" #POSTGRES_URL
    MySQL_USER_PYTHON= os.getenv("MYSQL_USER_PYTHON")
    MySQL_PASSWORD_PYRHON=os.getenv("PASSWORD_PYTHON")
    MySQL_SERVER_PYTHON : str = os.getenv("MYSQL_HOST_PYTHON","localhost")
 
    MySQL_DB_PYTHON=os.getenv("DATABASE_PYTHON")
    DATABASE_URL_PYTHON =f"mysql+mysqlconnector://SudarshanShresth:Asmir123@Sudarshanshrestha.mysql.pythonanywhere-services.com:3306/SudarshanShresth$default" #POSTGRES_URL
    # DATABASE_URL =POSTGRES_URL
    PGDBURL=os.getenv("PGDBURL")
    ACCESS_TOKEN_EXPIRES_IN=os.getenv("ACCESS_TOKEN_EXPIRES_IN")
    REFRESH_TOKEN_EXPIRES_IN=os.getenv("REFRESH_TOKEN_EXPIRES_IN") 
    SECRET_KEY :str = os.getenv("SECRET_KEY")   #new
    ALGORITHM = "HS256"   
    ALGO2='RS256'                      #new
    ACCESS_TOKEN_EXPIRE_MINUTES = 60*24  #in mins  #new
    REFRESH_TOKEN_EXPIRES_IN=60*24*2
    TEST_USER_EMAIL = "test@example.com"  #new
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL","redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND","redis://127.0.0.1:6379/0")

    JWT_PUBLIC_KEY:str=os.environ.get("JWT_PUBLIC_KEY")
    EXTERNALPGURL:str=os.environ.get("EXTERNALPGURL")
# @AuthJWT.load_config
# def get_config():
#     return Settings()
settings=Settings()

# from pydantic import BaseSettings

# class JWTSettings(BaseSettings):
#     DATABASE_PORT: int
#     POSTGRES_PASSWORD: str
#     POSTGRES_USER: str
#     POSTGRES_DB: str
#     POSTGRES_HOST: str
#     POSTGRES_HOSTNAME: str

#     JWT_PUBLIC_KEY: str
#     JWT_PRIVATE_KEY: str
#     REFRESH_TOKEN_EXPIRES_IN: int
#     ACCESS_TOKEN_EXPIRES_IN: int
#     JWT_ALGORITHM: str

#     CLIENT_ORIGIN: str

#     class Config:
#         env_file = './.env'


# jwtSettings = JWTSettings()

# class NotVerified(Exception):
#     pass


# class UserNotFound(Exception):
#     pass