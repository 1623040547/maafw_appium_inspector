from appium_android_controller import AppiumAndroidController
from maa.notification_handler import NotificationHandler, NotificationType
import time


# 添加通知处理器
class MyNotificationHandler(NotificationHandler):
    def on_resource_loading(
        self,
        noti_type: NotificationType,
        detail: NotificationHandler.ResourceLoadingDetail,
    ):
        print(f"资源加载状态: {noti_type}")
        print(f"资源加载详情: {detail}")
        print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    def on_controller_action(
        self,
        noti_type: NotificationType,
        detail: NotificationHandler.ControllerActionDetail,
    ):
        print(f"on_controller_action: {noti_type}, {detail}")

    def on_tasker_task(
        self, noti_type: NotificationType, detail: NotificationHandler.TaskerTaskDetail
    ):
        print(f"on_tasker_task: {noti_type}, {detail}")


def run_pipeline(controller: AppiumAndroidController, buy_index: int):
    # 构建完整的pipeline
    pipeline = {
        "Entry": {
            "action": "Custom",
            "custom_action": "RatioPanel",
            "custom_action_param": {
                "Entry": {
                    "custom_action": "AppBack",
                    "next": ["LeftSwipe"],
                },
                "LeftSwipe": {
                    "action": "Swipe",
                    "begin": [0.8, 0.5, 0, 0],
                    "end": [0.6, 0.5, 0, 0],
                    "next": ["Quit"],
                },
                "Quit": {
                    "action": "Click",
                    "target": [0.8, 0.85, 0, 0],
                    "next": ["SocailOpen"],
                },
                "SocailOpen": {
                    "recognition": "OCR",
                    "expected": "社交",
                    "action": "Click",
                    "target_offset": [0, -0.05, 0, 0],
                    "next": ["QQOpen"],
                },
                "QQOpen": {
                    "recognition": "OCR",
                    "expected": "QQ",
                    "action": "Click",
                    "target_offset": [0, -0.05, 0, 0],
                    "next": [],
                },
                # "next": ["FindSleep"],
            },
        },
        # "FindSleep": {
        #     "recognition": "OCR",
        #     "expected": "Relax",
        #     "action": "Custom",
        #     "custom_action": "RecNext",
        #     "custom_action_param": {"expected": "More"},
        #     "next": ["FindBreathing"],
        # },
        # "FindBreathing": {
        #     "recognition": "OCR",
        #     "expected": "Breathing Exercise",
        #     "action": "Click",
        # },
    }

    # 运行流水线
    result = controller.run_pipeline(pipeline=pipeline, resource_path="./resource")
    print(f"任务执行结果: {result}")


if __name__ == "__main__":
    # Android 设备配置
    android_capabilities = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "荣耀畅玩60 Plus",  # 或具体设备名称
        "appium:platformVersion": "14",  # 替换为实际的 Android 版本
        "appium:appPackage": "com.serenity.relax",  # 替换为实际的应用包名
        "appium:appActivity": ".MainActivity",  # 替换为实际的主活动名
        "appium:noReset": True,
        "appium:newCommandTimeout": 60,
    }
    # 创建控制器实例
    controller = AppiumAndroidController(
        capabilities=android_capabilities,
        notification_handler=MyNotificationHandler(),
        server_url="http://localhost:4723/wd/hub",  # 修改服务器URL，添加 /wd/hub
    )

    # 运行多次购买流程
    run_pipeline(controller, 0)
