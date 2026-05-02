# EGiB – server for plbuildings
## Description
API server which is used by [josm-plbuildings-server](https://github.com/praszuk/josm-plbuildings-server) to fetch EGiB government data
and parse it to OSM format.

## How to use it

Copy `example.env` to `.env`:
```commandline
cp example.env .env
```
and change (at least db pass).

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