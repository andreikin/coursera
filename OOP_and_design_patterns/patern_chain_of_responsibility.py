class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet(): # создаёт событие получения данных соответствующего типа
    def __init__(self, type):
        self.kind = "get"
        self.type = type


class EventSet(): # создаёт событие изменения поля типа type(<value>)
    def __init__(self, val):
        self.kind = "set"
        self.val = val
        self.type = type(val)


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == "get" and event.type == int:
            return obj.integer_field
        elif event.kind == "set" and event.type == int:
            obj.integer_field = event.val
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == "get" and event.type == float:
            return obj.float_field
        elif event.kind == "set" and event.type == float:
            obj.float_field = event.val
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == "get" and event.type == str:
            return obj.string_field
        elif event.kind == "set" and event.type == str:
            obj.string_field = event.val
        else:
            return super().handle(obj, event)
