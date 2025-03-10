from appium import webdriver
import numpy as np
from maa.notification_handler import NotificationHandler
import cv2
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from typing import Dict, Any
from appium.options.android import UiAutomator2Options

from maa.resource import Resource
from maa.tasker import Tasker
from .custom_actions import LongPressAction, RecNext, RatioPanel, AppBack
from .appium_controller import AppiumController


class AppiumAndroidController(AppiumController):
    def __init__(
        self,
        capabilities: Dict[str, Any],
        server_url: str = "http://127.0.0.1:4723",
        notification_handler: NotificationHandler = None,
    ):
        """
        初始化 Android Appium 控制器
        :param capabilities: Appium capabilities 配置字典
        :param server_url: Appium 服务器地址
        :param notification_handler: 通知处理器
        """
        super().__init__(notification_handler=notification_handler)
        self.notification_handler = notification_handler
        self.driver = None
        self.device_width = 0
        self.device_height = 0
        self.server_url = server_url
        self.capabilities = capabilities
        self.init_driver()
        self.init_device_size()

    def init_driver(self):
        try:
            options = UiAutomator2Options()
            options.load_capabilities(self.capabilities)
            # 添加必要的基础配置
            if "appium:automationName" not in self.capabilities:
                options.set_capability("appium:automationName", "UiAutomator2")
            if "platformName" not in self.capabilities:
                options.set_capability("platformName", "Android")

            self.driver = webdriver.Remote(self.server_url, options=options)
            print("Successfully connected to Appium server")
        except Exception as e:
            print(f"Failed to initialize driver: {e}")
            raise

    def start_app(self, intent: str) -> bool:
        try:
            self.driver.start_activity(intent.split("/")[0], intent.split("/")[1])
            return True
        except Exception as e:
            print(f"Start app failed: {e}")
            return False

    def stop_app(self, intent: str) -> bool:
        try:
            self.driver.terminate_app(intent.split("/")[0])
            return True
        except Exception as e:
            print(f"Stop app failed: {e}")
            return False

    def connect(self) -> bool:
        print("connect start")
        try:
            return self.driver is not None
        except Exception as e:
            print(f"Connect failed: {e}")
            return False

    def request_uuid(self) -> str:
        print("request_uuid start")
        try:
            return self.driver.session_id if self.driver else ""
        except Exception as e:
            print(f"Request UUID failed: {e}")
            return ""

    def init_device_size(self):
        try:
            window_size = self.driver.get_window_size()
            self.device_width = window_size["width"]
            self.device_height = window_size["height"]
            print(f"设备屏幕尺寸: {self.device_width}x{self.device_height}")
        except Exception as e:
            print(f"获取设备尺寸失败: {e}")

    def screencap(self) -> np.ndarray:
        print("screencap start")
        try:
            screenshot = self.driver.get_screenshot_as_png()
            image_array = cv2.imdecode(
                np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR
            )
            target_w = self.device_width
            target_h = int(self.device_height * self.device_width / self.device_width)
            image_array = cv2.resize(
                image_array, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4
            )
            return image_array
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return np.zeros((1280, 720, 3), dtype=np.uint8)

    def click(self, x: int, y: int) -> bool:
        try:
            print(f"Click {x} {y}")
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(
                self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            return True
        except Exception as e:
            print(f"Click failed: {e}")
            return False

    def long_click(self, x: int, y: int, duration: float = 2.0) -> bool:
        try:
            print(f"Long click at {x}, {y} for {duration} seconds")
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(
                self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            return True
        except Exception as e:
            print(f"Long click failed: {e}")
            return False

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int) -> bool:
        print("swipe start")
        try:
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(
                self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(x1, y1)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration / 1000)
            actions.w3c_actions.pointer_action.move_to_location(x2, y2)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            return True
        except Exception as e:
            print(f"Swipe failed: {e}")
            return False

    def touch_down(self, contact: int, x: int, y: int, pressure: int) -> bool:
        print("touch_down start")
        try:
            actions = self.driver.action.pointer_inputs[contact]
            actions.move_to(x=x, y=y)
            actions.pointer_down(pressure)
            self.driver.perform(actions)
            return True
        except:
            return False

    def touch_move(self, contact: int, x: int, y: int, pressure: int) -> bool:
        print("touch_move start")
        try:
            actions = self.driver.action.pointer_inputs[contact]
            actions.move_to(x=x, y=y)
            self.driver.perform(actions)
            return True
        except:
            return False

    def touch_up(self, contact: int) -> bool:
        print("touch_up start")
        try:
            actions = self.driver.action.pointer_inputs[contact]
            actions.pointer_up()
            self.driver.perform(actions)
            return True
        except:
            return False

    def press_key(self, keycode: int) -> bool:
        print("press_key start")
        try:
            self.driver.press_keycode(keycode)
            return True
        except Exception as e:
            print(f"Press key failed: {e}")
            return False

    def input_text(self, text: str) -> bool:
        print("input_text start ", text)
        try:
            # Android 使用 set_value 方法输入文本
            focused_element = self.driver.switch_to.active_element
            if focused_element:
                focused_element.set_value(text)
                return True
            return False
        except Exception as e:
            print(f"Input text failed: {e}")
            return False

    def run_pipeline(
        self, pipeline: Dict[str, Any], resource_path: str = None
    ) -> Dict[str, Any]:
        try:
            if resource_path is None:
                import os

                resource_path = os.path.join(os.path.dirname(__file__), "resource")

            resource = Resource()
            resource.use_cpu()
            resource.register_custom_action("LongPress", LongPressAction(self))
            resource.register_custom_action("RecNext", RecNext(self))
            resource.register_custom_action("RatioPanel", RatioPanel(self))
            resource.register_custom_action("AppBack", AppBack(self))

            res_job = resource.post_bundle(resource_path)
            result = res_job.wait()
            if not result.succeeded:
                print(f"资源加载失败: {result}")
                return {}

            self.set_screenshot_target_short_side(self.device_width)

            conn_result = self.post_connection().wait()
            if not conn_result.succeeded:
                print(f"控制器连接失败: {conn_result}")
                return {}

            tasker = Tasker(notification_handler=self.notification_handler)

            if not tasker.bind(resource, self):
                print("任务管理器绑定失败")
                return {}

            if not tasker.inited:
                print("MAA 初始化失败")
                return {}

            task_detail = tasker.post_task("Entry", pipeline).wait().get()
            return task_detail

        except Exception as e:
            print(f"运行流水线失败: {e}")
            return {}

    def device_size(self) -> tuple[int, int]:
        return self.device_width, self.device_height

    def app_back(self) -> bool:
        try:
            self.driver.back()
            return True
        except Exception:
            return False
