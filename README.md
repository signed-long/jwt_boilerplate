# jwt_boilerplate
Boilerplate code for a flask API using a JWT-based authorization scheme.

### To run:
Make git ignore changes to your development .env files by running:
```bash
git update-index --skip-worktree .env \
    && git update-index --skip-worktree .env.db \
    && git update-index --skip-worktree .env.test \
    && git update-index --skip-worktree .env.test.db
```

Default values for these files will work but you may want to change them for development or testing purposes ie. for changing token expiration times:

Mark ```entrypoint.sh``` as executable by running:
```bash
chmod +x ./web/entrypoint.sh
```

Build and run containers:
```bash
docker-compose up --build
```
