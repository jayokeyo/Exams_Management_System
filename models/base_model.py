#!/usr/bin/python3
"""BaseModel Class of Models Module"""
import os
import json
import models
from uuid import uuid4, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime


Base = declarative_base()

class BaseModel:
    """attributes and functions for BaseModel class"""
    id = Column(String(60), nullable=False, primary_key=True)
    def __init__(self, *args, **kwargs):
        """instantiation of new BaseModel Class"""
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid4())

    def __set_attributes(self, attr_dict):
        """private: converts attr_dict values to python class attributes"""
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid4())
        for attr, val in attr_dict.items():
            setattr(self, attr, val)

    def __is_serializable(self, obj_v):
        """private: checks if object is serializable"""
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def bm_update(self, attr_dict=None):
        """updates the basemodel and sets the correct attributes"""
        IGNORE = ['id', 'student_id', 'teacher_id', 'parent_id', 'subject_id', 'class_id']
        if attr_dict:
            updated_dict = {
                k: v for k, v in attr_dict.items() if k not in IGNORE
            }
            for key, value in updated_dict.items():
                setattr(self, key, value)
            self.save()

    def save(self):
        """updates attribute updated_at to current time"""
        models.storage.new(self)
        models.storage.save()

    def to_json(self, saving_file_storage=False):
        """returns json representation of self"""
        obj_class = self.__class__.__name__
        bm_dict = {
            k: v if self.__is_serializable(v) else str(v)
            for k, v in self.__dict__.items()
        }
        bm_dict.pop('_sa_instance_state', None)
        bm_dict.update({
            '__class__': obj_class
            })
        if not saving_file_storage and obj_class == 'User':
            bm_dict.pop('password', None)
        return(bm_dict)

    def __str__(self):
        """returns string type representation of object instance"""
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """deletes current instance from storage"""
        models.storage.delete(self)
