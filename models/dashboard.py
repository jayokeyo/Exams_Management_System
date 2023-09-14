#!/usr/bin/python3
""" holds class Dashboard"""
import models
from models.base_model import BaseModel, Base
from models.graph import Graph
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Dashboard(BaseModel, Base):
    """Representation of a dashboard """
    __tablename__ = 'dashboards'
    name = Column(String(128), nullable=False)
    description = Column(String(1000), nullable=True)
    graphs = relationship("Graph", backref="dashboards", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes teacher"""
        super().__init__(*args, **kwargs)
