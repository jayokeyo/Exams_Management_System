#!/usr/bin/python3
""" holds class Parent"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Parent(BaseModel, Base):
    """Representation of a parent """
    __tablename__ = 'parents'
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    contact = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes teacher"""
        super().__init__(*args, **kwargs)
