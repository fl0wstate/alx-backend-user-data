#!/usr/bin/env python3
""" Main 0
"""
import uuid
import base64
from models.user import User
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


a = Auth()


# res = a.require_auth(None, ["/api/v1/status/"])
# if not res:
#     print("require_auth must return True when path is None")
#     exit(1)
# print("OK")
#
#
# res = a.require_auth("/api/v1/status/", None)
# if not res:
#     print("require_auth must return True when excluded_paths is None")
#     exit(1)
# print("OK")
#
# res = a.require_auth("/api/v1/status/", [])
# if not res:
#     print("require_auth must return True when excluded_paths is empty")
#     exit(1)
# print("OK")
#
# res = a.require_auth("/api/v1/users/", ["/api/v1/stats/", "/api/v1/status/"])
# if not res:
#     print("require_auth must return True when path is not in excluded_paths")
#     exit(1)
# print("OK")
#
# res = a.require_auth("/api/v1/status/", ["/api/v1/stats/", "/api/v1/status/", "/api/v1/users/"])
# if res:
#     print("require_auth must return False when path is in excluded_paths")
#     exit(1)
# print("OK")
#
# res = a.require_auth("/api/v1/status", ["/api/v1/stats/", "/api/v1/status/", "/api/v1/users/"])
# if res:
#     print("require_auth must return False when path is in excluded_paths - slash tolerant")
#     exit(1)
# print("OK")
#


# print(a.require_auth(None, None))
# print(a.require_auth(None, []))
# print(a.require_auth("/api/v1/status/", []))
# print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))

# a = BasicAuth()

# print(a.extract_base64_authorization_header(None))
# print(a.extract_base64_authorization_header(89))
# print(a.extract_base64_authorization_header("Holberton School"))
# print(a.extract_base64_authorization_header("Basic Holberton"))
# print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
# print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
# print(a.extract_base64_authorization_header("Basic1234"))


# print(a.decode_base64_authorization_header(None))
# print(a.decode_base64_authorization_header(89))
# print(a.decode_base64_authorization_header("Holberton School"))
# print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
# print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
# print(a.decode_base64_authorization_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))


# print(a.extract_user_credentials(None))
# print(a.extract_user_credentials(89))
# print(a.extract_user_credentials("Holberton School"))
# print(a.extract_user_credentials("Holberton:School"))
# print(a.extract_user_credentials("bob@gmail.com:toto1234"))


# """ Create a user test """
# user_email = str(44)
# user_clear_pwd = str(55)
# user = User()
# user.email = user_email
# user.first_name = "Bob"
# user.last_name = "Dylan"
# user.password = user_clear_pwd
# print("New user: {}".format(user.display_name()))
# user.save()
# print(user.count())
#
# """ Retreive this user via the class BasicAuth """
#
# a = BasicAuth()
#
# u = a.user_object_from_credentials(None, None)
# print(u.display_name() if u is not None else "None")
#
# u = a.user_object_from_credentials(89, 98)
# print(u.display_name() if u is not None else "None")
#
# u = a.user_object_from_credentials("email@notfound.com", "pwd")
# print(u.display_name() if u is not None else "None")
#
# u = a.user_object_from_credentials(user_email, "pwd")
# print(u.display_name() if u is not None else "None")
#
# u = a.user_object_from_credentials(user_email, user_clear_pwd)
# print(u.display_name() if u is not None else "None")

user_email = "bob@hbtn.io"
user_clear_pwd = "H0lbertonSchool98!"
user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {} / {}".format(user.id, user.display_name()))
user.save()

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))
