#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

a = Auth()
# print(a.require_auth(None, None))
# print(a.require_auth(None, []))
# print(a.require_auth("/api/v1/status/", []))
# print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))

a = BasicAuth()

print(a.extract_base64_authorization_header(None))
print(a.extract_base64_authorization_header(89))
print(a.extract_base64_authorization_header("Holberton School"))
print(a.extract_base64_authorization_header("Basic Holberton"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
print(a.extract_base64_authorization_header("Basic1234"))
