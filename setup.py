#!/usr/bin/env python2

'''

@Author : Debapriya Das
@Email : yodebu@gmail.com

'''


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

def iptables_install():
    servicefilepath = "/etc/init.d"
    file = "iptables-persistent"

    pathto = servicefilepath + os.sep + file
    print pathto
    print mycopy(file, servicefilepath)
    print os.chmod(servicefilepath, 0755)
    command = "update-rc.d iptables defaults"
    print os.system(command)


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
    p = mycopy(filepath, backuppath)
    if p is not 0 :
        print "backup didnt happen, some issues with Copying...let's contact Debapriya"
        exit(-13)
    print "Backup Done, time to rewrite the configuration file now"
    deleteContent(filepath)
    print "Deleted file contents..."
    p = mycopy(newfile,filepath)
    if p is not 0 :
        print "new file copy didnt happen, some issues with Copying...let's contact Debapriya"
        exit(-13)
    print "new file replaced"



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
        for user in userdict.keys():
            password = userdict[user]
            status = adduser(user, password)
            print password, status
            if status is not 0 :
                print "Some Error while adding users..."
                break
            else:
                status = 0

        print "Added all users from list ..."
        return status




def getportlist(conffile):
    '''
    read configuration file and extract port numbers
    '''
    portlist = [] # will have SSH by default
    file = open(conffile,'r')
    lines = file.readlines()
    for line in lines:
        if line[0] is not '#' and "http_port" in line and line[0] is 'h':
            http_port, port = line.split()
            portlist.append(port)

    file.close()
    return portlist


def handleservice(package, command):
    if command not in ['save', 'restart', 'stop']:
        print "Invalid command"
        return -13
    from subprocess import STDOUT, check_call, PIPE, Popen
    p = Popen(['service', package, command], stdout=PIPE)
    print p.communicate()
    if p.returncode is 0 :
        print "Success"
    return p.returncode




def iptable_exec(exec_string):
    '''
    takes an IPTable command string and executes it
    '''

    iptable = ["iptables"]
    commandlist = exec_string.split()
    for command in commandlist:
        iptable.append(command)
    from subprocess import STDOUT, check_call, PIPE, Popen
    p = Popen(iptable, stdout=PIPE)
    print p.communicate()
    if p.returncode is 0 :
        print "Success"
    return p.returncode



def firewall_configuration(conffilepath):
    space = " "
    ports = getportlist(conffilepath)
    print "list of ports : "
    print ports
    if 'PORT' in ports:
        ports.remove('PORT')
    for port in ports:
        rulestring = "-I INPUT -p tcp --dport" + space + port + space + "-j ACCEPT"
        status = iptable_exec(rulestring)
        if status is not 0:
            print "Something is wrong...call Debapriya"
            exit(-5)

    rulestring = "-I INPUT -p tcp --dport" + space + "22" + space + "-j ACCEPT"
    status = iptable_exec(rulestring)
    iptable_exec("-A INPUT -i lo -j ACCEPT")
    iptable_exec("-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")
    iptable_exec("-A INPUT -j DROP")

    handleservice("iptables-persistent", "save")
    handleservice("iptables-persistent", "restart")

    handleservice("squid3", "restart")

    iptable_exec("-D INPUT -j DROP")
    iptable_exec("-A INPUT -p icmp -j ACCEPT")
    iptable_exec("-A INPUT -j DROP")

    handleservice("iptables-persistent", "save")
    handleservice("iptables-persistent", "restart")

    handleservice("squid3", "restart")

    print "Done!"





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
                print "You have an Ubuntu OS : " \
                + platform.linux_distribution()[0] + " " \
                + platform.linux_distribution()[1] + " " \
                + platform.linux_distribution()[2]
                if "trusty" not in platform.linux_distribution()[2] :
                    print "only for 14.04, run on 14.04 only"
                    exit(-14)

                print "Yippee!"
                print "Now Time for work!!"
                if apt_update() is 0 :
                    print "Update Success"
                else :
                    print "Something failed, try again later or communicate to Debapriya"

                if apt_upgrade() is 0 :
                    print "Upgrade Success"
                else :
                    print "Something failed, try again later or communicate to Debapriya"

                packagestoinstall = ["apache2-utils", "squid3", "iptables-persistent"]
                for packagetoinstall in packagestoinstall:
                    if apt_install(packagetoinstall) is 0 :
                        print "Install Success"
                    else :
                        print "Something failed, try again later or communicate to Debapriya"
                        exit(-9)

                print "Installation of all packages complete, time to configure ....."

                userdict = {'user1':"", 'user2':""}
                squidconfig = "squid.conf.file"

                handlemultipleuseradd(userdict)
                print "Added users"
                configuration_copy_handler(squidconfig)
                print "Copied my config file"
                firewall_configuration(SQUID_CONFIGURATION_PATH)
                print "Configuration Done...."
                print "Sucesssfully Completed!"
                print "Say thanks to Deb"





        elif sys.platform is 'darwin':
            print "Okay, you have a Mac, work in progress!"
    else:
        print "Sorry, Not a Posix Shell"



if __name__=="__main__":
    main()
