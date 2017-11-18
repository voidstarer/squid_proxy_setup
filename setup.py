#!/usr/bin/env python2


import os

def main():
    '''
    Main() : main functionality of the code
    '''
    if os.name is 'Posix' or 'posix':
        print "Hi " + os.getenv('USER') + ", this looks like a POSIX Shell"
    else:
        print "Sorry, Not a Posix Shell"



if __name__=="__main__":
    main()
