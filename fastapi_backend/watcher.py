"""后端文件监听脚本：改动关键文件后自动跑 mypy 并重建 OpenAPI。"""

# time 用于节流判断（防止短时间重复触发）。
import time
# re 用于匹配需要监听的文件路径。
import re
# subprocess 用于执行外部命令（mypy / 生成 schema）。
import subprocess
# os 用于路径处理。
import os
# Observer 是 watchdog 的监听器对象。
from watchdog.observers import Observer
# FileSystemEventHandler 是事件回调基类。
from watchdog.events import FileSystemEventHandler
# Timer 用于实现防抖（debounce）。
from threading import Timer

# 监听规则：main.py、schemas.py、以及 app/routes 下所有 Python 文件。
WATCHER_REGEX_PATTERN = re.compile(r"(main\.py|schemas\.py|routes/.*\.py)$")
# 监听目录根路径。
APP_PATH = "app"


# 自定义文件变更处理器。
class MyHandler(FileSystemEventHandler):
    # 初始化处理器状态。
    def __init__(self):
        # 调用父类初始化。
        super().__init__()
        # 防抖定时器对象（默认无）。
        self.debounce_timer = None
        # 上次触发时间戳（秒）。
        self.last_modified = 0

    # 文件被修改时触发。
    def on_modified(self, event):
        # 仅处理文件，并且文件路径满足监听规则。
        if not event.is_directory and WATCHER_REGEX_PATTERN.search(
            os.path.relpath(event.src_path, APP_PATH)
        ):
            # 获取当前时间戳。
            current_time = time.time()
            # 若距离上次触发超过 1 秒，才继续处理。
            if current_time - self.last_modified > 1:
                # 更新最近触发时间。
                self.last_modified = current_time
                # 若已存在旧定时器，先取消，避免重复执行。
                if self.debounce_timer:
                    self.debounce_timer.cancel()
                # 启动 1 秒后的防抖执行。
                self.debounce_timer = Timer(1.0, self.execute_command, [event.src_path])
                self.debounce_timer.start()

    # 防抖后实际执行的任务入口。
    def execute_command(self, file_path):
        # 打印被修改文件路径。
        print(f"File {file_path} has been modified and saved.")
        # 执行类型检查。
        self.run_mypy_checks()
        # 重新生成 OpenAPI schema。
        self.run_openapi_schema_generation()

    # 运行 mypy 类型检查。
    def run_mypy_checks(self):
        """运行 mypy 并输出结果。"""
        # 打印开始日志。
        print("Running mypy type checks...")
        # 执行命令：uv run mypy app。
        result = subprocess.run(
            ["uv", "run", "mypy", "app"],
            capture_output=True,
            text=True,
            check=False,
        )
        # 打印标准输出和错误输出。
        print(result.stdout, result.stderr, sep="\n")
        # 根据返回码打印结论。
        print(
            "Type errors detected! We recommend checking the mypy output for "
            "more information on the issues."
            if result.returncode
            else "No type errors detected."
        )

    # 运行 OpenAPI schema 生成命令。
    def run_openapi_schema_generation(self):
        """执行 OpenAPI schema 生成。"""
        # 打印开始日志。
        print("Proceeding with OpenAPI schema generation...")
        try:
            # 执行生成命令。
            subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-m",
                    "commands.generate_openapi_schema",
                ],
                check=True,
            )
            # 成功日志。
            print("OpenAPI schema generation completed successfully.")
        except subprocess.CalledProcessError as e:
            # 失败日志。
            print(f"An error occurred while generating OpenAPI schema: {e}")


# 脚本直接运行入口。
if __name__ == "__main__":
    # 创建文件系统观察者。
    observer = Observer()
    # 注册处理器，并递归监听 app 目录。
    observer.schedule(MyHandler(), APP_PATH, recursive=True)
    # 启动监听。
    observer.start()
    try:
        # 主循环保持进程常驻。
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Ctrl + C 时停止监听。
        observer.stop()
    # 等待监听线程退出。
    observer.join()
