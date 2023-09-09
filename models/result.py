#!/usr/bin/python3
""" holds class Result"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Result(BaseModel, Base):
    """ representation of result"""
    __tablename__ = "results"
    subject_id = Column(String(60), ForeignKey("subjects.id"), nullable=False)
    student_id = Column(String(60), ForeignKey("students.id"), nullable=False)
    class_id = Column(String(60), ForeignKey("classes.id"), nullable=False)
    exam_id = Column(String(4), nullable=False)
    score = Column(String(5), nullable=True)
    grade = Column(String(5), nullable=True)
