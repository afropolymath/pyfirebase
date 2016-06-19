import sys
import signal
from pyfirebase import Firebase

firebase = Firebase('https://apitest-72809.firebaseio.com/')

# Create a reference to the root by not passing in paramters to the ref function
root = firebase.ref()


# This function will be called everytime the event happens
def print_data(event, data):
    print event
    print data

# We can the event listener to the root ref. We also specify that print_data should be called on event
root.on('child_changed', callback=print_data)


# Extra logic to turn on listener when we quit
def signal_handler(signal, frame):
    print "Trying to exit"
    root.off()
    sys.exit(0)

# Binding Ctrl + C signal to signal_handler
signal.signal(signal.SIGINT, signal_handler)
signal.pause()
