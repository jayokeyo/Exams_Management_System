#!/usr/bin/python3
""" holds class Class"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Class(BaseModel, Base):
    """Representation of a parent """
    __tablename__ = 'classes'
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes teacher"""
        super().__init__(*args, **kwargs)
