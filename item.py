import feutils
import item_type


class Item:
    def __init__(self, item_code):
        self.item_code = item_code
        self.name = feutils.item_table(item_code)
        self.item_type = feutils.item_type_table(item_code)

        self.info = feutils.item_info_lookup(self.name, self.item_type)

