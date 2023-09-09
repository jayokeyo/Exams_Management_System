#!/usr/bin/python3
""" holds class Watchlist"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Watchlist(BaseModel, Base):
    """Representation of a watchlist"""
    __tablename__ = 'watchlist'
    student_id = Column(String(60), ForeignKey("students.id"), nullable=False)
    teacher_id = Column(String(60), ForeignKey("teachers.id"), nullable=False)
    reason = Column(String(1000), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes watchlist"""
        super().__init__(*args, **kwargs)
