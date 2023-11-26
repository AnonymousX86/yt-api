# -*- coding: utf-8 -*-
from sqlalchemy import Column, inspect, Integer, String
from sqlalchemy.orm import Session

from core import Base, create_session


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    spotify_id = Column(String(22), nullable=False)
    youtube_id = Column(String(34), nullable=False)

    @classmethod
    def add_playlist(cls, *, spotify_id: str, youtube_id: str) -> 'Playlist':
        with create_session() as session:
            new_playlist = cls(spotify_id=spotify_id, youtube_id=youtube_id)
            session.add(new_playlist)
            session.commit()
            return new_playlist

    @classmethod
    def remove_playlist(cls, *, spotify_id: str = None, youtube_id: str = None) -> None:
        if not spotify_id and not youtube_id:
            return
        with create_session() as session:
            if spotify_id:
                playlist_to_remove = session.query(cls).filter_by(spotify_id=spotify_id).first()
            elif youtube_id:
                playlist_to_remove = session.query(cls).filter_by(youtube_id=youtube_id).first()
            session.delete(playlist_to_remove)
            session.commit()

    @classmethod
    def get_playlist(cls, *, spotify_id: str = None, youtube_id: str = None) -> 'Playlist':
        if not spotify_id and not youtube_id:
            return None
        with create_session() as session:
            if spotify_id:
                playlist = session.query(cls).filter_by(spotify_id=spotify_id).first()
            elif youtube_id:
                playlist = session.query(cls).filter_by(youtube_id=youtube_id).first()
            return playlist


def test_playlist(session: Session) -> bool:
    inspector = inspect(session.bind)
    return 'playlists' in inspector.get_table_names()


if __name__ == '__main__':
    from logging import basicConfig, getLogger, INFO
    from rich.logging import RichHandler

    basicConfig(
        level=INFO,
        format='%(message)s',
        datefmt='[%X]',
        handlers=[RichHandler(markup=True, rich_tracebacks=True)]
    )
    log = getLogger('sqlalchemy.engine')
    log.setLevel(INFO)

    session = create_session()
    if (valid := test_playlist(session)):
        log.info('The `playlists` table exists and is correctly structured.')
    else:
        log.error('The `playlists` table does not exist or is not correctly structured.')
