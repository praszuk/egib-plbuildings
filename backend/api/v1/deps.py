from fastapi import Query


class Location:
    def __init__(
        self,
        lat: float = Query(gt=-90, lt=90),
        lon: float = Query(gt=-180, lt=180),
    ):
        self.lat = lat
        self.lon = lon
