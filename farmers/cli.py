# Copyright 2018 Abraham Cabrera.

import argparse
import sys

from farmers.manager.inventory import InventoryManager
from prettytable import PrettyTable
from pprint import pprint


def handle_add(code, name, price):
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
    inventory_manager = InventoryManager()
    try:
        if inventory_manager.add(code, name, price):
            print("Item added succesfully")
            return True
    except TypeError as type_error:
        print("Failed to add item because price is not of type float.")
        return False
    print("Could not add item to inventory!")
    return False


def handle_remove(code):
    """
    Remove item from inventory by code.

    :param code: item code. \n
    :type code: string. \n
    :returns: True if success else False. \n
    :rtype: boolean.
    """
    inventory_manager = InventoryManager()
    try:
        if inventory_manager.remove(_code=code):
            print("Item removed succesfully.")
            return True
    except ValueError as value_error:
        print("Must supply code of item to remove.")
    return False


def handle_update(code, field, value):
    """
    Updates an item in inventory.

    :param code: item code. \n
    :type code: string. \n
    :param field: item key to be updated. \n
    :type field: string. \n
    :param value: item value. \n
    :type value: string|float. \n
    :returns: True if success else False. \n
    :rtype: boolean.
    """
    try:
        success = False
        inventory_manager = InventoryManager()
        if field == "name" and isinstance(value, str):
            success = inventory_manager.update(code, _name=value)
        elif field == "price" and isinstance(value, float):
            success = inventory_manager.update(code, _price=value)
        else:
            return TypeError("value has incorrect type")
        if success:
            print("Update success.")
            return True
    except TypeError as type_error:
        print("Price must be of type float!")
        return False
    print("Item with code does not exist.")
    return False


def handle_get(field, value, format):
    """
    Updates an item in inventory.

    :param field: item key to be updated. \n
    :type field: string. \n
    :param value: item value. \n
    :type value: string|float. \n
    :param format: format to print the item in. \n
    :type format: string. \n
    :returns: True if success else False. \n
    :rtype: boolean.
    """
    inventory_manager = InventoryManager()
    item = None
    if field == "code":
        item = inventory_manager.get(_code=value)
    elif field == "name":
        item = inventory_manager.get(_name=value)
    else:
        raise ValueError("Field must be either code or name.")
    if not item:
        print("Item not found!")
        return False
    if format == "pretty":
        pretty_table = PrettyTable()
        pretty_table.field_names = ["Code", "Name", "Price"]
        pretty_table.add_row([item["code"],
                              item["name"],
                              "${0:.2}".format(item["price"])])
        print(pretty_table)
    elif format == "json":
        pprint(item)
    else:
        print("Format must be either pretty or json.")
        return False
    return True


def handle_list_items(format):
    """
    Prints all the inventory items.

    :param format: format to print the item in. \n
    :type format: string. \n
    :returns: True if success else False. \n
    :rtype: boolean.
    """
    inventory_manager = InventoryManager()
    items = inventory_manager.get_all()
    if not items:
        print("No items to display")
        return False
    if format == "pretty":
        pretty_table = PrettyTable()
        pretty_table.field_names = ["Code", "Name", "Price"]
        for key in items:
            row_item = [key,
                        items[key]["name"],
                        "${0:.2f}".format(items[key]["price"])]
            pretty_table.add_row(row_item)
        print(pretty_table)
    elif format == "json":
        pprint(items)
    else:
        print("Format must be either pretty or json.")
        return False
    return True


def handle_args(args):
    status = False
    if args.command == "add":
        status = handle_add(args.code, args.name, args.price)
    elif args.command == "remove":
        status = handle_remove(args.code)
    elif args.command == "get":
        status = handle_get(args.field, args.value, args.format)
    elif args.command == "update":
        status = handle_update(args.code, args.field, args.value)
    else:
        status = result = handle_list_items(args.format)
    return status


def main():
    parser = argparse.ArgumentParser(description="Farmers Market Inventory Manager cli")

    inventory_parsers = parser.add_subparsers(dest="command")
    
    inventory_add_parser = inventory_parsers.add_parser("add", help="Add item to inventory.")
    inventory_add_parser.add_argument("--code", type=str, required=True, help="code of item to add.")
    inventory_add_parser.add_argument("--name", type=str, required=True, help="name of item to add.")
    inventory_add_parser.add_argument("--price", type=float, required=True, help="price of item to add.")

    inventory_remove_parser = inventory_parsers.add_parser("remove", help="Remove item from inventory")
    inventory_remove_parser.add_argument("--code", type=str, required=True, help="code of item to remove.")

    inventory_get_parser = inventory_parsers.add_parser("get", help="Get item from inventory.")
    inventory_get_parser.add_argument("--field", choices=["code", "name"], help="Get item by code.")
    inventory_get_parser.add_argument("--value", help="Get name by code.")
    inventory_get_parser.add_argument("--format", choices=["pretty", "json"], default="pretty", help="Format to print the item.")

    inventory_update_parser = inventory_parsers.add_parser("update", help="Update item from inventory.")
    inventory_update_parser.add_argument("--code", type=str, required=True, help="code of item to update.")
    inventory_update_parser.add_argument("--field", choices=["name", "price"], help="Name of item to update.")
    inventory_update_parser.add_argument("--value", help="Price of item to update.")

    inventory_list_parser = inventory_parsers.add_parser("list", help="List items in inventory")
    inventory_list_parser.add_argument("--format", choices=["pretty", "json"], default="pretty", help="Format to print the items.")

    args = parser.parse_args()

    status = handle_args(args)
    return 0 if status else 1


if __name__ == "__main__":
    sys.exit(main())