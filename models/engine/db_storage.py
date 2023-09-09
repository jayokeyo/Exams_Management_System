#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models import base_model, teacher, student, classes, subject, result, watchlist
from models.teacher import Teacher
from models.parent import Parent
from models.base_model import BaseModel, Base
from models.classes import Class
from models.student import Student
from models.result import Result
from models.subject import Subject
from models.watchlist import Watchlist
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes_available = {"Parent": Parent, "Watchlist": Watchlist, "Result": Result, "Subject": Subject, 
        "Class": Class, "Student": Student, "Teacher": Teacher}


class DBStorage:
    """interaacts with the MySQL database"""
    CNC = {
        'Teacher': teacher.Teacher,
        'Student': student.Student,
        'Class': classes.Class,
        'Subject': subject.Subject,
        'Result': result.Result,
        'Watchlist': watchlist.Watchlist,
        'Parent': Parent
    }
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        #HBNB_MYSQL_USER = getenv('EMS_MYSQL_USER')
        #HBNB_MYSQL_PWD = getenv('EMS_MYSQL_PWD')
        #HBNB_MYSQL_HOST = getenv('EMS_MYSQL_HOST')
        #HBNB_MYSQL_DB = getenv('EMS_MYSQL_DB')
        #HBNB_ENV = getenv('EMS_ENV')
        self.__engine = create_engine('mysql+mysqldb://root@localhost/EMS_dev', pool_pre_ping=True)
        #self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
        #                             format(EMS_MYSQL_USER,
        #                                     EMS_MYSQL_PWD,
        #                                    EMS_MYSQL_HOST,
        #                                    EMS_MYSQL_DB))
        #if HBNB_ENV == "test":
        #   Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.
        If cls is None, queries all types of objects.
        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
        """retrieve one object of class <cls> with id <id>"""
        if cls and id:
            _obj = "{}.{}".format(cls, id)
            _all = self.all(cls)
            return _all.get(_obj)
        return None

    def count(self, cls=None):
        """count of all objects in storage"""
        return (len(self.all(cls)))

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
