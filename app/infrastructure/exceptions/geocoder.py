class IncorrectGeolocation(Exception):
    pass


class GeocodingFailed(Exception):
    pass


class LotsOfGeocodingResults(Exception):
    address: str
