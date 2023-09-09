#!/usr/bin/python3
""" holds class Student"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship


student_subject = Table(
        'student_subject', Base.metadata, Column('student_id', String(60), 
            ForeignKey('students.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True), 
        Column('subject_id', String(60), 
            ForeignKey('subjects.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True))

class Student(BaseModel, Base):
    """Representation of a student"""
    
    __tablename__ = "students"
    class_id = Column(String(600), ForeignKey("classes.id"), nullable=False)
    parent_id = Column(String(600), ForeignKey("parents.id"), nullable=False)
    first_name = Column(String(128), nullable=True)
    surname = Column(String(128), nullable=True)
    subjects = relationship("Subject", secondary="student_subject", backref="student_subjects", viewonly=False)

    def __init__(self, *args, **kwargs):
        """initializes student"""
        super().__init__(*args, **kwargs)
