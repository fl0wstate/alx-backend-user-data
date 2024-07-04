#!/usr/bin/env python3
"""Mock function of a logger builtin function"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 seperator: str) -> str:
    """function that tries to replicate the logger function"""
    data = message.split(';')
    for idx, item in enumerate(data):
        if item.split('=')[0] in fields:
            data[idx] = item.replace(item.split('=')[1], redaction)
    return f"{seperator}".join(data)
