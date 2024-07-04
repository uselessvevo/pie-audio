"""
Etc. structs and models
"""
from datetime import datetime, date

DATA_TYPE_TRANSLATION: dict[type, str] = {
    str: "string",
    int: "number",
    float: "number",
    list: "array",
    tuple: "array",
    bytes: "bytes",
    bytearray: "byte array",
    date: "date",
    datetime: "date with time",
}