import os


def setup_resource_structure():
    """设置资源目录结构"""
    base_path = os.path.dirname(os.path.abspath(__file__))

    # 创建资源目录结构
    directories = [
        "resource",
        "resource/image",
        "resource/model",
        "resource/pipeline"
    ]

    for dir_path in directories:
        full_path = os.path.join(base_path, dir_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"创建目录: {full_path}")

    # 创建必要的配置文件
    config_files = {
        "resource/default_pipeline.json": """{
        "Default": {
            "rate_limit": 2000
        },
        "TemplateMatch": {
            "recognition": "TemplateMatch",
            "threshold": 0.7
        }
    }"""
    }

    for file_path, content in config_files.items():
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"创建配置文件: {full_path}")


if __name__ == "__main__":
    print("开始检查资源目录结构...")
    setup_resource_structure()
    print("资源目录结构检查完成")
