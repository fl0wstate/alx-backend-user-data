#!/usr/bin/env python3
import uuid
# from api.v1.auth.basic_auth import BasicAuth
from models.user import User

""" Create a user test """
user_email = str(uuid.uuid4())
user_clear_pwd = str(uuid.uuid4())
user = User()
user.email = user_email
user.first_name = "Bob"
user.last_name = "Dylan"
user.password = user_clear_pwd
print("New user: {}".format(user.display_name()))
user.save()
print(user.all())
print(user.count())
copy = user.search({"first_name": "Bob", "last_name": "Dylan"})
for match in copy:
    print(match.email, match.first_name, match.last_name)
