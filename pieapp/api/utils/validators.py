import dateutil.parser


def date_validator(value: str):
    try:
        return dateutil.parser.parse(value, fuzzy=True)
    except dateutil.parser.ParserError:
        return False
