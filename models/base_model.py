#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from models import storage_type

time_format = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, val in kwargs.items():
                if key == '__class__':
                    continue
                
                setattr(self, key, val)

                if key != '__class__':
                    setattr(self, key, val)

                if key in ["created_at", "updated_at"]:
                    setattr(self, key, datetime.fromisoformat(kwargs[key]))
            
                del kwargs['__class__']
                self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """ Updates updated_at with current time when instance is changed """
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """ Convert instance into dict format """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        
        dict_copy = dictionary.copy()

        if "_sa_instance_state" in dict_copy.keys():
            del dict_copy["_sa_instance_state"]

        return dict_copy

    def delete(self):
        """ deletes the current instance from the storage """
        from models import storage
        storage.delete(self)
