import os
import threading
import time

from utils import get_company_list
from utils import get_company_info
from utils import get_file_list
from utils import get_average_list
from logs import make_log
from zip_file import create_zip

import test

send_over = False


def compress_thread(file_list, database, dest_host, dest_disk):
    try:
        make_log("INFO", "开始压缩文件：" + database)

        create_zip(file_list, database, dest_host, dest_disk)

        make_log("INFO", "文件压缩完毕：" + database)

    except Exception as e:
        print(e)


# 获取该类已开启的线程数；
def thread_nums(name='compress'):
    thread_list = [thread for thread in threading.enumerate()
                   if thread.getName().startswith(name)]

    return len(thread_list)


def compress(file_dir):
    try:

        # 第一步，得到公司列表；
        # company_list = get_company_list(file_dir)
        company_list = test.init()

        # 第二步，获取发送分配信息；
        company_list = get_company_info(company_list)

        for company in company_list:

            new_compress_thread = threading.Thread(target=compress_thread,
                                                   args=(company.file_list, company.company,
                                                         company.dest_host, company.dest_disk),
                                                   name="compress")
            new_compress_thread.start()

        global send_over
        while True:
            time.sleep(5)
            if thread_nums("compress") == 0:
                print("所有文件压缩完毕")
                send_over = True
                break

    except Exception as e:
        print(e)

