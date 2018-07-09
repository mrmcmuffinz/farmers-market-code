# Copyright 2018 Abraham cabrera.
import os

from abc import ABC, abstractmethod
from enum import Enum

class ConnectionFactoryType(Enum):
    UNSUPPORTED = 0
    MONGODB = 1

class ConnectionFactory(ABC):
    @abstractmethod
    def get_connection(self):
        pass
    
def get_mongodb_properties():
    port = int(os.getenv("MONGODB_PORT")) if os.getenv("MONGODB_PORT") else None
    properties = {
        "db": os.getenv("MONGODB_DATABASE"),
        "host": os.getenv("MONGODB_HOST"),
        "port": port,
        "user": os.getenv("MONGODB_USERNAME"),
        "password": os.getenv("MONGODB_PASSWORD")
    }
    return properties

def connection_factory(connection_type):
    if not isinstance(connection_type, ConnectionFactoryType):
        raise TypeError("connection_type is not type of ConnectionFactoryType")
    if connection_type is ConnectionFactoryType.MONGODB:
        from pymongo import MongoClient
        class MongoDBConnectionFactory(ConnectionFactory):
            def __init__(self, properties):
                self.user = properties.get("user")
                self.password = properties.get("password")
                self.host = properties.get("host")
                self.port = properties.get("port")
                self.db = properties.get("db")
                self.conn = None

            def get_connection(self):
                return MongoClient(host=self.host, 
                                   port=self.port,
                                   username=self.user,
                                   password=self.password)

        connection_properties = get_mongodb_properties()
        return MongoDBConnectionFactory(connection_properties)
    raise NotImplementedError("Connection type not implemented!")