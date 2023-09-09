from models.base_model import BaseModel
from models.subject import Subject
from models.classes import Class
from models.teacher import Teacher
from models.result import Result
from models.student import Student
from models.watchlist import Watchlist
from models.engine import db_storage


CNC = db_storage.DBStorage.CNC
storage = db_storage.DBStorage()
storage.reload()
