# EGiB – server for plbuildings
## Description
API server which is used by [josm-plbuildings-server](https://github.com/praszuk/josm-plbuildings-server) to fetch EGiB government data
and parse it to OSM format.

## How to use it
### Development 
To run dev, you can use docker:
```commandline
docker-compose -f docker-compose-dev.yml up
```

or you can install GDAL library (libgdal-dev) in your OS and run: 
```commandline
make install
make run
```

Check [Makefile](Makefile) for more.
### Production
1. Install GDAL library in your OS (libgdal-dev) Python3 and Virtualenv.
2. Type:`make prod-install` to install requirements (you can run `make clean` before).
3. Run server using `make prod-run`.

## License
[MIT](LICENSE)