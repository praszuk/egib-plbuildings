# EGiB – server for plbuildings
## Description
API server which is used by [josm-plbuildings-server](https://github.com/praszuk/josm-plbuildings-server) to fetch EGiB government data
and parse it to OSM format.

## How to use it
### Example .env file
```
# Database
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=database_name
POSTGRES_USER=database_user
POSTGRES_PASSWORD=database_password
```

### Development 
For development, you can install all dependencies using: 
```commandline
make install
```

Check [Makefile](Makefile) for more.
### Run development
_Note: Port 8081_
```commandline
docker compose -f docker-compose-dev.yml up
```

### Run production
_Note: Port 80_
```commandline
docker compose -f docker-compose-prod.yml up
```

## License
[MIT](LICENSE)