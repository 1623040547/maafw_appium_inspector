import os
from typing import Optional

from flask import Flask, request, jsonify

from flask_sock import Sock
import base64
import cv2
import time
import json
from maa.tasker import Tasker
from maa.resource import Resource
from maafw_appium.appium_ios_controller import AppiumIOSController

app = Flask(__name__)
sock = Sock(app)

# 从环境变量获取端口
port = int(os.environ.get('FLASK_PORT', 5000))

# 全局实例
# 添加会话状态标志
controller: Optional[AppiumIOSController] = None
tasker: Optional[Tasker] = None
resource: Optional[Resource] = None
session_active = False


@app.route('/init', methods=['POST'])
def init_controller():
    global controller, tasker, resource, session_active
    try:
        data = request.json
        capabilities = data.get('capabilities', {})
        server_url = data.get('server_url', 'http://127.0.0.1:4723')

        # 如果已存在会话，先清理
        reset_controller()

        controller = AppiumIOSController(
            capabilities=capabilities,
            server_url=server_url
        )

        # 初始化并连接控制器
        if not controller.connect():
            reset_controller()
            return jsonify({"status": "error", "message": "控制器连接失败"})

        # 验证会话是否成功创建
        try:
            controller.driver.session_id
            session_active = True
        except Exception as e:
            reset_controller()
            return jsonify({"status": "error", "message": f"会话创建失败: {str(e)}"})

        # 初始化资源
        resource = Resource()
        resource.use_cpu()

        # 初始化任务管理器
        tasker = Tasker()

        # 绑定资源和控制器
        if not tasker.bind(resource, controller):
            return jsonify({"status": "error", "message": "任务管理器绑定失败"})

        return jsonify({"status": "success"})
    except Exception as e:
        session_active = False
        reset_controller()
        return jsonify({"status": "error", "message": str(e)})


@sock.route('/screen')
def screen_stream(ws):
    global controller, tasker, session_active
    try:
        while True:
            if controller and tasker and session_active:
                try:
                    screen = None
                    # 检查会话状态并尝试重连
                    try:
                        if not controller.driver.session_id:
                            if not controller.connect():
                                session_active = False
                                raise Exception("会话重连失败")
                    except:
                        session_active = False
                        reset_controller()
                        raise Exception("会话已断开")
                except Exception as e:
                    print(f"Failed to get cached image: {e}")
                    continue

                if screen is None and controller:
                    try:
                        screen = controller.screencap()
                    except Exception as e:
                        session_active = False
                        reset_controller()
                        print(f"截图失败，会话可能已断开: {e}")
                        continue

                if screen is not None:
                    # 将图像编码为JPEG格式
                    _, buffer = cv2.imencode('.jpg', screen)
                    # 转换为base64字符串
                    base64_image = base64.b64encode(buffer).decode('utf-8')
                    # 发送给客户端
                    ws.send(json.dumps({
                        'type': 'screen',
                        'data': base64_image
                    }))
            time.sleep(0.5)  # 控制刷新率
    except Exception as e:
        print(f"WebSocket error: {e}")
        session_active = False


def reset_controller():
    global controller, tasker, resource, session_active
    if controller:
        try:
            if hasattr(controller, 'driver') and controller.driver:
                controller.driver.quit()
        except:
            pass
    controller = None
    tasker = None
    resource = None
    session_active = False


@app.route('/action/tap', methods=['POST'])
def handle_tap():
    global controller, session_active
    try:
        if not controller or not session_active:
            return jsonify({"status": "error", "message": "控制器未初始化"})

        data = request.json
        x = data.get('x', 0)
        y = data.get('y', 0)

        # 使用 click 方法替代 tap
        success = controller.click(int(x), int(y))
        if not success:
            return jsonify({"status": "error", "message": "点击操作失败"})
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/action/swipe', methods=['POST'])
def handle_swipe():
    global controller, session_active
    try:
        if not controller or not session_active:
            return jsonify({"status": "error", "message": "控制器未初始化"})

        data = request.json
        start_x = data.get('startX', 0)
        start_y = data.get('startY', 0)
        end_x = data.get('endX', 0)
        end_y = data.get('endY', 0)
        duration = data.get('duration', 0.5)

        # 转换为整数并将秒转为毫秒
        success = controller.swipe(
            int(start_x),
            int(start_y),
            int(end_x),
            int(end_y),
            int(duration * 1000)
        )
        if not success:
            return jsonify({"status": "error", "message": "滑动操作失败"})
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/action/long_press', methods=['POST'])
def handle_long_press():
    global controller, session_active
    try:
        if not controller or not session_active:
            return jsonify({"status": "error", "message": "控制器未初始化"})

        data = request.json
        x = data.get('x', 0)
        y = data.get('y', 0)
        duration = data.get('duration', 1.0)

        success = controller.long_click(x, y, duration)

        if not success:
            return jsonify({"status": "error", "message": "长按操作失败"})
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/screen_info', methods=['GET'])
def get_screen_info():
    global controller, session_active
    try:
        if not controller or not session_active:
            return jsonify({"status": "error", "message": "控制器未初始化"})

        return jsonify({
            "status": "success",
            "data": {
                "width": controller.device_width,
                "height": controller.device_height
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port)
