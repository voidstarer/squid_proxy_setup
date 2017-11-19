#!/usr/bin/env python2


import os
import sys
import platform

def apt_update():
    '''
    function to update the Packages
    '''
    from subprocess import STDOUT, check_call, PIPE, Popen
    # a = check_call(['apt-get', 'install', '-y', packagetoinstall], stdout=STDOUT, stderr=STDOUT)
    p = Popen(['apt-get', 'update'], stdout=PIPE)
    print p.communicate()
    if p.returncode is 0 :
        print "Success"
    return p.returncode


def apt_upgrade():
    '''
    function to upgrade the Packages
    '''
    from subprocess import STDOUT, check_call, PIPE, Popen
    # a = check_call(['apt-get', 'install', '-y', packagetoinstall], stdout=STDOUT, stderr=STDOUT)
    p = Popen(['apt-get', 'upgrade'], stdout=PIPE)
    print p.communicate()
    if p.returncode is 0 :
        print "Success"
    return p.returncode


def apt_install(packagetoinstall):
    '''
    function to install packages
    '''
    packagetoinstall = str(packagetoinstall)
    from subprocess import STDOUT, check_call, PIPE, Popen
    # a = check_call(['apt-get', 'install', '-y', packagetoinstall], stdout=STDOUT, stderr=STDOUT)
    p = Popen(['apt-get', 'install', '-y', packagetoinstall], stdout=PIPE)
    print p.communicate()
    if p.returncode is 0 :
        print "Success"
    return p.returncode



def main():
    '''
    Main() : main functionality of the code
    '''
    if os.name is 'Posix' or 'posix':
        # checking a valid POSIX Shell
        print "Hi " + os.getenv('USER') + ", this looks like a POSIX Shell"

        if 'linux' in sys.platform :
            print "Okay, you have a Linux OS, this script is compatible"
            print "Now checking if you have Ubuntu"
            if 'ubuntu' or 'Ubuntu' in platform.linux_distribution():
                print platform.linux_distribution()
                print "Yippeeeee! you have an Ubuntu OS : " \
                + platform.linux_distribution()[0] + " " \
                + platform.linux_distribution()[1] + " " \
                + platform.linux_distribution()[2]

                print "Now Time for work!!"
                if apt_update() is 0 :
                    print "Update Success"
                else :
                    print "Something failed, try again later or communicate to Debapriya"

                if apt_upgrade() is 0 :
                    print "Update Success"
                else :
                    print "Something failed, try again later or communicate to Debapriya"

                packagestoinstall = ["sl", "ls"]
                for packagetoinstall in packagestoinstall:
                    if apt_install(packagetoinstall) is 0 :
                        print "Install Success"
                    else :
                        print "Something failed, try again later or communicate to Debapriya"
                        exit(-9)


        elif sys.platform is 'darwin':
            print "Okay, you have a Mac, work in progress!"
    else:
        print "Sorry, Not a Posix Shell"



if __name__=="__main__":
    main()
