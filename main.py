import sys
import time

from threading import Thread

from src.token.oauth import client, app
from app.start import start_app
from src.database.database import db_setup


def run_flask():
    cli = sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None
    app.run(
        port=client.port,
        host=client.host,
        ssl_context=("cert/cert.pem", "cert/priv_key.pem"),
    )


if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    Thread(target=start_app, daemon=True).start()
    db_setup()

    while True:
        time.sleep(1)
