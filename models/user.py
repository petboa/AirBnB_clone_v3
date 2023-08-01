#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete-orphan")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def to_dict(self, save_pass=False):
        """returns a dictionary representation of the instance"""
        result_dict = {}
        for key, value in self.__dict__.items():
            if key == "_sa_instance_state":
                continue
            if key == "created_at" or key == "updated_at":
                if value is not None:
                    result_dict[key] = value.isoformat()
                else:
                    result_dict[key] = None
            elif key == "_password" and not save_pass:
                continue
            else:
                result_dict[key] = value
        result_dict["__class__"] = self.__class__.__name__
        return result_dict


    @property
    def password(self):
        """get password"""
        return self._password

    @password.setter
    def password(self, passwd):
        """hash password"""
        self._password = hashlib.md5(passwd.encode()).hexdigest()

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
