import pysftp
from getpass import getpass

def sendFile(ip=None, port=None, username=None, password=None, log='/tmp/pysftp.log', remote_file_location=None, local_file=None):
    if ip == None:
        ip = input('Enter ip address of host: ')
    if port == None:
        port = input('Enter port of host: ')
    if username == None:
        username = input('Enter username of host: ')
    if password == None:
        password = getpass('Enter password of host: ')
    if remote_file_location == None:
        remote_file_location = input('Enter file location to send file: ')
    if local_file == None:
        local_file = input('Enter filename of file to send: ')

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None #Note that this is now open to man in the middle attacks, this is fine in this instance as the data being sent should already be encrypted and I want to make the hand off to the next secretary as easy as possible. Thus this avoids making people copy in the identity of their backup (in my case, my phone)

    with pysftp.Connection(host=ip, port=int(port), username=username, password=password, log=log, cnopts=cnopts) as srv:
        with srv.cd(remote_file_location):
            srv.put(local_file)
