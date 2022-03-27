import feutils


class Item:
    def __init__(self, item_code):
        self.item_code = item_code
        self.name = feutils.item_table(item_code)
        self.item_type = feutils.item_type_table(item_code)

        self.info = feutils.item_info_lookup(self.name, self.item_type)

    def __str__(self):
        return self.name


def construct_unit_inventory(inventory_codes: list):
    inventory = []
    for code in inventory_codes:
        inventory.append(Item(code))
    return inventory
