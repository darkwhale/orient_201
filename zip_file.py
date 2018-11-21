import zipfile
import os
import time

from mask import read_mask
from mask import write_mask
from process_bar import process_bar

batch_size = "1M"
zip_dir = "zips"

# 创建zips文件夹；
if not os.path.exists(zip_dir):
    os.mkdir(zip_dir)


# 清除zips文件夹下临时文件；
def clear():
    for file in os.listdir(zip_dir):
        if file.startswith('tmp'):
            os.remove(os.path.join(zip_dir, file))


# 标准化块大小到字节；
def decode_batch_size(batch_str):
    if batch_str.endswith("K"):
        return int(batch_str[:-1])*1024

    if batch_str.endswith("M"):
        return int(batch_str[:-1])*1024*1024

    if batch_str.endswith("G"):
        return int(batch_str[:-1])*1024*1024*1024


"""
创建压缩文件
压缩文件名：第一位表示要发送的主机号，第二位表示要存储的磁盘号，第三位表示是否为该压缩批次的最后一个文件；
后续为公司名，时间戳；
"""


def create_zip(file_list, database, dest_host):

    # file_index记录了下一个需要压缩的文件；
    file_index = read_mask(dest_host + database)

    new_file_list = file_list[file_index:]

    for index, file in enumerate(new_file_list):
        process_bar(float(index) / len(new_file_list))

        if index == 0:
            old_zip_file_name = os.path.join(zip_dir, "tmp" + dest_host + database + str(time.time()) + '.zip')
            part_zip = zipfile.ZipFile(old_zip_file_name,
                                       'w', zipfile.ZIP_DEFLATED)

        part_zip.write(file, os.path.basename(os.path.dirname(file)) + os.path.basename(file))

        if os.path.getsize(part_zip.filename) >= decode_batch_size(batch_size) \
                or index + 1 == len(new_file_list):

            # 关闭旧的zip对象；
            part_zip.close()

            # 压缩完毕重命名文件，表示压缩完毕，可以进行传输，并删除原文件；
            # 注意，该语句需要放置在上一句后面，避免windows上的文件保护；
            write_mask(dest_host + database, index + 1)

            os.rename(old_zip_file_name, old_zip_file_name[:5] + old_zip_file_name[8:])

            # 当不为最后一个文件时，创建新的压缩文件；
            if index + 1 != len(new_file_list):

                old_zip_file_name = os.path.join(zip_dir, "tmp" + dest_host + database + str(time.time()) + '.zip')
                part_zip = zipfile.ZipFile(old_zip_file_name, 'w', zipfile.ZIP_DEFLATED)

    process_bar(1)

