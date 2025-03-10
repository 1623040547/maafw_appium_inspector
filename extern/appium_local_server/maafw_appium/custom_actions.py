from maa.define import Rect
from maa.context import Context
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition
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
      * 10001: 使用识别框对应的x值
      * 10002: 使用识别框对应的y值
      * 10003: 使用识别框对应的w值
      * 10004: 使用识别框对应的h值
      * 20003: 使用设备屏幕对应的w值
      * 20004: 使用设备屏幕对应的h值
      * -10001: 使用识别框对应的值-x值
      * -10002: 使用识别框对应的-y值
      * -10003: 使用识别框对应的-w值
      * -10004: 使用识别框对应的-h值
      * -20003: 使用设备屏幕对应的-w值
      * -20004: 使用设备屏幕对应的-h值
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

    def _process_code(self, code: int, rec_box: Rect):
        device_size = self.controller.device_size()
        if code == 10001:
            return rec_box.x
        if code == 10002:
            return rec_box.y
        if code == 10003:
            return rec_box.w
        if code == 10004:
            return rec_box.h
        if code == 20003:
            return device_size[0]
        if code == 20004:
            return device_size[1]
        if code == -10001:
            return -rec_box.x
        if code == -10002:
            return -rec_box.y
        if code == -10003:
            return -rec_box.w
        if code == -10004:
            return -rec_box.h
        if code == -20003:
            return -device_size[0]
        if code == -20004:
            return -device_size[1]
        return code

    def _process_box(self, rec_box: Rect, target: str, data: dict):
        """递归处理所有层级的 target 参数"""
        # 处理字典中的 target
        if data.__contains__(target):
            if isinstance(data[target], list):
                x = self._process_code(data[target][0], rec_box)
                y = self._process_code(data[target][1], rec_box)
                w = self._process_code(data[target][2], rec_box)
                h = self._process_code(data[target][3], rec_box)
                print(f"target {target} {x} {y} {w} {h}")
                data[target] = [
                    int(x),
                    int(y),
                    int(w),
                    int(h),
                ]

            # 递归处理字典中的其他值
        for key, value in data.items():
            if isinstance(value, dict):
                if data.get("custom_action", "") == "RecNext" and key == "custom_action_param":
                    continue
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
            print(f"返回动作执行失败: {e}")
            return CustomAction.RunResult(success=False)


@resource.custom_action("ForEach")
class ForEach(CustomAction):
    """遍历执行任务列表
    
    参数格式:
    {
        "action": "Custom",
        "custom_action": "ForEach",
        "custom_action_param": {
            "forEachList": ["item1", "item2", "item3"],  # 要遍历的列表
            "forEachTarget": [["Entry", "target"], ["Entry", "roi"]],  # 要替换的目标路径
            "pipeline": {  # 要执行的任务流水线
                "Entry": {
                    "target": "placeholder",  # 将被 forEachList 中的值替换
                    "roi": "placeholder"
                }
            },
            "flag": 0  # 可选，执行结果判断标志，0:全部成功才算成功，1:有一个成功就算成功，默认为0
        }
    }
    
    特殊处理:
    - forEachList: 遍历执行的数据列表
    - forEachTarget: 指定要替换的目标路径，支持多层嵌套
    - pipeline: 要执行的任务流水线
    - flag: 执行结果判断标志
      * 0: 所有任务都成功才返回成功（AND）
      * 1: 任意任务成功就返回成功（OR）
    
    示例:
    {
        "action": "Custom",
        "custom_action": "ForEach",
        "custom_action_param": {
            "forEachList": ["A", "B", "C"],
            "forEachTarget": [["Entry", "recognition", "text"]],
            "pipeline": {
                "Entry": {
                    "recognition": {
                        "text": "placeholder"
                    },
                    "action": "Click"
                }
            }
        }
    }
    """

    def __init__(self, controller: AppiumController = None):  # 新增构造函数
        super().__init__()
        self.controller = controller

    def _process_pipeline(self, pipeline: dict, targets: list[list], replaceVal):
        for target in targets:
            print(f"for-each 8 {target} {replaceVal}")
            last = pipeline
            last2 = None
            last2val = None
            for val in list(target):
                last2 = last
                last2val = val
                last = last[val]
            last2[last2val] = replaceVal
        return pipeline

    def run(
            self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        try:
            params = json.loads(argv.custom_action_param)
            forEachList: list = params.get("forEachList")
            forEachTarget: list[list] = params.get("forEachTarget")
            pipeline: dict = params.get("pipeline")
            flag = params.get("flag", 0)
            result: bool
            if flag == 0:
                result = True
            else:
                result = False
            for item in forEachList:
                new_context = context.clone()
                pipeline = self._process_pipeline(pipeline, forEachTarget, item)
                print(f"for-each pipeline: {pipeline}")
                r1 = new_context.run_task("Entry", pipeline)
                if flag == 0:
                    result &= r1.status.succeeded
                else:
                    result |= r1.status.succeeded
            return CustomAction.RunResult(success=True)
        except Exception as e:
            print(f"for-each执行失败: {e}")
            return CustomAction.RunResult(success=False)


@resource.custom_recognition("FindText")
class FindText(CustomRecognition):
    """使用文本查找进行识别
    参数格式:
    {
        "recognition": "Custom",
        "custom_recognition": "FindText",
        "custom_recognition_param": {
            "text": "要查找的文本",
            "index": 0  # 可选，指定使用第几个匹配的元素，默认0表示第一个
                   # 负数表示从后往前数，如 -1 表示最后一个
        }
    }
    """

    def __init__(self, controller: AppiumController = None):
        super().__init__()
        self.controller = controller

    def analyze(
            self,
            context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        try:
            # 获取参数
            params = json.loads(argv.custom_recognition_param)
            text = params.get("text", "")
            index = params.get("index", 0)

            print(f"识别文本: {text}, 索引: {index}, ROI: {argv.roi}")

            # 使用 controller 查找元素
            positions = self.controller.find_element_by_text(text)
            valid_positions = []

            # 过滤出在 ROI 内的元素
            for pos in positions:
                x, y, w, h = pos
                # 检查元素中心点是否在 ROI 内
                center_x = x + w / 2
                center_y = y + h / 2
                if (argv.roi.x <= center_x <= argv.roi.x + argv.roi.w and
                        argv.roi.y <= center_y <= argv.roi.y + argv.roi.h):
                    valid_positions.append(pos)

            if valid_positions:
                # 处理负数索引
                if index < 0:
                    index = len(valid_positions) + index

                # 检查索引是否有效
                if 0 <= index < len(valid_positions):
                    x, y, w, h = valid_positions[index]
                    return CustomRecognition.AnalyzeResult(
                        box=(x, y, w, h),
                        detail=f"Found text '{text}' at index {index} in ROI"
                    )

            return CustomRecognition.AnalyzeResult(
                box=None,
                detail=f"Text '{text}' not found in ROI"
            )

        except Exception as e:
            print(f"文本识别失败: {e}")
            return CustomRecognition.AnalyzeResult(
                box=None,
                detail=f"Recognition failed: {str(e)}"
            )
