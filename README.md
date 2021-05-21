# jwt_boilerplate
Boilerplate code for a flask API using a JWT-based authorization scheme.

#### Environment variables:
Default environment variables in the repo will work but you may want to change them for development or testing purposes ie. for changing token expiration times.

#### To run:
Mark ```entrypoint.sh``` as executable by running:
```bash
chmod +x ./web/entrypoint.sh
```

Build and run containers:
```bash
docker-compose up --build
```
