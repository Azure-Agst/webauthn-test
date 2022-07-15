# WebAuthn Test

A small Python web server utilizing the `webauthn` library to successfully implement WebAuthn. Fun afternoon project that taught me a bunch.

## Running

### Docker:

```
$ docker run -dp 5000:5000 ghcr.io/azure-agst/webauthn-test
```

### Python Virtualenv:

```
$ python3 -m venv .venv
$ source .vemv/bin/activate
$ pip install -r requirements.txt
$ flask run
```

## Registration Procedure

1. Client sends a request to the server with registration info. (i.e. username, email, etc.)
2. Server uses registration info to format a `publicKeyCredentialCreationOptions` object, then sends it back to Client.
3. User uses `navigator.credentials.create()` to generate a `PublicKeyCredential`, then sends it back to the server.
4. Server validates that client `PublicKeyCredential` is valid.
5. Server then creates user entry in database, storing `credential_id` and `credential_public_key` for use later.
6. Server returns successful JSON response.

## Authentication Procedure

1. Client sends a request to the server with username.
2. Server looks up user's known keys and uses them to format a `publicKeyCredentialRequestOptions` object, then sends it back to user.
3. Client uses `navigator.credentials.get()` to generate a `PublicKeyCredential` response with signature, then sends it back to the server.
4. Server validates that the signature was encrypted properly using the private key.
5. Server then authenticates the user by setting session variables.
6. Server returns successful JSON response.

## References

WebAuthn Guide: https://webauthn.guide/