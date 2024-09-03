# auth.py

from typing import TypedDict, Union
# from .base import ObservableModel


class User(TypedDict):
    username: str


# base.py

from typing import Callable, TypeVar, Any

Self = TypeVar("Self", bound="ObservableModel")


class ObservableModel:
    """Models that can have event listeners.

    Observable models can register callback functions for specific events.
    When any data changes, relavent events can be triggered.
    This allows all the controllers that depends on the current state of those data to
    react to the changes.
    """

    def __init__(self):
        self._event_listeners: dict[str, list[Callable[[Any], None]]] = {}

    def add_event_listener(self, event: str, fn: Callable[[Self], None]) -> Callable:
        """Registers event callback functions.

        Adds a callback function to the list of listeners of the specified event and
        returns a function that removes the listener from the list.

        Args:
            event (str): Name of the event.
            fn (function): Callback function to be registered.
                The function will be called with the model instance as the argument.

        Returns:
            function: Function to remove the listener function.
        """
        try:
            self._event_listeners[event].append(fn)
        except KeyError:
            self._event_listeners[event] = [fn]

        return lambda: self._event_listeners[event].remove(fn)

    def trigger_event(self, event: str) -> None:
        if event not in self._event_listeners.keys():
            return

        for func in self._event_listeners[event]:
            func(self)


class Auth(ObservableModel):
    def __init__(self):
        super().__init__()
        self.is_logged_in = False
        self.current_user: Union[User, None] = None

    def login(self, user: User) -> None:
        self.is_logged_in = True
        self.current_user = user
        self.trigger_event("auth_changed")

    def logout(self) -> None:
        self.is_logged_in = False
        self.current_user = None
        self.trigger_event("auth_changed")


# init_model.py

# from .auth import Auth


class Model:
    def __init__(self):
        self.auth = Auth()

