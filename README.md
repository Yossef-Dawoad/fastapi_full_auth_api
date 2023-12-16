# FASTAPI *Complete Auth system

the project aims as a resourceful best practice for building production-grade web applications as possible with fastapi starting with all you need about authentication.

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
- [x] Simple User creation or registration process  
- [x] injecting an email verification system into the registration process  
- [x] welcome email with successful email verification  
- [x] user signup & create email 
- [x] verify account process with mail verifcation system 
- [x] user login process
- [ ] test coverage of up 90%  
- [ ] 100% migration to sqlalchemy 2.x syntax  
- [ ] 100% migration to pydantic 2.x syntax   
