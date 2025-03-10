from maa.define import Rect
from maa.context import Context
from maa.custom_action import CustomAction
from maa.resource import Resource
import json
from .appium_controller import AppiumController  # 新增导入

resource = Resource()


@resource.custom_action("LongPress")
class LongPressAction(CustomAction):
    """长按指定位置
    
    参数格式:
    {
        "action": "Custom",
        "custom_action": "LongPress",
        "target": [100, 100, 0, 0]
        "custom_action_param": {
            "duration": 2.0  # 长按时长(秒)
        }
    }
    
    特殊处理:
    - 使用识别框的坐标作为点击位置
    - duration 参数可选，默认为 2.0 秒
    """
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
    """识别后执行下一个任务
    
    参数格式:
    {
        "action": "Custom",
        "custom_action": "RecNext",
        "custom_action_param": {
            "Entry": {
                "action": "Click",
                "next": ["NextTask"]
            }
        }
    }
    
    特殊处理:
    - target 坐标支持特殊值：
      * -1: 使用识别框对应的值 (x, y, w, h)
      * -2: 使用设备屏幕尺寸 (x, y, w, h)
    - 支持的坐标参数：
      * target
      * target_offset
      * roi
      * roi_offset
      * begin
      * begin_offset
      * end
      * end_offset
    """
    def __init__(self, controller: AppiumController = None):  # 新增构造函数
        super().__init__()
        self.controller = controller

    def _process_box(self, rec_box: Rect, target: str, data: dict):
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
                if x == -1:
                    x = rec_box.x
                if y == -1:
                    y = rec_box.y
                if w == -1:
                    w = rec_box.w
                if h == -1:
                    h = rec_box.h
                if x == -2:
                    x = device_size[0]
                if y == -2:
                    y = device_size[1]
                if w == -2:
                    w = device_size[0]
                if h == -2:
                    h = device_size[1]
                data[target] = [
                    int(x),
                    int(y),
                    int(w),
                    int(h),
                ]

            # 递归处理字典中的其他值
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self._process_box(rec_box, target, value)
        return data

    def run(
            self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        try:
            params = json.loads(argv.custom_action_param)
            params = self._process_box(argv.box, "target", params)
            params = self._process_box(argv.box, "target_offset", params)
            params = self._process_box(argv.box, "roi", params)
            params = self._process_box(argv.box, "roi_offset", params)
            params = self._process_box(argv.box, "begin", params)
            params = self._process_box(argv.box, "begin_offset", params)
            params = self._process_box(argv.box, "end", params)
            params = self._process_box(argv.box, "end_offset", params)
            new_context = context.clone()
            pipeline = params
            result = new_context.run_task(
                "Entry",
                pipeline,
            )

            if result.status.succeeded:
                return CustomAction.RunResult(success=True)

            return CustomAction.RunResult(success=False)

        except Exception as e:
            print(f"RecNext执行失败: {e}")
            return CustomAction.RunResult(success=False)


@resource.custom_action("RatioPanel")
class RatioPanel(CustomAction):
    """按比例处理面板区域
    
    参数格式:
    {
        "action": "Custom",
        "custom_action": "RatioPanel",
        "custom_action_param": {
            "Entry": {
                "action": "Click",
                "target": [0.5, 0.5, 0.8, 0.8]
            }
        }
    }
    
    特殊处理:
    - 坐标值支持 0-1 之间的比例：
      * x, y: 相对于屏幕宽高的比例位置
      * w, h: 相对于屏幕宽高的比例尺寸
    - 支持的坐标参数：
      * target
      * target_offset
      * roi
      * roi_offset
      * begin
      * begin_offset
      * end
      * end_offset
    """
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
                if 1 < x < 0:
                    x = int(x * device_size[0])
                if 0 < y < 1:
                    y = int(y * device_size[1])
                if 0 < w < 1:
                    w = int(w * device_size[0])
                if 0 < h < 1:
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
    """执行返回操作
    
    参数格式:
    {
        "action": "Custom",
        "custom_action": "AppBack",
        “next”: []
    }
    
    特殊处理:
    - 无需坐标参数
    - 直接调用系统返回功能
    - next 参数可选，支持链式任务执行
    """
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
