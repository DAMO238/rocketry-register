import comms
from getpass import getpass
import json
import driveutils
import re

#TODO: Delete copies of database on drive

class Finder():
    _data = None
    _last_id = None
    def _write_data(self):
        with open('rocket_database', 'w') as f:
            json.dump(self._data, f)

    def _read_data(self):
        with open('rocket_database', 'r') as f:
            self._data = json.load(f)

    def _upload_data(self):
        driveutils.delete_files('rocket_database', 'text/plain')
        driveutils.upload_file('rocket_database', 'text/plain')

    def _change_object_location(self, obj, new_owner, new_location):
        if obj in self._data:
            self._data[obj] = (new_owner, new_location)
            return True #successful
        else:
            return False #data was not found

    def _remove_object(self, obj, owner):
        if obj in self._data:
            if self._data[obj][0] != owner:
                return False
            del self._data[obj]
            return True
        else:
            return False

    def _add_object(self, obj, owner, location):
        if obj in self._data:
            return False
        else:
            self._data[obj] = (owner, location)
            return True

    def _get_object(self, obj):
        if obj in self._data:
            return f'{obj} can be found at {self._data[obj][1]} and is in the hands of {self._data[obj][0]}.'
        else:
            return f'{obj} could not be found'

    def _list_objects(self, full_info = False):
        msg = 'Objects are:\n\n'
        for obj, info in self._data.items():
            if full_info:
                msg += f'{obj}, owned by {info[0]} at {info[1]}\n'
            else:
                msg += f'{obj}\n'
        return msg

    def _search_objects(self, obj, full_info = False):
        try:
            regex = re.compile(obj)
        except:
            return 'Regular expression failed to compile!'
        msg = 'Search Results: \n\n'
        for obj, info in self._data:
            if len(regex.findall(obj)) != 0:
                if full_info:
                    msg += f'{obj}, owned by {info[0]} at {info[1]}\n'
                else:
                    msg += f'{obj}\n'
        return msg

    def _parse_instruction(self, owner, instruction):
        instruction = instruction.split(':')

        if instruction[0].lower() == 'add' and len(instruction) == 3:
            if self._add_object(instruction[1], owner, instruction[2]):
                comms.send_email(owner, 'Added Object', f'Added {instruction[1]} to {instruction[2]} using your id: {owner}!\n\nThank you for your report')
            else:
                comms.send_email(owner, 'Failed to Add Object', f'Failed to add {instruction[1]} to {instuction[2]}. This may be because {instruction[1]} is already in the database.')

        if instruction[0].lower() == 'remove' and len(instruction) == 2:
            if self._remove_object(instruction[1], owner):
                comms.send_email(owner, 'Removed Object', f'Removed {instruction[1]} from database.\n\nThank you for your report.')
            else:
                comms.send_email(owner, 'Failed to Remove Object', f'Failed to remove object. This could be because you are not the owner of the object and must claim it first by moving it, or it may because the object does not exist')

        if instruction[0].lower() == 'move' and len(instruction) == 3:
            if self._change_object_location(instruction[1], owner, instruction[2]):
                comms.send_email(owner, 'Moved Object', f'Moved {instruction[1]} to {instruction[2]} and assigned to your id: {owner}!\n\nThank you for your report')
            else:
                comms.send_email(owner, 'Failed to Move Object', f'Failed to move {instruction[1]} to {instruction[2]}. This may be because the object does not exist.')

        if instruction[0].lower() == 'list' and len(instruction) <= 2:
            full_info = False
            try:
                if instruction[1].lower() == 'all':
                    full_info = True
            except:
                pass
            comms.send_email(owner, 'List of Objects', self._list_objects(full_info))

        if instruction[0].lower() == 'search' and len(instruction) == 2:
            comms.send_email(owner, 'Search Results', self._search_objects(instruction[1]))

        if instruction[0].lower() == 'search' and len(instruction) == 3:
            if instruction[2].lower == 'all':
                comms.send_email(owner, 'Search Results', self._search_objects(instruction[1], True))
            else:
                comms.send_email(owner, 'Search Results', self._search_objects(instruction[1]))

        if instruction[0].lower() == 'help':
            comms.send_email(owner, 'Help Sheet', 'Please see the attached sheet on how to use this program', 'README.md')
        
        if instruction[0].lower() == 'find' and len(instruction) == 2:
            comms.send_email(owner, 'Search Report', self._get_object(instruction[1]))
 

    def _main_loop(self):
        mail = comms.get_emails()
        if self._last_id == None:
            self._last_id = mail[-1]['Message-ID']
            return
        if self._last_id != mail[-1]['Message-ID']:
            print(f"Received email from {mail[-1]['From']} with subject {mail[-1]['Subject']}")
            self._last_id = mail[-1]['Message-ID']
            self._parse_instruction(mail[-1]['From'], mail[-1]['Subject'])
            self._write_data()
            try:
                self._upload_data()
            except:
                print('Could not upload data')
        

    def __init__(self):
        print('Initialising, Please Wait...')
        self._read_data()
        print('Initialisation Complete')
        while True:
            self._main_loop()

if __name__ == '__main__':
    finder = Finder()
