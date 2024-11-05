import flask
import requests
import time

from flask import Flask, request
from src.config import (
    BASE_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    PORT,
    HOST,
    API_KEY,
    AUTH_CODE,
    add_auth_token,
    add_auth_code,
)
from src.token.Client import Client

app = Flask(__name__)
client = Client(CLIENT_ID, CLIENT_SECRET, HOST, PORT, API_KEY)


@app.route("/")
def authorize():
    """
    Authorize the Client using personal 'bungie.net' account
    """
    authorize_url = f"{BASE_URL}/en/oauth/authorize?client_id={client.client_id}&response_type=code&state=asdf"
    if "code" in request.args:
        client.authorization_code = request.args["code"]
        if AUTH_CODE == "":
            add_auth_code(request.args["code"])
    if client.authorization_code == "":
        return flask.redirect(authorize_url)
    else:
        return flask.redirect("/redirect_url")


@app.route("/redirect_url")
def redirect():
    """

    :return:
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "grant_type": "authorization_code",
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "code": client.authorization_code,
    }

    r = requests.post(
        f"{BASE_URL}/platform/app/oauth/token/", data=data, headers=headers
    )
    resp = r.json()
    print(resp)

    add_auth_token(resp["access_token"])

    client.token = {
        "access_token": resp["access_token"],
        "access_expires": time.time() + resp["expires_in"],
        "refresh_token": resp["refresh_token"],
        "refresh_expires": time.time() + resp["refresh_expires_in"],
    }
    return flask.redirect("/end")


@app.route("/refresh_url")
def refresh():
    """

    :return:
    """

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "grant_type": "refresh_token",
        "refresh_token": client.token["refresh_token"],
        "client_id": client.client_id,
        "client_secret": client.client_secret,
    }

    r = requests.post(
        "https://www.bungie.net/platform/app/oauth/token/", data=data, headers=headers
    )
    resp = r.json()

    client.token["access_token"] = resp["access_token"]
    client.token["access_expires"] = time.time() + resp["expires_in"]
    client.token["refresh_token"] = resp["refresh_token"]
    client.token["refresh_expires"] = time.time() + resp["refresh_expires_in"]

    # Replace csv file with new data
    data_ = {
        "access_token": [client.token["access_token"]],
        "access_expires": [client.token["access_expires"]],
        "refresh_token": [client.token["refresh_token"]],
        "refresh_expires": [client.token["refresh_expires"]],
    }
    # df = pd.DataFraclient(data_)
    # df.to_csv('../data.csv')

    return flask.redirect("/end")
