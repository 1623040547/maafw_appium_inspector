from appium import webdriver
import numpy as np
from maa.notification_handler import NotificationHandler
import cv2
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from appium.options.common.base import AppiumOptions
from typing import Dict, Any

from maa.resource import Resource
from maa.tasker import Tasker
from .appium_controller import AppiumController
from .custom_actions import LongPressAction, RecNext, RatioPanel, AppBack, ForEach, FindText


class AppiumIOSController(AppiumController):
    def start_app(self, intent: str) -> bool:
        pass

    def stop_app(self, intent: str) -> bool:
        pass

    def __init__(
        self,
        capabilities: Dict[str, Any],
        server_url: str = "http://127.0.0.1:4723",
        notification_handler: NotificationHandler = None,
    ):
        """
        初始化 iOS Appium 控制器
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
        options = AppiumOptions()
        options.load_capabilities(self.capabilities)
        self.driver = webdriver.Remote(self.server_url, options=options)

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
            # 获取设备实际屏幕尺寸
            window_size = self.driver.get_window_size()
            self.device_width = window_size["width"]
            self.device_height = window_size["height"]
            # 重新计算缩放因子（以宽度为基准，因为是竖屏应用）
            print(f"设备屏幕尺寸: {self.device_width}x{self.device_height}")
        except Exception as e:
            print(f"获取设备尺寸失败: {e}")

    def screencap(self) -> np.ndarray:
        print("screencap start")
        try:
            # 获取截图
            screenshot = self.driver.get_screenshot_as_png()
            # 直接将PNG转换为numpy数组
            image_array = cv2.imdecode(
                np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR
            )

            # 计算目标尺寸（竖屏应用，以宽度为短边）
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
            print(f"Click ${x} ${y}")
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
            actions.w3c_actions.pointer_action.pause(duration / 1000)  # 转换为秒
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
        except:
            return False

    def input_text(self, text: str) -> bool:
        print("input_text start ", text)
        try:
            # 获取所有顶层元素
            elements = self.driver.find_elements("class name", "XCUIElementTypeAny")
            input_field = None

            # 遍历查找输入框
            for element in elements:
                try:
                    element_type = element.get_attribute("type")
                    if element_type in [
                        "XCUIElementTypeSecureTextField",
                        "XCUIElementTypeTextField",
                    ]:
                        input_field = element
                        break
                except:
                    continue

            # 如果没找到输入框，使用第一个元素
            if not input_field and elements:
                input_field = elements[0]

            if input_field:
                input_field.send_keys(text)
                return True

            return False

        except Exception as e:
            print(f"Input text failed: {e}")
            return False

    def run_pipeline(
        self, pipeline: Dict[str, Any], resource_path: str = None
    ) -> Dict[str, Any]:
        """
        运行 MAA 任务流水线
        :param pipeline: 任务流水线配置
        :param resource_path: 资源路径，默认为当前目录下的 resource 文件夹
        :return: 任务执行结果
        """
        try:
            if resource_path is None:
                import os

                resource_path = os.path.join(os.path.dirname(__file__), "resource")

            # 初始化资源
            resource = Resource()
            resource.use_cpu()
            resource.register_custom_action("LongPress", LongPressAction(self))
            resource.register_custom_action("RecNext", RecNext(self))
            resource.register_custom_action("RatioPanel", RatioPanel(self))
            resource.register_custom_action("AppBack", AppBack(self))
            resource.register_custom_action("ForEach", ForEach(self))
            resource.register_custom_recognition("FindText", FindText(self))

            # 加载资源
            res_job = resource.post_bundle(resource_path)
            result = res_job.wait()
            if not result.succeeded:
                print(f"资源加载失败: {result}")
                return {}

            # 设置截图目标短边
            self.set_screenshot_target_short_side(self.device_width)

            # 连接控制器
            conn_result = self.post_connection().wait()
            if not conn_result.succeeded:
                print(f"控制器连接失败: {conn_result}")
                return {}

            # 创建任务管理器
            tasker = Tasker(notification_handler=self.notification_handler)

            # 绑定资源和控制器
            if not tasker.bind(resource, self):
                print("任务管理器绑定失败")
                return {}

            if not tasker.inited:
                print("MAA 初始化失败")
                return {}

            # 运行任务
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

    def find_element_by_text(self, text: str) -> list[tuple[int, int, int, int]]:
        print(f"Finding elements with text: {text}")
        try:
            # 使用 XPath 查找包含文本的元素
            elements = self.driver.find_elements("xpath", f"//*[contains(@label, '{text}') or contains(@name, '{text}') or contains(@value, '{text}')]")
            positions = []
            
            for element in elements:
                try:
                    # 获取元素位置和大小
                    location = element.location
                    size = element.size
                    
                    # 提取位置信息
                    x = int(location['x'])
                    y = int(location['y'])
                    w = int(size['width'])
                    h = int(size['height'])
                    
                    positions.append((x, y, w, h))
                except:
                    continue
                    
            return positions
        except Exception as e:
            print(f"Find elements by text failed: {e}")
            return []
