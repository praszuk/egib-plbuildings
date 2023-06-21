class ParserError(Exception):
    pass


class InvalidKeyParserError(ParserError):
    pass


class PowiatNotFound(Exception):
    pass


class PowiatDataNotFound(Exception):
    pass


class PowiatNotSupported(Exception):
    pass
