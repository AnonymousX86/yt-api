# -*- coding: utf-8 -*-
from os import getenv
from pathlib import Path
from pickle import load as pickle_loads, dump as pickle_dump

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow


CREDENTIALS_FILE = 'spoyt_credentials.pickle'
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
DEVELOPER_KEY = getenv('DEVELOPER_KEY')


def get_authenticated_service() -> Resource:
    """Authorize the request and store authorization credentials."""
    credentials: Credentials = None

    # Try to load credentials from file
    if (path := Path(CREDENTIALS_FILE)).exists():
        with open(path, 'rb') as f:
           credentials = pickle_loads(f)

    if not credentials or not credentials.valid:
        # Try to refresh credentials
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        # Obtain new credentials
        else:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                SCOPES
            )
            credentials: Credentials = flow.run_local_server()

    # Save credentials to keyring
    if not path.exists():
        with open(path, 'x'):
            pass
    with open(path, 'wb') as f:
       pickle_dump(credentials, f)

    return build(
        API_SERVICE_NAME,
        API_VERSION,
        credentials=credentials,
        developerKey=DEVELOPER_KEY
    )
