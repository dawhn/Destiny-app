class Client:
    def __init__(self, client_id, client_secret, host, port, api_key, redirect_url=""):
        self.client_id = str(client_id)
        self.client_secret = client_secret
        self.host = host
        self.port = str(port)
        self.api_key = api_key
        self.redirect_url = redirect_url
        self.authorization_code = ""
        self.token = {}
