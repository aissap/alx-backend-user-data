#!/usr/bin/env python3
"""
Filtered Logger
"""

import os
import re
import logging
import mysql.connector
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Formatter class """

    def __init__(self, fields: Tuple[str, ...]):
        super().__init__("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        for field in self.fields:
            message = message.replace(field + "=", field + "=***;")
        return message


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """The log message."""
    for field in fields:
        message = re.sub(rf"{field}=.*?({separator}|$)", f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """Configures the logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the database."""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_name
    )


def main():
    """Get user data from the database and logs it."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor.fetchall():
        filtered_row = "; ".join([f"{field}={value}" for field, value in zip(cursor.column_names, row)])
        logger.info(filtered_row)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
