
class FEActionError(Exception):
    pass


class Action:
    def __init__(self, action_name, action_item):
        if action_name is not 'Attack' or 'Item' or 'Wait':
            raise FEActionError('Action was not of type Attack, Item, or Wait. Was: ' + action_name)

        self.name = action_name

        if action_name is 'Attack' and action_item is None:
            raise FEActionError('Attack actions must also have a unit action item associated with them.')

        if action_name is 'Item' and action_item is None:
            raise FEActionError('Item actions must also have an Item action item associated with them.')

        self.action_item = action_item

    def is_attack(self):
        return self.action_name is 'Attack'

    def is_item(self):
        return self.action_name is 'Item'

    def is_wait(self):
        return self.action_name is 'Wait'

