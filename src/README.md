
# Farmers Market CLI

Welcome to farmers market cli, below you can see some examples of how to use it.

# Help Menu

```
$ farmers -h
usage: farmers [-h]
               {inventory-add,inventory-remove,inventory-get,inventory-update,inventory-list,basket-add,basket-cancel,basket-checkout,basket-create,basket-print,basket-remove}
               ...

Farmers Market Manager cli

positional arguments:
  {inventory-add,inventory-remove,inventory-get,inventory-update,inventory-list,basket-add,basket-cancel,basket-checkout,basket-create,basket-print,basket-remove}
    inventory-add       Add item to inventory.
    inventory-remove    Remove item from inventory
    inventory-get       Get item from inventory.
    inventory-update    Update item from inventory.
    inventory-list      List items in inventory
    basket-add          Add item to basket.
    basket-cancel       Cancel basket.
    basket-checkout     Checkout basket.
    basket-create       Create Basket.
    basket-print        Print basket.
    basket-remove       Remove item from basket.

optional arguments:
  -h, --help            show this help message and exit
```

# List Items in inventory

```
$ farmers inventory-list
+------+---------+--------+
| Code |   Name  | Price  |
+------+---------+--------+
| AP1  |  Apples | $6.00  |
| CF1  |  Coffee | $11.23 |
| CH1  |   Chai  | $3.11  |
| MK1  |   Milk  | $4.75  |
| OM1  | Oatmeal | $3.69  |
+------+---------+--------+
```

# Add item to inventory:

```
$ farmers inventory-add --code="AP1" --name="Apples" --price=6.00
Item added succesfully
$ farmers inventory-add --code="CF1" --name="Coffee" --price=11.23
Item added succesfully
$ farmers inventory-add --code="CH1" --name="Chai" --price=3.11
Item added succesfully
$ farmers inventory-add --code="MK1" --name="Milk" --price=4.75
Item added succesfully
$ farmers inventory-add --code="OM1" --name="Oatmeal" --price=3.69
Item added succesfully
```