from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.discovery import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

#TODO: Allow for deleting files to avoiding filling drive up with crap

def authorize():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def delete_files(filename, mimeType):
    service = authorize()
    page_token = None
    while True:
        response = service.files().list(q="mimeType='{mimeType}' and name='{filename}'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id)',
                                              pageToken=page_token).execute()
        for item in response.get('files', []):
            try:
                print(item['id'])
                service.files().delete(item['id']).execute()
            except:
                print(f'failed to delete file with id: {id}')
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    

def get_last_10_files():
    service = authorize()
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def upload_file(filename, mimeType):
    service = authorize()
    file_metadata = { 'name' : filename }
    media = MediaFileUpload( filename, mimetype=mimeType )
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def get_id(filename, mimeType):
    service = authorize()
    page_token = None
    response = service.files().list(q=f"mimeType='{mimeType}' and name='{filename}'", spaces='drive', fields='nextPageToken, files(id)', pageToken=page_token).execute()
    return response.get('files', [])[0].get('id')

def download_file(file_id, filename):
    service = authorize()
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print ("Download %d%%" % int(status.progress() * 100))
    with open(filename, 'wb') as f:
        f.write(fh.getbuffer())


if __name__ == '__main__':
    main()
