#!/usr/bin/python3
""" holds class Graph"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String


class Graph(BaseModel, Base):
    """Representation of a graph """
    __tablename__ = 'graphs'
    x_axis = Column(String(128), nullable=False)
    y_axis = Column(String(128), nullable=True)
    where_clause = Column(String(128), nullable=False)
    groupby_clause = Column(String(128), nullable=True)
    graph_type = Column(String(128), nullable=False)
    description = Column(String(1000), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes teacher"""
        super().__init__(*args, **kwargs)
