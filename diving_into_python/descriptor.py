class Value:

    def __init__(self):
        self.value = 0

    def __set__(self, instance, value):
        self.value = value - value * instance.commission

    def __get__(self, instance, obj_type):
        return self.value

