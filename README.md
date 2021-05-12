# jwt_boilerplate
Boilerplate code for a flask API using a JWT-based authorization scheme.

### To run:
Make git ignore changes to your development .env files by running:
```bash
git update-index --skip-worktree .env && git update-index --skip-worktree .env.db
```

Update the following files for a development environment:
- .env
- .env.db

Now changes to these files will not be tracked in git, and the environment variables already set in main's .env files will be used for continuous integration testing without having to change ```docker-compose.yml```.

Mark ```entrypoint.sh``` as executable by running:
```bash
chmod +x ./web/entrypoint.sh
```

Build and run container:
```bash
docker-compose up --build
```
