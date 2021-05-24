# jwt_boilerplate
Boilerplate code for a flask API using a JWT-based authorization scheme.

### To build and run service:
```bash
docker-compose up --build
```

### To build and run tests:
```bash
docker-compose -f docker-compose-tests.yml up --exit-code-from web --build
```

#### Environment variables:
Default environment variables in the repo will work but you may want to change them for development or testing purposes (ie. for changing token expiration times) and must change them in production (secrets).

To make sure git does't track changes to .env (the default values are used for CI testing and should stay as they are) files run:
```bash
git update-index --skip-worktree .env \
    && git update-index --skip-worktree .env.db \
    && git update-index --skip-worktree .env.test \
    && git update-index --skip-worktree .env.test.db
```
