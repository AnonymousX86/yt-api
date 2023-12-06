# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from .core import Base, create_session


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, nullable=False)
    spotify_id = Column(String(22), nullable=False)
    youtube_id = Column(String(11), nullable=False)

    @classmethod
    def add_track(cls, *, spotify_id: str, youtube_id: str) -> 'Track':
        with create_session() as session:
            new_track = cls(spotify_id=spotify_id, youtube_id=youtube_id)
            session.add(new_track)
            session.commit()
            return new_track

    @classmethod
    def remove_track(cls, *, spotify_id: str = None, youtube_id: str = None) -> None:
        if not spotify_id and not youtube_id:
            return
        with create_session() as session:
            if spotify_id:
                track_to_remove = session.query(cls).filter_by(spotify_id=spotify_id).first()
            elif youtube_id:
                track_to_remove = session.query(cls).filter_by(youtube_id=youtube_id).first()
            session.delete(track_to_remove)
            session.commit()

    @classmethod
    def get_track(cls, *,  spotify_id: str = None, youtube_id: str = None) -> 'Track':
        if not spotify_id and not youtube_id:
            return None
        with create_session() as session:
            if spotify_id:
                track = session.query(cls).filter_by(spotify_id=spotify_id).first()
            elif youtube_id:
                track = session.query(cls).filter_by(youtube_id=youtube_id).first()
            return track

    def remove(self) -> None:
        self.remove_track(spotify_id=self.spotify_id)
