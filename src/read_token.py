import os
import tomllib

def get_token():
    """从本地toml文件中获取gm token"""
    # project_path = os.path.dirname(os.getcwd())
    project_path = os.getcwd()
    if project_path.split('\\')[-1] == 'src':
        project_path = os.path.dirname(project_path)
    config_path = os.path.join(project_path, 'config.toml')  # 生成绝对路径
    # 确保文件存在
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config 文件未找到: {config_path}")
    with open(config_path, 'br') as f:
        secret = tomllib.load(f)
    return secret['gm']['token'].get('token')

if __name__ == '__main__':
    print(get_token())
