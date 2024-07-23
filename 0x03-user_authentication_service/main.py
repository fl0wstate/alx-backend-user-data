#!/usr/bin/env python3
"""Main file for testing all the created function"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Getting all the registered register_user but filtering
    them according to the email provided"""
    for i in range(2):
        endpoint_one = f"{BASE_URL}/users"
        data = {
            "email": email,
            "password": password
        }
        resp = requests.post(endpoint_one, data=data)
        if i == 0:
            assert resp.status_code == 200
            assert resp.json() == {
                "email": email,
                "message": "user created"
            }
        elif i == 1:
            assert resp.status_code == 400
            assert resp.json() == {
                "message": "email already registered"
            }


def log_in(email: str, password: str) -> str:
    """ Log in with right password"""
    url = f"{BASE_URL}/sessions"
    data = {
        "email": email,
        "password": password
    }
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {'email': 'user.email', 'message': 'logged in'}
    return resp.cookies["session_id"]


def log_in_wrong_password(email: str, password: str) -> None:
    """Logging in with in valid data spec password"""
    endpoint_two = f"{BASE_URL}/sessions"
    data = {
        "email": email,
        "password": password
    }
    resp = requests.post(endpoint_two, data=data)
    assert resp.status_code == 401


def profile_unlogged() -> None:
    """ Profile of users who are not logged in"""
    url = f"{BASE_URL}/profile"
    resp = requests.get(url)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Profile of a logged user"""
    url = f"{BASE_URL}/profile"
    cookies = {
        "session_id": session_id
    }
    resp = requests.get(url, cookies=cookies)
    assert resp.status_code == 200
    assert resp.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ Log out a user test"""
    url = f"{BASE_URL}/sessions"
    cookies = {
        "session_id": session_id
    }
    resp = requests.delete(url, cookies=cookies)
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """ Reseting password test"""
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email
    }
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    assert resp.json()["email"] == email
    assert "reset_token" in resp.json()
    return resp.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update user password test"""
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    resp = requests.put(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'Password updated'}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
