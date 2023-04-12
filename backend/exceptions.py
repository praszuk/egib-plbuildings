class ParserError(Exception):
    pass


class ParserNotFound(ParserError):
    pass


class InvalidKeyParserError(ParserError):
    pass


class PowiatNotFound(Exception):
    pass
