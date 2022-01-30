# Notes 
This is a WIP and purely for practice:
- Barebones CRUD API built with FastAPI and Docker
- Use PostgreSQL in a docker container as database
- Deploy containers with Docker Compose on GCP Compute Engine VM
- Automate deployment of containers on push to repo with Github Actions
    - On a PR, run unit tests
    - On a push to main: ssh into VM; git pull changes; docker-compose up
