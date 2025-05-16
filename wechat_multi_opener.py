import tkinter as tk
from tkinter import filedialog
import subprocess
from tqdm.tk import tqdm
import time
import os
import configparser

Bar=tqdm(total=100)

class LanguageManager:
    """语言管理器类，负责处理多语言配置"""
    
    def __init__(self):
        """初始化语言管理器"""
        self.config = configparser.ConfigParser()  # 配置文件解析器
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')  # 数据目录路径
        self.config_path = os.path.join(self.data_dir, 'Language_Config.ini')  # 配置文件路径
        self.current_lang = 'zh'  # 默认语言为中文
        self.load_config()  # 加载配置

    def load_config(self):
        """加载语言配置文件"""
        if os.path.exists(self.config_path):
            # 如果配置文件存在，读取配置
            self.config.read(self.config_path, encoding='utf-8')
            self.current_lang = self.config.get('DEFAULT', 'language', fallback='zh')
        else:
            # 如果配置文件不存在，创建数据目录
            os.makedirs(self.data_dir, exist_ok=True)

    def save_config(self):
        """保存当前语言配置"""
        self.config.set('DEFAULT', 'language', self.current_lang)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def get_text(self, key):
        """根据key获取当前语言的文本"""
        return self.config.get(self.current_lang, key, fallback=key)

    def toggle_language(self):
        """切换当前语言(中/英)"""
        self.current_lang = 'en' if self.current_lang == 'zh' else 'zh'
        self.save_config()  # 保存切换后的语言设置

def startqdm():
    """启动进度条显示"""
    lang_mgr = LanguageManager()  # 创建语言管理器实例
    
    # 模拟加载文件进度
    Bar.set_description(lang_mgr.get_text('loading_file'))
    for i in range(3):
        time.sleep(1)
        Bar.update(10)
    
    # 模拟加载源码进度
    Bar.set_description(lang_mgr.get_text('loading_source'))
    for i in range(3):
        time.sleep(1)
        Bar.update(10)
    
    # 模拟编译进度
    Bar.set_description(lang_mgr.get_text('compiling'))
    for i in range(3):
        time.sleep(1)
        Bar.update(10)
    
    # 模拟启动进度
    Bar.set_description(lang_mgr.get_text('starting'))
    time.sleep(1)
    Bar.update(10)
    Bar.close()  # 关闭进度条

class WeChatMultiOpener:
    def __init__(self, root):
        """初始化微信多开器界面"""
        self.root = root  # 主窗口对象
        self.lang_mgr = LanguageManager()  # 语言管理器实例
        self.update_ui_text()  # 更新界面文本

        # 创建界面变量
        self.wechat_path = tk.StringVar()  # 存储微信路径的字符串变量
        self.count = tk.IntVar(value=1)  # 存储多开数量的整型变量，默认值为1

        # 微信路径选择组件
        # 路径标签
        tk.Label(root, text=self.lang_mgr.get_text('wechat_path_label')).grid(row=0, column=0, padx=10, pady=5)
        # 路径输入框
        tk.Entry(root, textvariable=self.wechat_path, width=40).grid(row=0, column=1, padx=10, pady=5)
        # 路径选择按钮
        tk.Button(root, text=self.lang_mgr.get_text('select_path_button'), command=self.select_path).grid(row=0, column=2, padx=10, pady=5)

        # 多开数量输入组件
        # 数量标签
        tk.Label(root, text=self.lang_mgr.get_text('count_label')).grid(row=1, column=0, padx=10, pady=5)
        # 数量输入框
        tk.Entry(root, textvariable=self.count, width=10).grid(row=1, column=1, padx=10, pady=5)

        # 多开按钮
        tk.Button(root, text=self.lang_mgr.get_text('start_button'), command=self.open_wechat).grid(row=2, column=1, padx=10, pady=20)

        # 语言切换按钮
        tk.Button(root, text='中/En', command=self.toggle_language).grid(row=2, column=2, padx=10, pady=20)

        # 刷新所有标签文本
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                # 更新路径标签文本
                if '微信主程序路径' in widget.cget('text') or 'WeChat Program Path' in widget.cget('text'):
                    widget.config(text=self.lang_mgr.get_text('wechat_path_label'))
                # 更新数量标签文本
                elif '多开数量' in widget.cget('text') or 'Instance Count' in widget.cget('text'):
                    widget.config(text=self.lang_mgr.get_text('count_label'))
            elif isinstance(widget, tk.Button):
                # 更新路径选择按钮文本
                if '选择路径' in widget.cget('text') or 'Select Path' in widget.cget('text'):
                    widget.config(text=self.lang_mgr.get_text('select_path_button'))
                # 更新开始按钮文本
                elif '开始多开' in widget.cget('text') or 'Start' in widget.cget('text'):
                    widget.config(text=self.lang_mgr.get_text('start_button'))

    def select_path(self):
        path = filedialog.askopenfilename(filetypes=[('可执行文件', '*.exe')])
        if path:
            self.wechat_path.set(path)

    def toggle_language(self):
        """切换语言"""
        self.lang_mgr.toggle_language()
        self.update_ui_text()
        
    def update_ui_text(self):
        """更新界面文本"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                if '微信主程序路径' in widget.cget('text') or 'WeChat Program Path' in widget.cget('text'):
                    widget.config(text=self.lang_mgr.get_text('wechat_path_label'))
                elif '多开数量' in widget.cget('text') or 'Instance Count' in widget.cget('text'):
                    widget.config(text=self.lang_mgr.get_text('count_label'))
            elif isinstance(widget, tk.Button):
                if '选择路径' in widget.cget('text') or 'Select Path' in widget.cget('text'):
                    widget.config(text=self.lang_mgr.get_text('select_path_button'))
                elif '开始多开' in widget.cget('text') or 'Start' in widget.cget('text'):
                    widget.config(text=self.lang_mgr.get_text('start_button'))

    def open_wechat(self):
        wechat_path = self.wechat_path.get()
        count = self.count.get()
        if wechat_path:
            for _ in range(count):
                try:
                    subprocess.Popen([wechat_path])
                except Exception as e:
                    print(self.lang_mgr.get_text('error_msg').format(e))

def check_and_create_config():
    """检查并创建语言配置文件"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')  # 数据目录路径
    config_path = os.path.join(data_dir, 'Language_Config.ini')  # 配置文件路径
    
    # 如果数据目录不存在则创建
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 如果配置文件不存在则创建默认配置
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'language': 'zh'}  # 默认语言设置
        
        # 中文配置
        config['zh'] = {
            'title': '微信多开器',
            'wechat_path_label': '微信主程序路径:',
            'select_path_button': '选择路径',
            'count_label': '多开数量:',
            'start_button': '开始多开',
            'loading_file': '加载文件中',
            'loading_source': '加载源码中',
            'compiling': '编译文件中',
            'starting': '启动文件中',
            'error_msg': '打开微信时出错: {}'
        }
        
        # 英文配置
        config['en'] = {
            'title': 'WeChat Multi Opener',
            'wechat_path_label': 'WeChat Program Path:',
            'select_path_button': 'Select Path',
            'count_label': 'Instance Count:',
            'start_button': 'Start',
            'loading_file': 'Loading Files',
            'loading_source': 'Loading Source Code',
            'compiling': 'Compiling',
            'starting': 'Starting',
            'error_msg': 'Error opening WeChat: {}'
        }
        
        # 写入配置文件
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)

if __name__ == '__main__':
    check_and_create_config()
    startqdm()
    root = tk.Tk()
    app = WeChatMultiOpener(root)
    root.mainloop()