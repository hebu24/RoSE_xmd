from typing import Any


class Registry:
    def __init__(self):
        self._items: dict[str, Any] = {}

    def register(self, name: str, value: Any) -> Any:
        if name in self._items:
            raise KeyError(name)
        self._items[name] = value
        return value

    def get(self, name: str) -> Any:
        return self._items[name]

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))
