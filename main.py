"""
总文件，压缩文件，传输文件；
目前测试的python3直接ctrl+c即可退出所有进程和线程，
所谓的端口占用是tcp的保护机制，等待2分钟即可；
"""

from transport import transport
from compress import compress
from logs import make_log
from zip_file import clear
from mask import clear_mask
from mask import is_last_file
from mask import write_last_file

import threading
import sys
import os


if __name__ == '__main__':

    # 清除上次未完成的临时文件；
    clear()

    file_dir = sys.argv[1]

    if not os.path.exists(file_dir):
        print("文件不存在")
        exit(1)

    # 判断是否是继续上次的工作；
    if not is_last_file(os.path.abspath(file_dir)):
        clear_mask()
        write_last_file(os.path.abspath(file_dir))

    # 开启压缩数据线程，用于压缩数据；
    compress_thread = threading.Thread(target=compress, args=(file_dir, ))
    compress_thread.start()
    make_log("INFO", "数据压缩进程已启动，准备压缩数据")

    # 开启传输数据线程，用于传输数据；
    transport_thread = threading.Thread(target=transport, args=(5,))
    transport_thread.start()
    make_log("INFO", "数据传输进程已启动")
