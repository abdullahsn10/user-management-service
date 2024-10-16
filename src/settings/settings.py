import os
from dotenv import load_dotenv


# load environment variables
load_dotenv()

# load database settings
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_SERVICE = os.getenv("DB_SERVICE")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# database url
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_SERVICE}/{POSTGRES_DB}"
)


# database settings
DATABASE_SETTINGS = {
    "URL": SQLALCHEMY_DATABASE_URL,
}

# security settings
with open(os.getenv("PRIVATE_KEY_PATH"), "rb") as key_file:
    PRIVATE_KEY = key_file.read()

with open(os.getenv("PUBLIC_KEY_PATH"), "rb") as key_file:
    PUBLIC_KEY = key_file.read()


JWT_TOKEN_SETTINGS = {
    "PRIVATE_KEY": PRIVATE_KEY,
    "PUBLIC_KEY": PUBLIC_KEY,
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
}

# gRPC settings
GRPC_HOST = os.getenv("GRPC_HOST")
GRPC_PORT = os.getenv("GRPC_PORT")
GRPC_SERVER_ADDRESS = f"{GRPC_HOST}:{GRPC_PORT}"
