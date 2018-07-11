# Copyright 2018, Abraham Cabrera

from farmers.manager.database.dao.item import ItemDAO

def test_item_dao():
    # Create an item data access object.
    item_dao = ItemDAO()

    # Create an item in inventory.
    assert item_dao.create("MF1", "Muffins", float(2.50))

    # Get said created item by code.
    item = item_dao.read(code="MF1")

    # Validate contents are right.
    assert item
    assert item["code"] == "MF1"
    assert item["name"] == "Muffins"
    assert float(item["price"]) == float(2.50)

    # Raising the price to $3.00
    assert item_dao.update("MF1", price=float(3.00))

    # Get item again by name.
    item = item_dao.read(name="Muffins")
    # Validate contents are right.
    assert item
    assert float(item["price"]) == float(3.00)

    # Remove item from inventory
    assert item_dao.delete(code="MF1")
