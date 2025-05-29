import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import subprocess
import os
import traceback

class LauncherUI:
    def __init__(self, root):
        """初始化启动器界面"""
        self.root = root
        self.root.title("LauncherU")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")
        
        # 主容器
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # 程序标题
        tk.Label(main_frame, text="LauncherU", font=("Microsoft YaHei", 24, "bold"), 
                bg="#f0f0f0", fg="#333333").pack(pady=(10, 5))
        
        # 版本信息
        tk.Label(main_frame, text="版本: 2.0", font=("Microsoft YaHei", 12), 
                bg="#f0f0f0", fg="#666666").pack(pady=5)
        
        # 按钮容器
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # 启动按钮
        tk.Button(button_frame, text="启动微信多开器", command=self.start_main_program, 
                 height=2, width=20, font=("Microsoft YaHei", 12), 
                 bg="#4CAF50", fg="white", activebackground="#45a049").pack(pady=10)
        
        # 手动选择按钮
        tk.Button(button_frame, text="手动选择脚本", command=self.select_script,
                 height=2, width=20, font=("Microsoft YaHei", 12),
                 bg="#2196F3", fg="white", activebackground="#0b7dda").pack(pady=10)
        
        """tk.Button(button_frame, text="关于", command=self.About,
                 height=2, width=15, font=("Microsoft YaHei", 12),
                 bg="#28b0b4", fg="white", activebackground="#28b0b4").pack(pady=10)"""
        
    def start_main_program(self):
        """启动主程序"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), "wechat_multi_opener.py")
            subprocess.Popen(["python", script_path])
        except Exception as e:
            self.show_error_window("无法启动程序", str(e), traceback.format_exc())
            
    def select_script(self):
        """手动选择要运行的Python脚本"""
        file_path = filedialog.askopenfilename(
            title="选择Python脚本",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                subprocess.Popen(["python", file_path])
            except Exception as e:
                self.show_error_window("无法启动脚本", str(e), traceback.format_exc())

class ErrorWindow:
    """自定义错误窗口类"""
    def __init__(self, parent, title, summary, details):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("500x400")
        
        # 错误摘要
        tk.Label(self.window, text="错误摘要:", font=("Microsoft YaHei", 12, "bold")).pack(pady=(10,5), padx=10, anchor="w")
        tk.Label(self.window, text=summary, font=("Microsoft YaHei", 11), wraplength=480, justify="left").pack(padx=10, anchor="w")
        
        # 错误详情
        tk.Label(self.window, text="错误详情:", font=("Microsoft YaHei", 12, "bold")).pack(pady=(10,5), padx=10, anchor="w")
        
        # 可滚动文本框
        text_frame = tk.Frame(self.window)
        text_frame.pack(fill="both", expand=True, padx=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.details_text = scrolledtext.ScrolledText(
            text_frame, wrap="word", yscrollcommand=scrollbar.set,
            font=("Microsoft YaHei", 10), height=10
        )
        self.details_text.pack(fill="both", expand=True)
        self.details_text.insert("end", details)
        self.details_text.configure(state="disabled")
        
        # 复制按钮
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, text="复制错误信息", command=self.copy_error,
            font=("Microsoft YaHei", 10), width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame, text="关闭", command=self.window.destroy,
            font=("Microsoft YaHei", 10), width=15
        ).pack(side="left", padx=5)
    
    def copy_error(self):
        """复制错误信息到剪贴板"""
        self.window.clipboard_clear()
        self.window.clipboard_append(self.details_text.get("2.0", "end"))


if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherUI(root)
    root.mainloop()