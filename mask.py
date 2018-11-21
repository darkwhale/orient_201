import os
import threading

file_lock = threading.Lock()

# mask_file记录每次发送过程中的文件进度，mask_new_file记录上次完成的数据；
mask_file = 'mask/mask'
last_file = 'mask/file'

if not os.path.exists(os.path.dirname(mask_file)):
    os.mkdir(os.path.dirname(mask_file))

if not os.path.exists(mask_file):
    with open(mask_file, 'w') as creator:
        pass

if not os.path.exists(last_file):
    with open(last_file, 'w') as creator:
        pass


# 清空记录文件；
def clear_mask():
    with open(mask_file, 'w') as creator:
        pass


# 写文件;
def write_mask(mask_index, mask_symbol):
    # 上锁，多线程同步；
    file_lock.acquire()
    with open(mask_file, 'r') as reader:
        mask_lines = reader.readlines()

    mask_dict = {}

    for mask_line in mask_lines:
        mask_line = mask_line.strip()
        database, index = mask_line.split()
        mask_dict[database] = index

    mask_dict[mask_index] = str(mask_symbol)

    new_mask_lines = []

    for key, value in mask_dict.items():
        new_mask_line = key + ' ' + value + '\n'
        new_mask_lines.append(new_mask_line)

    with open(mask_file, 'w') as writer:
        writer.write(''.join(new_mask_lines))

    file_lock.release()


# 读文件；
def read_mask(mask_index):
    try:
        file_lock.acquire()

        with open(mask_file, 'r') as reader:
            mask_lines = reader.readlines()

        mask_dict = {}

        for mask_line in mask_lines:
            mask_line = mask_line.strip()
            database, index = mask_line.split()
            mask_dict[database] = index

        file_lock.release()

        if mask_dict.get(mask_index) is not None:
            return int(mask_dict.get(mask_index))
        else:
            return 0

    except Exception as e:
        file_lock.release()
        print(e)
        return 0


# 判断该文件是否是上次的;
def is_last_file(mask):
    with open(last_file, 'r') as reader:
        mask_str = reader.readlines()

    if len(mask_str) == 1:
        return mask_str[0].strip() == mask

    else:
        return False


# 写last_file;
def write_last_file(mask):
    with open(last_file, 'w') as writer:
        writer.write(mask)
