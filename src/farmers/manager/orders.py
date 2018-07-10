# Copyright 2018 Abraham Cabera.

import logging

from farmers.manager.database.dao import item, items, basket

class BasketManager():
    def __init__(self):
        module_class_name = self.__module__ + "." + self.__class__.__name__
        self.logger = logging.getLogger(module_class_name)

    def create(self, codes):
        if not isinstance(codes, list):
            self.logger.error("Codes must be in formt of list.")
            return None
        code_errors = False
        for code in codes:
            if not item.ItemDAO().read(code=code):
                code_errors = True
                break
        if code_errors:
            self.logger.error("There are item codes in your list that do not exist in inventory!")
            return None
        return basket.BasketDAO().create(codes)

    def additem(self, _id, code):
        item_dao = item.ItemDAO()
        if item_dao.read(code=code):
            basket_dao = basket.BasketDAO()
            return basket_dao.additem(_id, code)
        self.logger.error("Item with code '%s', does not exist in inventory", code)
        return False

    def removeitem(self, _id, code):
        basket_dao = basket.BasketDAO()
        return basket_dao.removeitem(_id, code)

    def cancel(self, _id):
        basket_dao = basket.BasketDAO()
        return basket_dao.cancel(_id)

    def checkout(self, _id):
        basket_dao = basket.BasketDAO()
        return basket_dao.checkout(_id)

    def get(self, _id):
        basket_dao = basket.BasketDAO()
        return basket_dao.read(_id)