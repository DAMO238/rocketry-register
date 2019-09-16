from getpass import getpass
import re
from fbchat import Client
from fbchat.models import *
import base64
import os
from cryptography.hazmat.backends import default_backend 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import json
import driveutils
import transferutils

NUMBER_OF_WEEKS_TO_FLAG = 3 #consts
SECRETARY_EMAIL = 'damien31@rocketmail.com' #for facebook
SECRETARY_PASSWORD = getpass('Input password for facebook: ')
ROCKETRY_THREAD = '2768832806521279'
KEY_PASSWORD = getpass('Input encryption key password: ')
SALT = b'\xbd\xcc\x8b>\x85\xe1\xb8\xef\x9d\xd38(A\xad\xfc\x97'

#TODO: Delete extra copies of register on drive to avoid filling it up with crap

def GetMembers():
    client = Client(SECRETARY_EMAIL, SECRETARY_PASSWORD)
    user_id_list = list(client.fetchThreadInfo(ROCKETRY_THREAD)[ROCKETRY_THREAD].participants)
    user_list = []
    for user_id in user_id_list:
        user_list.append(client.fetchUserInfo(user_id)[user_id])
    client.logout()
    return user_list

def CheckRegister(data, human_readable=True):
    members = GetMembers()
    regex = re.compile('[\.@]')
    for week in data:
        for email in week:
            first, last, *_ = regex.split(email)
            for member in members:
                if member.name.lower() == first.lower() + ' ' + last.lower():
                    members.remove(member)
    bad_members = []
    if human_readable:
        for member in members:
            bad_members.append(member.name)
    else:
        bad_members = members
    return bad_members

def ChangeRegister(data):
    if len(data) >= NUMBER_OF_WEEKS_TO_FLAG:
        del data[0]
    new_week = []
    print('ALL DATA MUST BE ENTERED AS SEEN IN FACEBOOK')#note that emails may not be accurate if different name is used for email and facebook, but emails will be internally consistent
    while True:
        first = input('Enter first name: ').lower()
        if first == 'break' or first == 'stop':
            break
        last = input('Enter last name: ').lower()
        college = input('Enter college code: ').lower()
        email = f'{first}.{last}@{college}.ox.ac.uk'
        new_week.append(email)
    data.append(new_week)

def WriteRegister(data):
    enc = json.JSONEncoder()
    store_data = enc.encode(data)
    store_data = store_data.encode('utf-8')
    fernet = Fernet(KEY)
    encrypted_data = fernet.encrypt(store_data)
    with open('register', 'wb') as f:
        f.write(encrypted_data)

def ReadRegister():
    dec = json.JSONDecoder()
    with open('register', 'rb') as f:
        encrypted_data = f.read()
    fernet = Fernet(KEY)
    store_data = fernet.decrypt(encrypted_data)
    store_data = store_data.decode('utf-8')
    data = dec.decode(store_data)
    return data

def GetKey(password_text):
    password = password_text.encode()
    kdf = PBKDF2HMAC( algorithm=hashes.SHA256(), length=32, salt=SALT, iterations=100000, backend=default_backend() )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

KEY = GetKey(KEY_PASSWORD)

def UploadRegister():
    driveutils.delete_files('register', 'text/plain')
    driveutils.upload_file('register', 'text/plain')
def DownloadRegister():
    driveutils.download_file(driveutils.get_id('register', 'text/plain'), 'register')

def RemoveMembers(fbids):
    client = Client(SECRETARY_EMAIL, SECRETARY_PASSWORD)
    for fbid in fbids:
        client.removeUserFromGroup(fbid, ROCKETRY_THREAD)

def RemoveAllMembers(users):
    ids = []
    for user in users:
        ids.append(user.uid)
    RemoveMembers(ids)

def RemoveSomeMembers(users):
    ids = []
    for user in users:
        prompt = None
        while prompt != 'Y' and prompt != 'N':
            prompt = input(f'Should I eject {user.name} into space?(Y/N)')
            if prompt == 'Y':
                ids.append(user.uid)
    RemoveMembers(ids)
   
def UpdateRemote():
    transferutils.sendFile(port=2222, username=damo, remote_file_location='python scripts', local_file='register')

 

if __name__ == '__main__':
    prompt = None
    while prompt != 'Y' and prompt != 'N':
        prompt = input('Download Register from Drive?(Y/N)')
        if prompt == 'Y':
            DownloadRegister()

    reg = ReadRegister()
    ChangeRegister(reg)
    members = CheckRegister(reg, False)

    if len(members) != 0:
        print('The following members have missed more than 3 consecutive meetings:')
        for member in members:
            print(member.name)
        prompt = None
        while prompt != 'none' and prompt != 'some' and prompt != 'all':
            prompt = input('How many members do you want to eject into space? (all/some/none)')
            if prompt == 'all':
                RemoveAllMembers()
            if prompt == 'some':
                RemoveSomeMembers()
    else:
        print('No members have missed 3 consecutive meetings')

    prompt = None
    while prompt != 'Y' and prompt != 'N':
        prompt = input('Write to Disk?(Y/N)')
        if prompt == 'Y':
            WriteRegister()

    prompt = None
    while prompt != 'Y' and prompt != 'N':
        prompt = input('Upload Register to Drive?(Y/N)')
        if prompt == 'Y':
            UploadRegister()

    prompt = None
    while prompt != 'Y' and prompt != 'N':
        prompt = input('Send Register to Backup?(Y/N)')
        if prompt == 'Y':
            UpdateRemote()
