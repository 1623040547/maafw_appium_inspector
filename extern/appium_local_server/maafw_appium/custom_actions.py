from maa.context import Context
from maa.custom_action import CustomAction
from maa.resource import Resource
import json
from .appium_controller import AppiumController  # 新增导入

resource = Resource()


@resource.custom_action("LongPress")
class LongPressAction(CustomAction):
    def __init__(self, controller: AppiumController = None):  # 新增构造函数
        super().__init__()
        self.controller = controller

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        try:
            # 获取参数
            x = argv.box.x
            y = argv.box.y
            params = json.loads(argv.custom_action_param)
            duration = params.get("duration", 2.0)

            print(f"执行长按动作: 坐标({x}, {y}), 时长{duration}秒")

            success = self.controller.long_click(x, y, duration)
            # 使用传入的 controller 或 context 中的 controller

            return CustomAction.RunResult(success=success)

        except Exception as e:
            print(f"长按动作执行失败: {e}")
            return CustomAction.RunResult(success=False)


@resource.custom_action("RecNext")
class RecNext(CustomAction):
    def __init__(self, controller: AppiumController = None):  # 新增构造函数
        super().__init__()
        self.controller = controller

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        try:
            # 获取参数
            x = argv.box.x
            y = argv.box.y
            width = argv.box.w
            height = argv.box.h
            params = json.loads(argv.custom_action_param)
            findRow = params.get("row", True)
            findColumn = params.get("column", False)
            expected = params.get("expected", "")
            recognition = params.get("recognition", "OCR")
            action = params.get("action", "Click")
            next = params.get("next", [])
            padding = params.get("padding", 0)
            more = params.get("more", {})

            new_context = context.clone()

            device_size = self.controller.device_size()

            pipeline = {}
            pipeline.update(
                {
                    "recognition": recognition,
                    "expected": expected,
                    "action": action,
                    "padding": padding,
                    "next": next,
                }
            )

            if findRow:
                pipeline.update({"roi": [x, y, device_size[0], height + padding]})
                pipeline.update(more)
                result = new_context.run_task(
                    "RecNext",
                    {"RecNext": pipeline},
                )

                if result.status.succeeded:
                    return CustomAction.RunResult(success=True)

            if findColumn:
                pipeline.update({"roi": [x, y, width + padding, device_size[1]]})
                pipeline.update(more)
                new_context.run_task(
                    "RecNext",
                    {"RecNext": pipeline},
                )
                if result.status.succeeded:
                    return CustomAction.RunResult(success=True)

            return CustomAction.RunResult(success=False)

        except Exception as e:
            print(f"RecNext执行失败: {e}")
            return CustomAction.RunResult(success=False)


@resource.custom_action("RatioPanel")
class RatioPanel(CustomAction):
    def __init__(self, controller: AppiumController = None):  # 新增构造函数
        super().__init__()
        self.controller = controller

    def _process_xy(self, target: str, data: dict):
        """递归处理所有层级的 target 参数"""
        # 处理字典中的 target
        if data.__contains__(target):
            # 这里添加对 target 的处理逻辑
            device_size = self.controller.device_size()
            if isinstance(data[target], list):
                x = data[target][0]
                y = data[target][1]
                w = data[target][2]
                h = data[target][3]
                if x < 1:
                    x = int(x * device_size[0])
                if y < 1:
                    y = int(y * device_size[1])
                if w < 1:
                    w = int(w * device_size[0])
                if h < 1:
                    h = int(h * device_size[1])
                data[target] = [
                    int(x),
                    int(y),
                    int(w),
                    int(h),
                ]

            # 递归处理字典中的其他值
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self._process_xy(target, value)
        return data

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        try:
            params = json.loads(argv.custom_action_param)
            params = self._process_xy("target", params)
            params = self._process_xy("target_offset", params)
            params = self._process_xy("roi", params)
            params = self._process_xy("roi_offset", params)
            params = self._process_xy("begin", params)
            params = self._process_xy("begin_offset", params)
            params = self._process_xy("end", params)
            params = self._process_xy("end_offset", params)
            new_context = context.clone()
            result = new_context.run_task("Entry", params)
            if result.status.succeeded:
                return CustomAction.RunResult(success=True)
            return CustomAction.RunResult(success=False)
        except Exception as e:
            print(f"RecNext执行失败: {e}")
            return CustomAction.RunResult(success=False)


@resource.custom_action("AppBack")
class AppBack(CustomAction):
    def __init__(self, controller: AppiumController = None):  # 新增构造函数
        super().__init__()
        self.controller = controller

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        try:
            self.controller.app_back()
            return CustomAction.RunResult(success=True)
        except Exception as e:
            print(f"长按动作执行失败: {e}")
            return CustomAction.RunResult(success=False)
