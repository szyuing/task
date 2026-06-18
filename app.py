import os
import sys
import json

try:
    import webview
except ImportError:
    print("错误：缺少 pywebview 依赖")
    print("请先执行：pip install -r requirements.txt")
    input("按回车键退出...")
    sys.exit(1)

def close_window():
    """关闭窗口"""
    if webview.windows:
        webview.windows[0].destroy()

def minimize_window():
    """最小化窗口"""
    if webview.windows:
        webview.windows[0].minimize()

def toggle_on_top():
    """切换置顶状态，返回当前是否置顶"""
    if webview.windows:
        win = webview.windows[0]
        win.on_top = not win.on_top
        return win.on_top
    return False


# ==================== 本地文件存储（JSON） ====================
def get_tasks_file():
    """获取任务 JSON 文件路径（Windows AppData 目录，更可靠）"""
    appdata = os.environ.get('APPDATA') or os.path.expanduser('~')
    data_dir = os.path.join(appdata, '任务计划')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'tasks.json')


def load_tasks():
    """从本地 JSON 文件加载任务，返回列表或 None（给 JS 调用）"""
    path = get_tasks_file()
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else None
    except Exception as e:
        print(f"加载任务失败: {e}")
        return None


def save_tasks(tasks):
    """将任务列表保存到本地 JSON 文件，返回是否成功（给 JS 调用）"""
    path = get_tasks_file()
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存任务失败: {e}")
        return False

def create_app():
    # 确保能找到 index.html
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, 'index.html')
    
    if not os.path.exists(html_path):
        print("错误：找不到 index.html")
        input("按回车键退出...")
        sys.exit(1)
    
    window = webview.create_window(
        title='任务计划',
        url=html_path,
        width=360,
        height=530,
        min_size=(300, 400),
        resizable=True,
        frameless=True,
        on_top=True,
        easy_drag=False,          # 使用 pywebview-drag-region 指定的拖拽区
        text_select=True,
        background_color='#f8fafc',
    )
    
    # 暴露 Python 函数给 JavaScript 调用
    window.expose(close_window)
    window.expose(minimize_window)
    window.expose(toggle_on_top)
    window.expose(load_tasks)
    window.expose(save_tasks)
    
    # debug=False 上线用，开发时可改为 True 右键菜单检查元素
    webview.start(debug=False)

if __name__ == '__main__':
    create_app()
