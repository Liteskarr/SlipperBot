"""
Аналог событий из c#
Подписчиком события может являться любой объект, для которого определен оператор вызова функции.
"""


class Signal:
    def __init__(self, *types):
        self._subs = []

    def add(self, function):
        """
        Добавляет нового подписчика.
        """
        self._subs.append(function)

    def delete(self, function_id: int):
        """
        Удаляет подписчика.
        """
        for i, s in enumerate(self._subs):
            if id(s) == function_id:
                del self._subs[i]
                return

    def notify(self, *args, **kwargs):
        """
        Оповещает всех подписчиков о произошедшем событии.
        """
        for subscriber in self._subs:
            subscriber(*args, **kwargs)
