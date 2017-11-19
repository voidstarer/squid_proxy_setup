#!/usr/bin/env python2


import os
import sys
import platform
import shutil


SQUID_CONFIGURATION_PATH = "/etc/squid3/squid.conf"
PASSWD_FILE = "/etc/squid3/passwd"

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

def mycopy(pathfrom, topath):
    '''
    Simple Copy handler

    '''
    status = -1
    if os.path.exists(pathfrom) is False:
        print "Path Does not exist"
        return status
    try :
        shutil.copy(pathfrom, topath)
        status = 0
    except IOError, PermissionDeniedError:
        status = -9
        print IOError
        print PermissionDeniedError
    return status


def deleteContent(fName):
    '''
    Empty a  file

    '''
    status = -1

    try:
        with open(fName, "w"):
            pass
        status = 0
    except IOError, PermissionDeniedError:
        print IOError
        print PermissionDeniedError
        print "File as not able to modify"

    return status


def configuration_copy_handler(newfile):
    '''
    configuration files properly copy handling

    '''
    basepath, filename = os.path.split(SQUID_CONFIGURATION_PATH)
    backupfile = filename + ".backup"
    print backupfile
    backuppath = basepath + os.sep + backupfile
    print backuppath
    print "creating backup ... "
    filepath = basepath + os.sep + filename
    p = mycopy(filepath)
    if p is not 0 :
        print "backup didnt happen, some issues with Copying...let's contact Debapriya"
        exit(-13)
    print "Backup Done, time to rewrite the configuration file now"
    deleteContent(filepath)
    


def adduser(username, password):
    '''
    a function that takes an Username and Password and creates the user
    '''
    from subprocess import STDOUT, check_call, PIPE, Popen
    # a = check_call(['apt-get', 'install', '-y', packagetoinstall], stdout=STDOUT, stderr=STDOUT)
    p = Popen(['htpasswd', '-b', PASSWD_FILE, username, password], stdout=PIPE)
    print p.communicate()
    if p.returncode is 0 :
        print "Success in adding user %s", username
    return p.returncode


def handlemultipleuseradd(userdict):
    '''
    This function area is for multiple user addition

    '''
    status = 0
    from subprocess import STDOUT, check_call, PIPE, Popen
      if os.path.exists(PASSWD_FILE) is False:
        print "passwd path does not exist"
        print "creating one ...."
        p = Popen(['touch', PASSWD_FILE], stdout=PIPE)
        print p.communicate()
        if p.returncode is not 0 :
            print PASSWD_FILE + "File creation failed"
            print "Exiting.."
            status = -13
            exit(-13)
        else :
            print "File got created..."
            status = 1
        for user in userdict.keys:
            password = userdict[user]
            status = adduser(user, password)
            if status is not 0 :
                print "Some Error while adding users..."
                break
            else:
                status = 0

        print "Added all users from list ..."
        return status




def main():
    '''
    Main() : main functionality of the code
    '''
    if os.name is 'Posix' or 'posix':
        # checking a valid POSIX Shell
        print "Hi " + os.getenv('USER') + ", this looks like a POSIX Shell"

        if os.geteuid() is not 0 :
            print "This program is supposed to be run as root"
            print "N00B$ are not supposed to run this"
            print "May the force be with you, Motherfucker!"
            exit(-13)

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
                    print "Upgrade Success"
                else :
                    print "Something failed, try again later or communicate to Debapriya"

                packagestoinstall = ["sl"]
                for packagetoinstall in packagestoinstall:
                    if apt_install(packagetoinstall) is 0 :
                        print "Install Success"
                    else :
                        print "Something failed, try again later or communicate to Debapriya"
                        exit(-9)

                print "Installation of all packages complete, time to configure ....."
                print copy("file1", "file2")





        elif sys.platform is 'darwin':
            print "Okay, you have a Mac, work in progress!"
    else:
        print "Sorry, Not a Posix Shell"



if __name__=="__main__":
    main()
