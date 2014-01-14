#!/usr/bin/python

"""
tinypass.py - Minimal, very low security, file passwording app

Checks unsigned cookies against unsalted passwords stored on disk
in plaintext; to serve large static files.

Requires bottle.py

Written by bbot@bbot.org
This is free and unencumbered software released into the public domain.
"""

from bottle import route, run, request, abort, static_file, template, get, post, BaseRequest
import pickle, os, glob, datetime

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
    data = readusers()
    try:
        row = data[filename]
    except KeyError:
        abort(404, "File not found")
    if (row['username'] == username and row['password'] == password):
        return True
    else:
        return False

@route('/password')
def password():
    return static_file('password.html', root=HTROOT)

@get('/users')
def getusers():
    """This is all you have to do to return a dict as a JSON file!
    I won't tell you how long it took me to figure that out."""
    return readusers()

@post('/users')
def postusers():
    #this bit will eventually hook into writeusers()
    foobar = request.json
    print foobar

def readusers():
    """Reads the most recently created .pkl file in as usersdict."""
    usersdict = pickle.load(open(max(glob.iglob('*.pkl'), key=os.path.getctime)))
    return usersdict

def writeusers(usersdict):
    """Writes usersdict to disk as a pickled object, with the current
    RFC3339 UTC datetime in the filename."""
    d = datetime.datetime.utcnow()
    time = d.isoformat('T') + 'Z'
    output = open('users' + time + '.pkl', 'wb')
    pickle.dump(usersdict, output)
    output.close()
    

run(host='localhost', port=8081, debug=True)

