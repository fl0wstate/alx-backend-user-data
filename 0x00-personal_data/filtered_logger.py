#!/usr/bin/env python3
"""Mock function of a logger builtin function"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    """Redacts specified fields in a message using regex."""
    def match_handler(match: str) -> str:
        """function that handles the matching pattern"""
        field, value, sep = match.groups()
        if field in fields:
            return f"{field}={redaction}{seperator}"
        else:
            return f"{field}={value}{seperator}"
    return re.sub(r'(\w+)=([^;]+)(.)', match_handler, message)
