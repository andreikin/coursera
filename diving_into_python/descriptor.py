


class Value:
    def __init__(self, amount):
        self.amount = amount

    def __get__(self, obj, obj_type):
        return self.amount

    def __set__(self, obj, value):
        with open('log.txt', 'w') as f:
            f.write(str(value))

        self.amount = value


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission