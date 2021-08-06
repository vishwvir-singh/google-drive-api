# google-drive-api
Upload, download, share, and manage files stored in Google Drive.

# Authorization protocol
The authorization protocol that this API requires to authenticate your app users is OAuth 2.0.

# You can use Google Drive API to:

1. Download files from Google Drive and Upload files to Google Drive.
2. Search for files and folders stored in Google Drive. Create complex search queries that return any of the file metadata fields in the Files resource.

# Prerequisites:

**To install the Google client library for Python, run the following command:**

    1. pip install --upgrade google-api-python-client 
    2. pip install --upgrade google-auth-httplib2 
    3. pip install --upgrade google-auth-oauthlib


**Enable Drive API for your project:** (Any application that calls Google APIs needs to enable those APIs in the API Console.)

    1. Open the API Library in the Google API Console.
    2. If prompted, select a project, or create a new one.
    5. Select the Drive API, then click the Enable button.
    6. If prompted, read and accept the API's Terms of Service.

**Create authorization credentials:** (Any application that uses OAuth 2.0 to access Google APIs must have authorization credentials that identify the application to Google's OAuth 2.0 server. The following steps explain how to create credentials for your project. Your applications can then use the credentials to access APIs that you have enabled for that project.)

    1. Go to the Credentials page.
    2. Click Create credentials > OAuth client ID.
    3. Select the TVs and Limited Input devices application type.
    4. Name your OAuth 2.0 client and click Create.
