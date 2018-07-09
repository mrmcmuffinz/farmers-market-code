import logging

from farmers.manager.database import factory, exceptions

class ItemsDAO():
    def __init__(self):
        module_class_name = self.__module__ + "." + self.__class__.__name__
        self.logger = logging.getLogger(module_class_name)
        self.connection_factory_type = factory.ConnectionFactoryType.MONGODB

    def read(self):
        """
        Read all items from inventory.

        :returns: dictionary composed of code(key), name and price. \n
        :rypte: `dict`.
        """
        items = {}
        connection_factory = factory.connection_factory(self.connection_factory_type)
        try:
            with connection_factory.get_connection() as client:
                for item in client.farmers.inventory.find():
                    items[item["code"]] = {
                        "name": item["name"],
                        "price": item["price"]
                    }
        except Exception as exception:
            self.logger.error(exception)
            return items
        return items
