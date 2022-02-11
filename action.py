
class FEActionError(Exception):
    pass


class Action:
    def __init__(self, action_name, action_item):
        # if action_name != 'Attack' or action_name != 'Item' or action_name != 'Wait':
        #     raise FEActionError(f"Action was not of type Attack, Item, or Wait. Was: '{action_name}'")

        self.name = action_name

        if action_name == 'Attack' and action_item is None:
            raise FEActionError('Attack actions must also have a unit action item associated with them.')

        if action_name == 'Item' and action_item is None:
            raise FEActionError('Item actions must also have an Item action item associated with them.')

        self.action_item = action_item

    def is_attack(self):
        return self.name == 'Attack'

    def is_item(self):
        return self.name == 'Item'

    def is_wait(self):
        return self.name == 'Wait'

    def __str__(self):
        if self.action_item is None:
            return f"{self.name}"
        return f"{self.name} - {self.action_item}"

