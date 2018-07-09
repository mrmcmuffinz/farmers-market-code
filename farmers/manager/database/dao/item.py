# Copyright 2018, Abraham Cabrera.
import logging

from farmers.manager.database import factory, exceptions

# This is a hack for exception handling, ideally we would override 
# the connection functions exception and throw our own customer exception instead.
# This would allow us to be Connection Agnostic and not have to import all the 
# different exception types for each Factory Type but since we are short on time
# we will just do this.
from pymongo import errors, ReturnDocument

class ItemDAO():
    """
    Inventory Item Data Access Object.
    """
    def __init__(self):
        module_class_name = self.__module__ + "." + self.__class__.__name__
        self.logger = logging.getLogger(module_class_name)
        self.connection_factory_type = factory.ConnectionFactoryType.MONGODB
    
    def create(self, code, name, price):
        """
        Create an item in inventory.

        :param code: item code. \n
        :type code: string. \n
        :param name: item name. \n
        :type name: string. \n
        :param price: item price. \n
        :type price: \n
        :returns: True if success else False. \n
        :rypte: boolean.
        """
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            with connection_factory.get_connection() as client:
                document = {"code": code, "name": name, "price": price}
                client.farmers.inventory.save(document)
        except errors.DuplicateKeyError as duplicate_key_error:
            self.logger.error(duplicate_key_error)
            return False
        return True
        
    def read(self, code=None, name=None):
        """
        Read an item from inventory using code or name.

        :param code: item code. \n
        :type code: string. \n
        :param name: item name. \n
        :type name: string. \n
        :raises:
          - ValueError: if neither code nor name is supplied.
        :returns: dictionary composed of code, name and price or None if it can't be found. \n
        :rypte: `dict`.
        """
        if not code and not name:
            raise ValueError("Need to supply either item code or name!")
        item = None
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            with connection_factory.get_connection() as client:
                if code:
                    _filter = {"code": code}
                else:
                    _filter = {"name": name}
                item = client.farmers.inventory.find_one(_filter)
                if item:
                    item.pop("_id")
        except Exception as exception:
            self.logger.error(exception)
            return item
        return item

    def update(self, code, name=None, price=None):
        """
        Updates an item from inventory using name or price or both.

        :param code: item code. \n
        :type code: string. \n
        :param name: item name. \n
        :type name: string. \n
        :raises:
          - ValueError: if neither code nor name is supplied.
        :returns: dictionary composed of code, name and price or None if it can't be found. \n
        :rypte: `dict`.
        """
        if not code and not name:
            raise ValueError("Need to supply either item code or name!")
        connection_factory = factory.connection_factory(self.connection_factory_type)
        document = None
        try:
            with connection_factory.get_connection() as client:
                _filter = {"code": code}
                if name and price:
                    update = {"name": name, "price": price}
                elif name:
                    update = {"name": name}
                else:
                    update = {"price", price}
                document = client.farmers.inventory.find_one_and_update(_filter,
                                                                        {"$set": update},
                                                                        return_document=ReturnDocument.AFTER)
                if document:
                    document.pop("_id")
        except Exception as exception:
            self.logger.error(exception)
            return document
        return document
    
    def delete(self, code=None, name=None):
        """
        Delete an item from inventory using code or name.

        :param code: item code. \n
        :type code: string. \n
        :param name: item name. \n
        :type name: string. \n
        :raises:
          - ValueError: if neither code nor name is supplied.
        :returns: True if succes else False. \n
        :rtype: boolean.
        """
        if not code and not name:
            raise ValueError("Need to supply either item code or name!")
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            with connection_factory.get_connection() as client:
                if code:
                    _filter = {"code": code}
                else:
                    _filter = {"name": name}
                result = client.farmers.inventory.delete_one(_filter)
                if result and result.deleted_count == 1:
                    return True
        except Exception as exception:
            self.logger.error(exception)
            return False
        return False
    