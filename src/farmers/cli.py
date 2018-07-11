# Copyright 2018 Abraham Cabrera.

import argparse
import math
import sys

from farmers.manager.inventory import InventoryManager
from farmers.manager.orders import BasketManager
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
    #try:
    if inventory_manager.add(code, name, price):
        print("Item added succesfully")
        return True
    #except TypeError as type_error:
    #    print("Failed to add item because price is not of type float.")
    #    return False
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
        if field == "name":
            success = inventory_manager.update(code, _name=value)
        elif field == "price":
            success = inventory_manager.update(code, _price=float(value))
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


def handle_basket_create(codes):
    """
    Handler for basket create operation.
    """
    bm = BasketManager()
    basket = bm.create(codes)
    print("Basket was created with id: {0}".format(basket))
    return True


def handle_basket_checkout(_id):
    """
    Handler for basket checkout operation.
    """
    bm = BasketManager()
    return bm.checkout(_id)


def handle_basket_cancel(_id):
    """
    Handler for basket cancel operation.
    """
    bm = BasketManager()
    return bm.cancel(_id)


def handle_basket_add_item(_id, code):
    """
    Handler for basket add item operation.
    """
    bm = BasketManager()
    return bm.additem(_id, code)


def handle_basket_remove_item(_id, code):
    """
    Handler for basket add item operation.
    """
    bm = BasketManager()
    return bm.removeitem(_id, code)


def determine_basket_promos(codes):
    """
    Determine Promotional Rules.

    :param codes: List of item codes. \n
    :type codes: list. \n
    :returns: dictionary of items with promos.
    :rtype: dict
    """
    items = {}
    inventory_manager = InventoryManager()
    subtotal = float(0.00)
    for code in codes:
        item = inventory_manager.get(_code=code)
        subtotal = subtotal + item["price"]
        if code not in items:
            items[code] = {"count": 1,
                            "price": item["price"],
                            "promo": "",
                            "promo-count": 0, 
                            "promo-price": float(0)}
        else:
            items[code]["count"] = items[code]["count"] + 1
        # Applying promo rules.
        # BOGO -- Buy-One-Get-One-Free Special on Coffee. (Unlimited)
        if "CF1" in items and items[code]["count"] % 2 == 0:
            items[code]["promo"] = "BOGO"
            items[code]["promo-count"] = int(math.floor(items[code]["count"] / 2))
            items[code]["promo-price"] = (-1) * items[code]["price"]
        # CHMK -- Purchase a box of Chai and get milk free. (Limit 1)
        if "MK1" in items and "CH1" in items:
            if items["MK1"]["promo-count"] == 0:
                items["MK1"]["promo"] = "CHMK"
                items["MK1"]["promo-count"] = 1
                items["MK1"]["promo-price"] = (-1) * items["MK1"]["price"]
        # APPL -- If you buy 3 or more bags of Apples, the price drops to $4.50.
        if "AP1" in items and items["AP1"]["count"] >= 3:
            items["AP1"]["promo"] = "APPL"
            items["AP1"]["promo-count"] = items["AP1"]["count"]
            items["AP1"]["promo-price"] = (-1.00) * 1.50
        # Missing rule for APOM -- Purchase a bag of Oatmeal and get 50% off a bag of Apples
    return items

def handle_basket_print(_id, format):
    """
    Handler for basket print operation.
    """
    basket = BasketManager().get(_id)
    if not basket:
        print("Basket could not be found.")
        return False
    if format == "pretty":
        codes = basket["items"]
        if codes:
            items = determine_basket_promos(codes)
            subtotal = float(0.0)
            promos = float(0.0)
            pretty_table = PrettyTable()
            pretty_table.field_names = ["Item", "Promo", "Promo-count", "Price"]
            for item in items:
                subtotal = subtotal + (items[item]["price"] * items[item]["count"])
                promos = promos + (items[item]["promo-price"] * items[item]["promo-count"])
                for idx in range(1, items[item]["count"]):
                    pretty_table.add_row([item, "", "", "${0:.2f}".format(items[item]["price"])])
                if items[item]["promo-count"] > 0:
                    pretty_table.add_row(["", 
                                          items[item]["promo"],
                                          items[item]["promo-count"],
                                          "${0:.2f}".format(items[item]["promo-price"])])
            total = subtotal + promos
            difference = subtotal - total
            print(pretty_table)
            print("Subtotal: ${0:.2f}".format(subtotal))
            print("Total: ${0:.2f}".format(total))
            if difference > 0:
                print("You saved: ${0:.2f}".format(difference))
        else:
            print("Not items in basket.")
    elif format == "json":
        pprint(basket)
    else:
        print("Invalid format option.")
        return False
    return True


def handle_args(args):
    status = False
    if args.command == "inventory-add":
        status = handle_add(args.code, args.name, args.price)
    elif args.command == "inventory-remove":
        status = handle_remove(args.code)
    elif args.command == "inventory-get":
        status = handle_get(args.field, args.value, args.format)
    elif args.command == "inventory-update":
        status = handle_update(args.code, args.field, args.value)
    elif args.command == "inventory-list":
        status = handle_list_items(args.format)
    elif args.command == "basket-add":
        status = handle_basket_add_item(args.id, args.code)
    elif args.command == "basket-create":
        status = handle_basket_create(args.codes)
    elif args.command == "basket-checkout":
        status = handle_basket_checkout(args.id)
    elif args.command == "basket-cancel":
        status = handle_basket_cancel(args.id)
    elif args.command == "basket-print":
        status = handle_basket_print(args.id, args.format)
    elif args.command == "basket-remove":
        status = handle_basket_remove_item(args.id, args.code)
    else:
        print("Unsupported command")
    return status


def main():
    parser = argparse.ArgumentParser(description="Farmers Market Manager cli")

    parsers = parser.add_subparsers(dest="command")
    
    inventory_add_parser = parsers.add_parser("inventory-add", help="Add item to inventory.")
    inventory_add_parser.add_argument("--code", type=str, required=True, help="code of item to add.")
    inventory_add_parser.add_argument("--name", type=str, required=True, help="name of item to add.")
    inventory_add_parser.add_argument("--price", type=float, required=True, help="price of item to add.")

    inventory_remove_parser = parsers.add_parser("inventory-remove", help="Remove item from inventory")
    inventory_remove_parser.add_argument("--code", type=str, required=True, help="code of item to remove.")

    inventory_get_parser = parsers.add_parser("inventory-get", help="Get item from inventory.")
    inventory_get_parser.add_argument("--field", choices=["code", "name"], help="Get item by code.")
    inventory_get_parser.add_argument("--value", help="Get name by code.")
    inventory_get_parser.add_argument("--format", choices=["pretty", "json"], default="pretty", help="Format to print the item.")

    inventory_update_parser = parsers.add_parser("inventory-update", help="Update item from inventory.")
    inventory_update_parser.add_argument("--code", type=str, required=True, help="code of item to update.")
    inventory_update_parser.add_argument("--field", choices=["name", "price"], help="Name of item to update.")
    inventory_update_parser.add_argument("--value", help="Price of item to update.")

    inventory_list_parser = parsers.add_parser("inventory-list", help="List items in inventory")
    inventory_list_parser.add_argument("--format", choices=["pretty", "json"], default="pretty", help="Format to print the items.")

    basket_add_parser = parsers.add_parser("basket-add", help="Add item to basket.")
    basket_add_parser.add_argument("--id", required=True, help="Id of basket to add to")
    basket_add_parser.add_argument("-c", "--code", required=True, help="codes of items to add to bucket.")

    basket_cancel_parser = parsers.add_parser("basket-cancel", help="Cancel basket.")
    basket_cancel_parser.add_argument("--id", required=True, help="Id of basket to cancel")

    basket_checkout_parser = parsers.add_parser("basket-checkout", help="Checkout basket.")
    basket_checkout_parser.add_argument("--id", required=True, help="Id of basket to checkout")

    basket_create_parser = parsers.add_parser("basket-create", help="Create Basket.")
    basket_create_parser.add_argument("-c", "--codes", nargs='+', required=True, help="codes of items to add during creation of bucket.")

    basket_print_parser = parsers.add_parser("basket-print", help="Print basket.")
    basket_print_parser.add_argument("--id", required=True, help="Id of basket to print")
    basket_print_parser.add_argument("--format", choices=["pretty", "json"], default="pretty", help="Format to print the item.")

    basket_remove_parser = parsers.add_parser("basket-remove", help="Remove item from basket.")
    basket_remove_parser.add_argument("--id", required=True, help="Id of basket to print")
    basket_remove_parser.add_argument("-c", "--code", required=True, help="codes of items to remove from bucket.")

    args = parser.parse_args()
    status = handle_args(args)
    return 0 if status else 1


if __name__ == "__main__":
    sys.exit(main())