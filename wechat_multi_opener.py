import tkinter as tk
from tkinter import filedialog
import subprocess
from tqdm.tk import tqdm
import time
import os
import configparser

Bar=tqdm(total=100)

class LanguageManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.config_path = os.path.join(self.data_dir, 'Language_Config.txt')
        self.current_lang = 'zh'
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            self.config.read(self.config_path, encoding='utf-8')
            self.current_lang = self.config.get('DEFAULT', 'language', fallback='zh')
        else:
            os.makedirs(self.data_dir, exist_ok=True)

    def save_config(self):
        self.config.set('DEFAULT', 'language', self.current_lang)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def get_text(self, key):
        return self.config.get(self.current_lang, key, fallback=key)

    def toggle_language(self):
        self.current_lang = 'en' if self.current_lang == 'zh' else 'zh'
        self.save_config()

def startqdm():
    lang_mgr = LanguageManager()
    Bar.set_description(lang_mgr.get_text('loading_file'))
    for i in range(3):
        time.sleep(1)
        Bar.update(10)
    Bar.set_description(lang_mgr.get_text('loading_source'))
    for i in range(3):
        time.sleep(1)
        Bar.update(10)
    Bar.set_description(lang_mgr.get_text('compiling'))
    for i in range(3):
        time.sleep(1)
        Bar.update(10)
    Bar.set_description(lang_mgr.get_text('starting'))
    time.sleep(1)
    Bar.update(10)
    Bar.close()

class WeChatMultiOpener:
    def __init__(self, root):
        self.root = root
        self.lang_mgr = LanguageManager()
        self.update_ui_text()

        self.wechat_path = tk.StringVar()
        self.count = tk.IntVar(value=1)

        # 微信路径选择
        tk.Label(root, text=self.lang_mgr.get_text('wechat_path_label')).grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.wechat_path, width=40).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text=self.lang_mgr.get_text('select_path_button'), command=self.select_path).grid(row=0, column=2, padx=10, pady=5)

        # 多开数量输入
        tk.Label(root, text=self.lang_mgr.get_text('count_label')).grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.count, width=10).grid(row=1, column=1, padx=10, pady=5)

        # 多开按钮
        tk.Button(root, text=self.lang_mgr.get_text('start_button'), command=self.open_wechat).grid(row=2, column=1, padx=10, pady=20)

        # 语言切换按钮
        tk.Button(root, text='中/En', command=self.toggle_language).grid(row=2, column=2, padx=10, pady=20)

    def update_ui_text(self):
        self.root.title(self.lang_mgr.get_text('title'))

    def toggle_language(self):
        self.lang_mgr.toggle_language()
        self.update_ui_text()
        # 刷新所有标签文本
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

    def select_path(self):
        path = filedialog.askopenfilename(filetypes=[('可执行文件', '*.exe')])
        if path:
            self.wechat_path.set(path)

    def open_wechat(self):
        wechat_path = self.wechat_path.get()
        count = self.count.get()
        if wechat_path:
            for _ in range(count):
                try:
                    subprocess.Popen([wechat_path])
                except Exception as e:
                    print(self.lang_mgr.get_text('error_msg').format(e))

if __name__ == '__main__':
    startqdm()
    root = tk.Tk()
    app = WeChatMultiOpener(root)
    root.mainloop()