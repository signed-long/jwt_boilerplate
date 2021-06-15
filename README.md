# jwt_boilerplate
Boilerplate code for a flask API using a JWT-based authorization scheme.

### To build and run service:
```bash
docker-compose up --build
```

### To build and run tests:
```bash
docker-compose -f docker-compose-tests.yml up --exit-code-from auth --build
```
