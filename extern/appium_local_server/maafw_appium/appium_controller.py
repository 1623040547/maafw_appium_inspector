from maa.controller import CustomController
from abc import abstractmethod
from numpy import ndarray


class AppiumController(CustomController):
    @abstractmethod
    def connect(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def request_uuid(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def start_app(self, intent: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def stop_app(self, intent: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def screencap(self) -> ndarray:
        raise NotImplementedError

    @abstractmethod
    def click(self, x: int, y: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def touch_down(
        self,
        contact: int,
        x: int,
        y: int,
        pressure: int,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def touch_move(
        self,
        contact: int,
        x: int,
        y: int,
        pressure: int,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def touch_up(self, contact: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def press_key(self, keycode: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def input_text(self, text: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def long_click(self, x: int, y: int, duration: float = 2.0) -> bool:
        raise NotImplementedError

    def device_size(self) -> tuple[int, int]:
        raise NotImplementedError

    def app_back(self) -> bool:
        raise NotImplementedError
