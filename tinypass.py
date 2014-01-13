#!/usr/bin/python

"""
tinypass.py - Minimal, very low security, file passwording app

Checks unsigned cookies against unsalted passwords stored on disk
in plaintext; to serve large static files.

Requires bottle.py

Written by bbot@bbot.org
This is free and unencumbered software released into the public domain.
"""

from bottle import route, run, request, abort, static_file, template
import pickle

# This is where the static files you're serving should live.
#HTROOT = '/srv/www/'

# Or you can import them from an external module, if you're being fancy
from constants import HTROOT

@route('/tinypass/<filename>')
def index(filename):
    username = request.get_cookie("username")
    password = request.get_cookie("password")
    if not username:
        return template('login')
    elif (check_password(filename, username, password)):
        try:
            return static_file(filename, root=HTROOT)
        except AttributeError:
            abort(404, "Username and password correct, but the file on the disk was not found. Filename typo?")
    else:
        return template('login', badpassword=badpassword)

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

run(host='localhost', port=8081, debug=True)

