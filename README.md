Creating a random secret_key:

    import secrets
    secret_key = secrets.token-urlsafe(32)
    print(secret_key)

Creating a private and public keys for JWT authentication

    openssl genrsa -out jwt-private.pem 2048
    openssl rsa -in jwt.private.pem -outform PEM -pubout -out jwt-public.pem