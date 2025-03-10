from appium_ios_controller import AppiumIOSController
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


def create_buy_pipeline(buy_index: int) -> dict:
    """创建单个购买流程的pipeline"""
    return {
        f"FindMin_{buy_index}": {
            "recognition": "OCR",
            "expected": "Min",
            "action": "Click",
            "next": [f"FindBuy_{buy_index}"]
        },
        f"FindBuy_{buy_index}": {
            "recognition": "OCR",
            "expected": "Buy",
            "index": buy_index,  # 指定第几个Buy
            "action": "Click",
            "next": ["FindInAppPurchase"]
        },
        "FindInAppPurchase": {
            "recognition": "OCR",
            "expected": "In-App Purchase",
            "action": "Click",
            "next": ["FindBlueButton"]
        },
        "FindBlueButton": {
            "recognition": "OCR",
            "expected": "购买",
            "action": "Click",
            "next": ["CheckPassword", "FindOK"]
        },
        "CheckPassword": {
            "recognition": "OCR",
            "expected": "密码",
            "action": "DoNothing",
            "next": ["InputPassword", "FindOK"],
            "timeout": 2
        },
        "InputPassword": {
            "action": "InputText",
            "input_text": "Iapiapiap0",
            "next": ["FindBlueConfirm", "FindOK"]
        },
        "FindBlueConfirm": {
            "recognition": "OCR",
            "expected": "登录",
            "index": -1,  # 第一个蓝色按钮
            "action": "Click",
            "next": ["FindOK"]
        },
        "FindOK": {
            "recognition": "OCR",
            "expected": "好",
            "action": "Click",
            "next": []
        }
    }


def run_pipeline(controller: AppiumIOSController, buy_index: int):
    # 构建完整的pipeline
    pipeline = {
        "Entry": {
            "next": ["TryLogin", f"FindMin_{buy_index}"]
        },
        "TryLogin": {
            "recognition": "OCR",
            "expected": "Log In",
            "action": "Click",
            "next": ["TryGuest", f"FindMin_{buy_index}"]
        },
        "TryGuest": {
            "recognition": "OCR",
            "expected": "Continue with Guest",
            "action": "Click",
            "next": [f"FindMin_{buy_index}"]
        }
    }

    # 添加第一组购买流程
    pipeline.update(create_buy_pipeline(buy_index))

    # 添加结束节点到 pipeline
    pipeline.update({"End": {}})

    # 运行流水线，指定资源路径
    result = controller.run_pipeline(
        pipeline=pipeline,
        resource_path="./resource"
    )
    print(f"任务执行结果: {result}")


if __name__ == "__main__":
    # iOS 设备配置
    ios_capabilities = {
        "platformName": "iOS",
        "appium:udid": "42a4c4c46c2f19ae1031e967d8154136fd93c681",
        "appium:automationName": "XCUITest",
        "appium:platformVersion": "16.7.10",
        "appium:bundleId": "com.diviner.test",
        "appium:newCommandTimeout": 60,
        "appium:wdaLocalPort": 8100
    }

    # 创建控制器实例
    controller = AppiumIOSController(
        capabilities=ios_capabilities,
        notification_handler=MyNotificationHandler()
    )
    run_pipeline(controller, 0)
    run_pipeline(controller, 1)
    run_pipeline(controller, 2)
    run_pipeline(controller, 3)
