#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from models import storage_type
from models.city import City
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if storage_type == 'db':
        name = Column(String(60), nullable=False)
        cities = relationship("City", backref="state",
                               cascade="all, delete, delete-orphan")
    else:
    name = ""

    @property
    def cities(self):
        """ Get list of cities """
        related_cities = []
        all_cities = models.storage.all("City").values()
        for city in all_cities:
            if city.state_id == self.id:
                related_cities.append(city)
        return related_cites
