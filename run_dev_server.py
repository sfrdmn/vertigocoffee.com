#!/usr/bin/env python
import pty, os, io, signal, sys, threading, subprocess

print "Starting compass and django daemons..."

m1, s1 = pty.openpty()
m2, s2 = pty.openpty()

server = subprocess.Popen(['python', 'manage.py', 'runserver'], stdout=s2, stderr=s2, close_fds=True, shell=False)
compass = subprocess.Popen(['compass', 'watch', 'vertigocoffee/static'], stdout=s1, stderr=s1, close_fds=True)

def server_thread():
  for line in io.open(m1, 'r'):
    print line

def compass_thread():
  for line in io.open(m2, 'r'):
    print line

t1 = threading.Thread(target=server_thread)
t1.daemon = True
t2 = threading.Thread(target=compass_thread)
t2.daemon = True

def sig_handler(signal, frame):
  print "Stopping compass and django daemons..."
  server.kill()
  compass.kill()
  sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

t1.start()
t2.start()

signal.pause()

t1.join()
t2.join()
