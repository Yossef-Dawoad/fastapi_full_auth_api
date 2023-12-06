# FASTAPI *Complete Auth system

the project aims as a resoursefull best practices for building production grade web applications as possible with fastapi starting with all you need about authentication.

# Installation 
### Method 1 - Docker
```bash
cd fastapi_full_auth_api

#build the servies 
docker-compose build

# run the services
docker-compose run 

# run the latest migrations if any
docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head

```

## Usages (Comming Sooon)

## Public Routes Available  


## Features
[x] Simple User creation or registeration process
[x] injecting email verification system into the registeration process
[ ] welcome emaill with succesfull email verification
[ ] user login process
[ ] test coverage of up 90%
[ ] 100% migration to sqlalchemy 2.x sentax
[ ] 100% migration to pydantic 2.x sentax 