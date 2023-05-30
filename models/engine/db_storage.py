#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the current database session"""
        new_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls, None)
            if cls:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    new_dict[key] = obj
        else:
            for cls in classes.values():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    new_dict[key] = obj
        return new_dict

    def get(self, cls, id):
        """Retrieve an object from the current database session"""
        if cls and id:
            obj = self.__session.query(cls).get(id)
            return obj
        else:
            return None

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session"""
        self.__session.close()

    def count(self, cls=None):
        """Count the number of objects in a class"""
        count = 0
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls, None)
            if cls:
                count = self.__session.query(cls).count()
        else:
            for cls in classes.values():
                count += self.__session.query(cls).count()
        return count

