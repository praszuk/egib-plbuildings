class ParserError(Exception):
    pass


class InvalidKeyParserError(ParserError):
    pass


class CountyNotFound(Exception):
    pass


class CountyDataNotFound(Exception):
    pass


class CountyNotSupported(Exception):
    pass
