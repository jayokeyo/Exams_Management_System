#!/usr/bin/python
""" holds class Subject"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Subject(BaseModel, Base):
    """Representation of Subject"""
    __tablename__ = 'subjects'
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Subject"""
        super().__init__(*args, **kwargs)
