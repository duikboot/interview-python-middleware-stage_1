import inspect
from abc import ABC, abstractmethod
from threading import local
from typing import Any, List, cast

from haps import SINGLETON_SCOPE, base, egg, scope


@base
class Registry(ABC):
    @property  # type: ignore
    @abstractmethod
    def access_token(self) -> str:
        pass

    @access_token.setter  # type: ignore
    @abstractmethod
    def access_token(self, token: str) -> None:
        pass

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def clean(self) -> None:
        pass


@egg
@scope(SINGLETON_SCOPE)
class ThreadLocalRegistry(Registry):
    def __init__(self) -> None:
        self._initialized = False
        self._registry = local()

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self.properties_names and self._initialized is False:
            raise AttributeError(
                "You can not set property value when Registry is not initialized"
            )
        super(ThreadLocalRegistry, self).__setattr__(key, value)

    def __getattr__(self, item: str) -> Any:
        if item in self.properties_names and self._initialized is False:
            raise AttributeError(
                "You can not get property value when Registry is not initialized"
            )

        return super(ThreadLocalRegistry, self).__getattribute__(item)

    def __delattr__(self, name: str) -> None:
        try:
            del self._registry.__dict__[name]
        except KeyError:
            pass

    @property
    def properties_names(self) -> List[str]:
        return [
            name
            for (name, value) in inspect.getmembers(
                Registry, lambda v: isinstance(v, property)
            )
        ]

    @property
    def access_token(self) -> str:
        return cast(str, self._registry.access_token)

    @access_token.setter
    def access_token(self, token: str) -> None:
        self._registry.access_token = token

    def initialize(self) -> None:
        self.clean()
        self._initialized = True

    def clean(self) -> None:
        del self.access_token
        del self.requesting_user
        del self.base_source
        del self.detail_source
        self._initialized = False
