#!/usr/bin/env python3
"""Mock function of a logger builtin function"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log message obfuscated'''
    pattern = '|'.join(f"(?<={field}=)[^{separator}]+" for field in fields)
    return re.sub(pattern, redaction, message)
