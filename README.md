Simple program to keep track of attendance of people in meetings and flags anyone who misses 3 meeings in a row for further action and can be easily modified to automatically act upon these flagged people.

First time use: start python3 in the working directory, and run the following commands:
```
import registration
data = []
registration.ChangeRegister(data)
```
and use break instead of the first name to stop adding people.

All further uses should be run as `python3 registration.py`

If you wish to utilise the Google Drive capabilities of this program, you must generate your 'credentials.json' from the Google Developers website and put in the working directory. Then the next time you run the registration, you will be redirected to the oauth2 page where you must log in to the Google account that you got the credentials for earlier. Once this is done, the program will generate a 'token.pickle' file which will allow you to skip the authorisation in the future.


To use the object tracker, run `python3 rocketFinder.py`. Then input the password to the given gmail account. Once the program is running, you can send emails to the email address specified and the script will send a response. Commands are as follows (words in {} are to be replaced with whatever you want the program to do):

Add:{object}:{location}             ->      Adds an object under your name to the given location, returns an error if the object already exists
Remove:{object}                     ->      Removes an object, returns an error if you do not own the object or if the object does not exist in the system
Move:{object}:{location}            ->      Moves an object to a new location and puts it under your name, returns an error if the object does not exist in the system
List:{optional: 'all'}              ->      Lists all objects in the system, if given the 'all' instruction, will also return locations and owners for those objects
Search:{query}:{optional: 'all'}    ->      Searchs database using a regular expression, 'all' has the same usage as for list, returns an error if the query cannot be compiled
Find:{object}                       ->      Finds object and returns the information about it, does not use regular expressions
Help                                ->      Send this file, README.md

Example usage:

Add:Carbon Fiber Rocket Body x4:lmh
List
Search:[pkj]:all
Move:homemade parachute:Engineering Storage
Remove:Balloon
Search:rocket

It treats each email as an owner, so make sure to be consistent with which email you send requests with.
