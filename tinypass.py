#!/usr/bin/python

"""
tinypass.py - Minimal, very low security file authentication app

Checks unsigned cookies against unsalted passwords stored on disk
in plaintext; to serve large static files.

Requires bottle.py

Written by bbot@bbot.org
This is free and unencumbered software released into the public domain.
"""

from bottle import route, run, request, abort, static_file
import pickle

# This is where the static files you're serving should live.
#HTROOT = '/srv/www/'

# Or you can import them from an external module, if you're being fancy
from constants import HTROOT

@route('/<filename>')
def index(filename):
    username = request.get_cookie("username")
    password = request.get_cookie("password")
    if not username:
        return "login form\n";
    elif (check_password(filename, username, password)):
        return static_file(file, root=HTROOT)
    else:
        return "bad username or password\n";

def check_password(filename, username, password):
    data = pickle.load(open('users.pkl', 'rb'))
    try:
        row = data[filename]
    except KeyError:
        abort(404, "File not found")
    if (row['username'] == username and row['password'] == password):
        return True
    else:
        return False

run(host='localhost', port=8080, debug=True)

