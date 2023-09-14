#!/usr/bin/python3
""" holds class Graph"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Graph(BaseModel, Base):
    """Representation of a graph """
    __tablename__ = 'graphs'
    dashboard_id = Column(String(60), ForeignKey("dashboards.id"))
    x_axis = Column(String(128), nullable=False)
    y_axis = Column(String(128), nullable=True)
    where_clause = Column(String(128), nullable=False)
    group_by = Column(String(128), nullable=True)
    graph_type = Column(String(128), nullable=False)
    description = Column(String(1000), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes teacher"""
        super().__init__(*args, **kwargs)
