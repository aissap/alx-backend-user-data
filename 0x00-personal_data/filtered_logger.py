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
    """
    Obfuscate specified fields in the log message.

    Args:
        fields: list of strings.
        redaction: the value by which the fields will be obfuscated.
        message: string "log line".
        separator: character used to separate all fields in the log line.

    Returns:
        log message with obfuscated fields.
    """
    return re.sub(
        r'(?<=^|{})(?:{}=[^{}]+)(?={}|$)'.format(
            separator, '|'.join(fields), separator, separator),
        lambda match: '{}={}'.format(
            match.group().split('=')[0], redaction), message)
