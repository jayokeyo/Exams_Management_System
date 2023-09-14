#!/usr/bin/python3
""" holds class Student"""
import models
from models.base_model import BaseModel, Base
from models.dashboard import Dashboard
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship


teacher_subject = Table(
        'teacher_subject', Base.metadata, Column('teacher_id', String(60),
            ForeignKey('teachers.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
        Column('subject_id', String(60),
            ForeignKey('subjects.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True))
teacher_class = Table(
        'teacher_class', Base.metadata, Column('teacher_id', String(60),
            ForeignKey('teachers.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
        Column('class_id', String(60),
            ForeignKey('classes.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True))

class Teacher(BaseModel, Base):
    """Representation of a teacher"""

    __tablename__ = "teachers"
    first_name = Column(String(128), nullable=True)
    surname = Column(String(128), nullable=True)
    email = Column(String(300), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    subjects = relationship("Subject", secondary="teacher_subject", backref="teacher_subjects", viewonly=False)
    classes = relationship("Class", secondary="teacher_class", backref="teacher_classes", viewonly=False)
    dashboards = relationship("Dashboard", backref="teachers", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes Teacher"""
        super().__init__(*args, **kwargs)
