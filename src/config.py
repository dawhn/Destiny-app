from starlette.config import Config

config = Config("src/.env")

BASE_URL = config("BASE_URL")
API_BASE_URL = config("API_BASE_URL")
DB_NAME = config("DB_NAME")
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
PORT = config("PORT")
HOST = config("HOST")
API_KEY = config("API_KEY")
AUTH_TOKEN = config("AUTH_TOKEN")
AUTH_CODE = config("AUTH_CODE")


def add_auth_code(code):
    with open(".env", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("AUTH_CODE="):
            # Update the existing variable
            lines[i] = f'AUTH_CODE="{code}"\n'

    with open(".env", "w") as file:
        file.writelines(lines)

    global AUTH_CODE
    AUTH_CODE = code


def add_auth_token(token):
    with open(".env", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("AUTH_TOKEN="):
            # Update the existing variable
            lines[i] = f'AUTH_TOKEN="{token}"\n'

    with open(".env", "w") as file:
        file.writelines(lines)

    global AUTH_TOKEN
    AUTH_TOKEN = token
