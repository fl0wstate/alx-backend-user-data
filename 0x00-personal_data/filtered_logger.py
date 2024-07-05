#!/usr/bin/env python3
"""Mock function of a logger builtin function"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    """Redacts specified fields in a message using regex."""
    return re.sub(r'(\w+)=([^;]+)(.)',
                  lambda match:
                  f"{match.group(1)}={redaction}{separator}"
                  if match.group(1) in fields
                  else f"{
                    match.group(0).replace(
                        match.group(0)[-1], separator
                        )}",
                  message)
