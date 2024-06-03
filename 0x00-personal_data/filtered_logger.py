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
<<<<<<< Updated upstream
        message)
=======
        message
    )


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Filters a log line."""
    patterns = create_patterns(fields, redaction, separator)
    return re.sub(patterns['extract'], patterns['replace'], message)
>>>>>>> Stashed changes


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
<<<<<<< Updated upstream
=======
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream

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
=======
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """Logs the information about user records in a table."""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


if __name__ == "__main__":
    main()
>>>>>>> Stashed changes
