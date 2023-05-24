#!/usr/bin/python3
"""module for DBStorage engine"""
from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.user import User


class DBStorage:
    """ A new engine for the database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """
        initializes the new database storage engine
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}"
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query and returns a dictionary of database __object"""
        dict_cls = {}
        if cls:
            cls_query = self.__session.query(cls).all()
            for obj in cls_query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                dict_cls[key] = obj
        else:
            classes = {"State": state, "City": city, "Amenity": amenity,
                       "User": user, "Place": place, "Review": review}
            for key, val in classes:
                for obj in self.__session.query(val):
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    dict_class[key] = obj

        return dict_cls

    def new(self, obj):
        """attribute that adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """ commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete obj from the current database session if not None"""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """Database and value creation and configuration"""
        # create session from current engine
        Base.metadata.create_all(self.__engine)

        # create database table
        ses_scope = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(ses_scope)
        self.__session = Session()

    def close(self):
        """closes session"""
        self.__session.close()
