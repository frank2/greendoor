#!/usr/bin/env python

import gevent
import gevent.monkey
gevent.monkey.patch_all()

from code import InteractiveConsole

import gevent.backdoor
from gevent.hub import getcurrent

import hashlib
import os
import sys

__all__ = ['Greendoor']

class Greendoor(gevent.backdoor.BackdoorServer):
    def __init__(self, listener, locals=None, banner=None, password=None, **server_args):
        if password is None:
            raise ValueError('password not present')

        self.salt = os.urandom(64)
        self.hash = hashlib.sha256(password + self.salt).hexdigest()
        
        gevent.backdoor.BackdoorServer.__init__(self, listener, locals, banner, **server_args)

    def handle(self, conn, address):
        file_obj = conn.makefile(mode='rw')
        file_obj = gevent.backdoor._fileobject(conn, file_obj, self.stderr)

        getcurrent()._fileobj = file_obj
        getcurrent().switch_in()

        file_obj.write('Password: ')
        password = file_obj.readline().rstrip('\r\n')
        salted = password + self.salt
        hash_digest = hashlib.sha256(salted).hexdigest()

        if not hash_digest == self.hash:
            file_obj.write('\nWrong password.\n')
            conn.close()
            file_obj.close()
            return

        try:
            console = InteractiveConsole(self._create_interactive_locals())

            if sys.version_info[:3] >= (3, 6, 0):
                console.interact(banner=self.banner, exitmsg='')
            else:
                console.interact(banner=self.banner)
        except SystemExit:
            if hasattr(sys, 'exc_clear'):
                sys.exc_clear()
        finally:
            conn.close()
            file_obj.close()
