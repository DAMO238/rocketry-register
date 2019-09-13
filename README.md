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
