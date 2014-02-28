#!/usr/bin/python

"""
tinypass.py - Minimal, very low security, file passwording app

Checks unsigned cookies against unsalted passwords stored on disk
in plaintext; to serve large static files.

Requires bottle.py

Written by bbot@bbot.org
This is free and unencumbered software released into the public domain.
"""

from bottle import route, run, request, abort, static_file, template, get, post
import pickle, os, glob, datetime

# This is where the static files you're serving should live.
#HTROOT = '/srv/www/'

# Or you can import them from an external module, if you're being fancy
from constants import HTROOT

@get('/<filename>')
def index(filename):
    username = request.get_cookie("username")
    password = request.get_cookie("password")
    if not username:
        return template('login')
    elif (check_password(filename, username, password)):
        if (filename == 'password.html'):
            return template('password.html', usersdict=readusers(), bizz=HTROOT)
        else:
            try:
                return static_file(filename, root=HTROOT)
            except AttributeError:
                abort(404, "Username and password correct, but the file on the disk was not found. Filename typo?")
    else:
        badpassword = True
        return template('login.html', badpassword=badpassword)

def check_password(filename, username, password):
    usersdict = readusers()
    try:
        row = usersdict[filename]
    except KeyError: #If the filename isn't in the usersdict then it's not passworded, so we want to let anyone see it
        return True
    if (row['username'] == username and row['password'] == password):
        return True
    else:
        return False

@post('/password.html')
def postpassword():
    """Uses POSTed form data to update `usersdict`, then calls `writeusers()`"""
    print 'foo'
    usersdict = readusers()
    setUsername = request.forms.get('username')
    setPassword = request.forms.get('password')
    setFilename = request.forms.get('filename')
    username = request.get_cookie("username")
    password = request.get_cookie("password")
    if (check_password('password.html', username, password)):
        print 'foo2'
        usersdict[setFilename] = {'username': setUsername, 'password': setPassword}
        print usersdict
        writeusers(usersdict)
        return template('password.html', usersdict=readusers(), bizz=HTROOT)
    else:
        print 'foo3'
        abort(503, "Bad username or password")

def readusers():
    """Reads the most recently created .pkl file into memory as `usersdict`."""
    try:
        usersdict = pickle.load(open(max(glob.iglob('*.pkl'), key=os.path.getctime)))
    except ValueError: #Unless we don't have a user database yet, in which case
        usersdict = {}
    return usersdict

def writeusers(usersdict):
    """Writes `usersdict` to disk as a pickled object, with the current
    RFC3339 UTC datetime in the filename."""
    d = datetime.datetime.utcnow()
    time = d.isoformat('T') + 'Z'
    output = open('users' + time + '.pkl', 'wb')
    pickle.dump(usersdict, output)
    output.close()

#These two are unfortunately ugly, so I hid them down at the bottom.
@route('/float-label.js')
def floatlabel():
    return static_file('float-label.js', root='.')

@route('/style.css')
def style():
    return static_file('style.css', root='.')

#And this just starts the server.
run(host='localhost', port=8081, debug=False)

