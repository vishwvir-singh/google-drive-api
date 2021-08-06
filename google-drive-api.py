import os
from googleapiclient import discovery, errors,http
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Directories
PROJECT_DIR = os.getcwd()
GDRIVE_ROOT_DIR = os.path.join(PROJECT_DIR, 'google_drive')
CRED_DIR = os.path.join(GDRIVE_ROOT_DIR, 'credentials')
DATA_DIR = os.path.join(GDRIVE_ROOT_DIR, 'drive_files')
CLIENT_SECRET_FILE = 'client_secret.json'

APPLICATION_NAME = 'Python- Drive API'


def get_credentials():
    creds = None
    credential_path = os.path.join(CRED_DIR, 'credentials.json')
    clientsecret_path = os.path.join(CRED_DIR, 'client_secret.json')
    if os.path.exists(credential_path):
        creds = Credentials.from_authorized_user_file(credential_path, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(clientsecret_fp, SCOPES)
        creds = flow.run_console()
        with open(credential_path, 'w') as credentials_f: credentials_f.write(creds.to_json())
    return creds

def create_service():
    """Creates Google Drive API oauth service using credential files
       :return: service object
    """
    credentials = get_credentials()
    # http = credentials.authorize(httplib2.Http())
    drive = discovery.build('drive', 'v3', credentials=credentials)
    return drive

def top_n_accessible_drive_files(top_n = 10):
    try:
        service = create_service()
        results = service.files().list(
            pageSize=top_n,
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items: print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
    except errors.HttpError as error:
        print (f'An error occurred: {error}')
        return []
    return items

def print_drive_file_metadata(file_id):
    """Print a file's metadata.

    Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
    """
    try:
        service = create_service()
        file = service.files().get(fileId=file_id).execute()
        print (f'Name: {file["name"]}')
        print (f'MIME type: {file["mimeType"]}')
    except errors.HttpError as error:
        print (f'An error occurred: {error}')
        return {}
    return file


def print_drive_file_content(file_id):
    """Print a file's content.

    Args:
    service: Drive API service instance.
    file_id: ID of the file.

    Returns:
    File's content if successful, None otherwise.
    """
    try:
        service = create_service()
        print (service.files().get_media(fileId=file_id).execute())
    except errors.HttpError as error:
        print (f'An error occurred: {error}')


def download_drive_file(file_id, local_dir=DATA_DIR):
    """Download a Drive file's content to the local filesystem.
    Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    fh: io.Base or file object, the stream that the Drive file's
        contents will be written to.
    """
    service = create_service()
    file_metadata = print_drive_file_metadata(service, file_id)
    if file_metadata:
        request = service.files().get_media(fileId=file_id)
        if not os.path.exists(local_dir): os.makedirs(local_dir)
        fh = http.io.BytesIO()
        downloader = http.MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download : {int(status.progress() * 100)}")
        with open(f'{local_dir}/{file_metadata["name"]}', "wb") as f:
            f.write(fh.getvalue())
        return f'{local_dir}/{file_metadata["name"]}'
    return ''
