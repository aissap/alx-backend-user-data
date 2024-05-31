#!/usr/bin/env python3
"""
Filtered Logger
"""

import os
import re
import logging
import mysql.connector
from typing import List, Tuple


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """Specifie the  fields in the log message."""
    return re.sub(
        r'(?<=^|{})(?:{}=[^{}]+)(?={}|$)'.format(
            separator, '|'.join(fields), separator, separator),
        lambda match: '{}={}'.format(match.group().split('=')[0], redaction),
        message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a LogRecord."""
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


def get_logger() -> logging.Logger:
    """Creates a new logger for user data."""
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to a database."""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    try:
        connection = mysql.connector.connect(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_pwd,
            database=db_name,
        )
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return None


def main():
    """Query the users table in the database."""
    db = get_db()
    if not db:
        return

    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users;")
        for row in cursor:
            log_message = '; '.join(
                f"{field}={value if field not in PII_FIELDS else '***'}"
                for field, value in zip(cursor.column_names, row)
            )
            logging.info(f"[HOLBERTON] user_data INFO {log_message}")
    except mysql.connector.Error as e:
        print("Error executing query:", e)
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
