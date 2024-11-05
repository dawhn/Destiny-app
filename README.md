# Destiny-app

## Generate Self-Signed Certificates

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

## Include in Flask App

```py
app = Flask(__name__)
app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
```

## Shell Script for Certificates
`generate_cert.sh` : 

```sh
#!/bin/bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```
- Call this script if `key.pem` or `cert.pem` is not available in the project

## Add Certificate to Default Browser

**Chrome :**
- Open settings.
- Navigate to `Privacy and Security` > `Security` > `Manage certificates`.
- Import the `cert.pem` under the `Truster Root Certification Authorities` tab.

**Firefox :**
- Open settings.
- Navigate to `Privacy & Security` > `Certificates` > `View Certificates`.
- Import `cert.pem` under the `Authorities` tab.


[//]: https://stackoverflow.com/questions/8169999/how-can-i-create-a-self-signed-cert-for-localhost:w
