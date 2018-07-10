# Copyright 2018, Abraham Cabrera.
import logging
import datetime

from enum import Enum

from bson.objectid import ObjectId
from farmers.manager.database import factory

# This is a hack for exception handling, ideally we would override 
# the connection functions exception and throw our own customer exception instead.
# This would allow us to be Connection Agnostic and not have to import all the 
# different exception types for each Factory Type but since we are short on time
# we will just do this.
from pymongo import errors, ReturnDocument


class BasketState(Enum):
    OPEN = 0,
    CLOSED = 1,
    CANCELED = 2


class BasketDAO():
    """
    """
    def __init__(self):
        module_class_name = self.__module__ + "." + self.__class__.__name__
        self.logger = logging.getLogger(module_class_name)
        self.connection_factory_type = factory.ConnectionFactoryType.MONGODB
    
    def additem(self, _id, code):
        """
        Adds item by code to basket.

        :param _id: basket id. \n
        :type _id: string. \n
        :param code: Code of item from inventory to add to bucket. \n
        :type code: string. \n
        :returns: True if success else False. \n
        :rtype: boolean.
        """
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            updated = None
            with connection_factory.get_connection() as client:
                _filter = {"_id": ObjectId(_id)}
                basket = client.farmers.basket.find_one(_filter)
                if basket:
                    items = basket["items"]
                    items.append(code)
                    update = {"items": items}
                    updated = client.farmers.basket.find_one_and_update(_filter,
                                                                        {"$set": update},
                                                                        return_document=ReturnDocument.AFTER)
            if updated:
                return True
            self.logger.error("Could not update basket")
        except Exception as exception:
            self.logger.error(exception)
        return False

    def cancel(self, _id):
        """
        Cancels a created basket and sets the status to canceled.

        :param _id: basket id to lookup for cancelation. \n
        :type _id: string. \n
        :returns: True if success else False. \n
        :rtype: boolean.
        """
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            with connection_factory.get_connection() as client:
                _filter = {"_id": ObjectId(_id)}
                update = {"state": BasketState.CANCELED.name}
                document = client.farmers.basket.find_one_and_update(_filter,
                                                                     {"$set": update},
                                                                     return_document=ReturnDocument.AFTER)
                if document:
                    return True
        except errors.DuplicateKeyError as duplicate_key_error:
            self.logger.error(duplicate_key_error)
            return False
        self.logger.error("Could not set basket to canceled state!")
        return False
    
    def checkout(self, _id):
        """
        Checkout a created basket, this will set the status to complete.

        :param _id: basket id to lookup for cancelation. \n
        :type _id: string. \n
        :returns: True if success else False. \n
        :rtype: boolean.
        """
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            with connection_factory.get_connection() as client:
                _filter = {"_id": ObjectId(_id)}
                update = {"state": BasketState.CLOSED.name}
                document = client.farmers.basket.find_one_and_update(_filter,
                                                                     {"$set": update},
                                                                     return_document=ReturnDocument.AFTER)
                if document:
                    return True
        except errors.DuplicateKeyError as duplicate_key_error:
            self.logger.error(duplicate_key_error)
            return False
        self.logger.error("Could not set basket to checkout state!")
        return False

    def create(self, codes):
        """
        Creates a basket with a list of item codes, sets the date 
        it was created and sets the status to open.

        :param codes: Item codes from inventory. \n
        :type codes: list. \n
        :returns: True if success else False. \n
        :rtype: boolean.
        """
        basket = None
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            with connection_factory.get_connection() as client:
                document = {"items": codes,
                            "state": BasketState.OPEN.name,
                            "created": datetime.datetime.utcnow()}
                basket = client.farmers.basket.save(document)
                if basket:
                    return basket
                self.logger.error("Error in creating basket!")
        except errors.DuplicateKeyError as duplicate_key_error:
            self.logger.error(duplicate_key_error)
        return None

    def read(self, _id):
        """
        Lookup a basket and return its contents.

        :param _id: basket id to lookup. \n
        :type _id: string. \n
        :returns: Dictionary of basket contents. \n
        :rtype: dict.
        """
        basket = None
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            with connection_factory.get_connection() as client:
                _filter = {"_id": ObjectId(_id)}
                basket = client.farmers.basket.find_one(_filter)
                if basket:
                    return basket
                self.logger.error("Could not find basket with id %s", _id)
        except Exception as exception:
            self.logger.error(exception)
        return None
    
    def removeitem(self, _id, code):
        """
        Removes item by code from basket.

        :param _id: basket id to lookup. \n
        :type _id: string. \n
        :param code: Code of item from inventory to remove from bucket. \n
        :type code: string. \n
        :returns: True if success else False. \n
        :rtype: boolean.
        """
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            updated = None
            with connection_factory.get_connection() as client:
                _filter = {"_id": ObjectId(_id)}
                basket = client.farmers.basket.find_one(_filter)
                if basket:
                    if basket["state"] != BasketState.OPEN.name:
                        self.logger.error("Cannot change the item list of a basket that is not opened.")
                        return False
                    items = basket["items"]
                    if code in items:
                        items.remove(code)
                        update = {"items": items}
                        updated = client.farmers.basket.find_one_and_update(_filter,
                                                                            {"$set": update},
                                                                            return_document=ReturnDocument.AFTER)
                    else:
                        self.logger.error("Code not in items list.")
            if updated:
                return True
            self.logger.error("Could not remove item from basket")
        except Exception as exception:
            self.logger.error(exception)
        return False
