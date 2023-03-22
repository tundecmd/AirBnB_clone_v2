#!/usr/bin/python3
""" DB Storage engine """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv


class DBStorage:
    """ DB Storage engine for mysql storage """
    __engine = None
    __session = None

    def __init__(self):
        """ Instantiate a new db storage instance """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                        HBNB_MYSQL_USER,
                        HBNB_MYSQL_PWD,
                        HBNB_MYSQL_HOST,
                        HBNB_MYSQL_DB
                    ), pool_pre_ping=True
                )

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session (self.__session)
        all objects depending of the class name
        """
        dict = {}
        if cls is None:
            for c in classes.values():
                objs = self.session.query(c).all()
                for obj in objs:
                    key = obj.__class__.name + '.' + obj.id
                    dict[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.name + '.' + obj.id
                dict[key] = obj
        return dict

    def new(self, obj):
        """ add the object to the current database session """
        if obj is None:
            return
        try:
            self.__session.add(obj)
            self.__session.flush()
            self.__session.refresh(obj)
        except Exception as e:
            self.__session.rollback()
            raise e

    def save(self):
        """ add the object to the current database session """
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj is None:
            return
        if obj is not None:
            try:
                self.session.delete(obj)
                self.session.commit()
            except Exception as e:
                # Handle any exceptions that occur during the deletion process
                self.__session.rollback()
                raise e

    def reload(self):
        """ reloads the db """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()
