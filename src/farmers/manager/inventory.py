# Copyright 2018 Abraham Cabera.

import logging

from farmers.manager.database.dao import item, items

class InventoryManager():
    def __init__(self):
        module_class_name = self.__module__ + "." + self.__class__.__name__
        self.logger = logging.getLogger(module_class_name)

    def add(self, code, name, price):
        """
        Add item to inventory.

        :param code: item code. \n
        :type code: string. \n
        :param name: item name. \n
        :type name: string. \n
        :param price: item price. \n
        :type price: float. \n
        :returns: True if success else False. \n
        :rtype: boolean.
        """
        price = float(price)
        _item = item.ItemDAO()
        return _item.create(code, name, price)
    
    def remove(self, _code=None, _name=None):
        """
        Removes an item from inventory by code or name.

        :param code: item code. \n
        :type code: string. \n
        :param name: item name. \n
        :type name: string. \n
        :returns: True if success else False. \n
        :rtype: boolean.
        """
        if not _code and not _name:
            raise ValueError("Item name and price cannot be None")
        _item = item.ItemDAO()
        return _item.delete(code=_code, name=_name)

    def update(self, code, _name=None, _price=None):
        """
        Updates an item in inventory either by name, price or both.

        :param code: item code. \n
        :type code: string. \n
        :param name: item name. \n
        :type name: string. \n
        :param price: item price. \n
        :type price: float. \n
        :returns: True if success else False. \n
        :rtype: boolean.
        """
        if not _name and not _price:
            raise ValueError("Item name and price cannot be None")
        _item = item.ItemDAO()
        if _item.update(code, name=_name, price=_price):
            return True
        return False
    
    def get(self, _code=None, _name=None):
        """
        Gets an item in inventory either by code or name.

        :param code: item code. \n
        :type code: string. \n
        :param name: item name. \n
        :type name: string. \n
        :returns: item dictionary. \n
        :rtype: `dict`.
        """
        if not _code and not _name:
            raise ValueError("Must specify code and name!")
        _item = item.ItemDAO()
        return _item.read(code=_code, name=_name)

    def get_all(self):
        """
        Gets all items in inventory.

        :returns: Dictionary of all items. \n
        :rtype: `dict`.
        """
        _items = items.ItemsDAO()
        return _items.read()