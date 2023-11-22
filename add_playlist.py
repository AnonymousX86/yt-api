"""
This code sample creates a private playlist in the authorizing user's
YouTube channel.
Usage:
  python playlist_updates.py --title=<TITLE> --description=<DESCRIPTION>
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path
from pickle import load as pickle_loads, dump as pickle_dump

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


CREDENTIALS_FILE = 'spoyt_credentials.pickle'

CLIENT_SECRETS_FILE = 'spoyt_o2.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
DEVELOPER_KEY = '632456508771-criin7m1g53l3e3s90pv6o6sgo9gdphj.apps.googleusercontent.com'


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
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
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


def add_playlist(youtube: Resource, args: Namespace) -> str:
    """Creates playlist then returns it's ID."""
    body = dict(
        snippet=dict(
            title=args.title,
            description=args.description
        ),
        status=dict(
            privacyStatus='private'
        )
    )

    playlists_insert_response: dict = youtube.playlists().insert(
        part='snippet,status',
        body=body
    ).execute()

    return playlists_insert_response.get('id')


if __name__ == '__main__':
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument(
        '--title',
        default='Test Playlist',
        help='The title of the new playlist.'
    )
    parser.add_argument(
        '--description',
        default='A private playlist created with the YouTube Data API.',
        help='The description of the new playlist.'
    )
    args = parser.parse_args()

    # Connect to YouTube
    youtube = get_authenticated_service()

    # Create playlist
    try:
        new_playlist = add_playlist(youtube, args)
        print(f'New playlist ID: {new_playlist}')
    except HttpError as e:
        print('An HTTP error {0.resp.status} occurred: {0.content}'.format(e))
