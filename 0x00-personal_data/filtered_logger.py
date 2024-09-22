#!/usr/bin/env python3
"""
filtered_logger module
"""
import re
import logging
from typing import List
import os
import mysql.connector

# PII_FIELDS constant
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character is separating all
                   fields in the log line.

    Returns:
        The obfuscated log message.
    """
    pattern = f'({"|".join(fields)})=.*?{separator}'
    return re.sub(
        pattern,
        lambda m: m.group(0).split('=')[0] + f'={redaction}{separator}',
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize RedactingFormatter """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR
        )
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Returns a logger object configured to handle PII data.

    Returns:
        A logging.Logger object configured to handle PII data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to a secure MySQL database using credentials from
    environment variables.

    Returns:
        A MySQLConnection object to the database.
    """
    # Retrieve database credentials from environment variables
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the MySQL database
    return mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=database
    )
