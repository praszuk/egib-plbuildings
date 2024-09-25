# EGiB – server for plbuildings
## Description
API server which is used by [josm-plbuildings-server](https://github.com/praszuk/josm-plbuildings-server) to fetch EGiB government data
and parse it to OSM format.

## How to use it
### Development 
For development, you can install all dependencies using: 
```commandline
make install
```

### Run development
_Note: Port 8081_
```commandline
make drun
```

### Run production
_Note: Port 80_
```commandline
make dprod-run
```

Check [Makefile](Makefile) for more.
## License
[MIT](LICENSE)