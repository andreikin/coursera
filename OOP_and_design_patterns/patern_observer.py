from abc import ABC, abstractmethod


class Engine:
    pass


class ObservableEngine(Engine):
    def __init__(self):
        self.__subscribers = set()  # При инициализации множество подписчиков задается пустым

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)  # Для того чтобы подписать пользователя, он добавляется во множество подписчиков

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)  # Удаление подписчика из списка

    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)  # Отправка уведомления всем подписчикам

    def prt(self):
        print(self.__subscribers)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, message): # Абстрактный наблюдатель задает метод update
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, message):
        self.achievements.add(message["title"])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, message):
        if not message in self.achievements:
            self.achievements.append(message)


