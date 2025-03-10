from extern.appium_local_server.maafw_appium.appium_ios_controller import AppiumIOSController
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


if __name__ == "__main__":
    # iOS 设备配置
    ios_capabilities = {
        "platformName": "iOS",
        "appium:udid": "42a4c4c46c2f19ae1031e967d8154136fd93c681",
        "appium:automationName": "XCUITest",
        "appium:platformVersion": "16.7.10",
        # "appium:bundleId": "",
        "appium:app": "",
        "appium:newCommandTimeout": 60,
        "appium:wdaLocalPort": 8100
    }

    # 创建控制器实例
    controller = AppiumIOSController(
        capabilities=ios_capabilities,
        notification_handler=MyNotificationHandler()
    )
    main_pipeline = {
        "Entry": {
            "pre_wait_freezes": 400,
            "next": ["ClickHomeBuyButton"]
        },
        "ClickHomeBuyButton": {
            "recognition": "OCR",
            "expected": "Min",
            "action": "Click",
            "post_wait_freezes": 400,
            "next": ["BuyMins"]
        },
        "BuyMins": {
            "recognition": "OCR",
            "expected": "Balance",
            "post_wait_freezes": 2000,
            "action": "Custom",
            "custom_action": "RecNext",
            "custom_action_param": {
                "Entry": {
                    "next": ["FindMins", "ScrollDown"],
                },
                "FindMins": {
                    "recognition": "Custom",
                    "custom_recognition": "FindText",
                    "custom_recognition_param": {
                        "text": ""
                    },
                    "action": "Click",
                    "roi": [0, 10002, 20003, 20004],
                    "roi_offset": [0, 40, 0, -10002],
                    "on_error": ["ScrollDown"],
                },
                "ScrollDown": {
                    "action": "Swipe",
                    "post_wait_freezes": 2000,
                    "begin": [10001, 10002, 0, 0],
                    "begin_offset": [20, 60, 0, 0],
                    "end": [10001, 10002, 0, 0],
                    "end_offset": [20, -150, 0, 0],
                    "next": ["FindMins", "Close1", "Pass1"]
                },
                "Close1": {
                    "recognition": "FeatureMatch",
                    "template": "dialogClose.png",
                    "action": "Click",
                }, "Pass1": {}
            },
            "next": ["ClickInAppPurchase"]
        },
        "ClickInAppPurchase": {
            "recognition": "OCR",
            "expected": "In-App Purchase",
            "action": "Click",
            "next": ["ClickBuyBottomButton"]
        },
        "ClickBuyBottomButton": {
            "recognition": "OCR",
            "expected": "购买",
            "action": "Click",
            "next": ["CheckPassword", "ClickOK"]
        },
        "CheckPassword": {
            "recognition": "OCR",
            "expected": "密码",
            "action": "DoNothing",
            "next": ["InputPassword", "ClickOK"],
            "timeout": 2
        },
        "InputPassword": {
            "action": "InputText",
            "input_text": "Iapiapiap0",
            "next": ["ClickLoginConfirm", "ClickOK"]
        },
        "ClickLoginConfirm": {
            "recognition": "OCR",
            "expected": "登录",
            "action": "Click",
            "index": -1,
            "next": ["ClickOK"]
        },
        "ClickOK": {
            "recognition": "OCR",
            "expected": "好",
            "action": "Click",
            "post_wait_freezes": 400,
            "next": []
        }
    }

    foreach_pipeline = {
        "Entry2": {
            "action": "Custom",
            "custom_action": "ForEach",
            "custom_action_param": {
                "forEachList": ["1 Min", "2 Mins", "8 Mins", "20 Mins", "15 Mins", "10 Mins",
                                "3 Mins"],
                "forEachTarget": [["BuyMins", "custom_action_param", "FindMins", "custom_recognition_param", "text"]],
                "pipeline": main_pipeline,
                "flag": 0
            }
        }
    }

    login_pipeline = {
        "Entry": {
            "next": ["TryPermit", "TryLogin"]
        },
        "TryPermit": {
            "recognition": "OCR",
            "expected": "允许",
            "action": "Click",
            "index": -1,
            "next": ["TryPermit", "TryLogin"]
        },
        "TryLogin": {
            "recognition": "OCR",
            "expected": "Log In",
            "action": "Click",
            "next": ["TryGuest"]
        },
        "TryGuest": {
            "recognition": "OCR",
            "expected": "Continue with Guest",
            "action": "Click",
            "next": ["Entry2"]
        }
    }

    login_pipeline.update(foreach_pipeline)

    # 运行流水线，指定资源路径
    result = controller.run_pipeline(
        pipeline=login_pipeline,
        resource_path="../maafw_appium/resource"
    )
    print(f"任务执行结果: {result}")
