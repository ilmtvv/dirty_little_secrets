# Context
HTTP service for one-time secrets.
It should allow you to create a secret, set a passphrase to open it, and generate a code that can be used to read the secret only once. No UI is needed, it must be a JSON Api service.

# Stack
- FastAPI
- Redis

# Docs
```
host + port + /docs -> swagger
```

# Run
Rename or copy and paste .env.docker and install name file like .env! If you want a custom run overwrite .env!
```
docker-compose up --build
```

# PEP
```
flake8
```

# Test
```
pytest
```
