import os
import platform
import random

# 每块硬盘最多能装的数据大小，以G为单位；
max_part_size = 300

# dest_host_list = ['01', '02', '03', '04', '05', '06',
#                   '11', '12', '13', '14', '15', '16',
#                   '21', '22', '23', '24', '25', '26', ]


# 快递公司类，用于记录每个公司属性；
class Company(object):
    def __init__(self,
                 company,
                 size=0,
                 dest_hosts=None):
        self.company = company
        self.size = size
        self.dest_hosts = dest_hosts

    def __lt__(self, other):
        return self.size < other.size

    def __str__(self):
        return self.company + str(self.size) + ',' + ','.join(self.dest_hosts)


# 判断系统位数；
def get_system_bytes():
    bite, system = platform.architecture()
    if bite.startswith('3'):
        return False
    if bite.startswith('6'):
        return True
    return True


# 获取文件夹下所有文件的绝对路径列表；
def get_file_list(file_dir):
    file_list = []

    for root, dirs, files in os.walk(file_dir):
        for name in files:
            file_list.append(os.path.join(root, name))

    file_list.sort()

    return file_list


# 分割列表；将total_list分为n份
def get_average_list(total_list, n):
    try:
        sub_lists = []

        batch_size = int(len(total_list) / n)
        for i in range(0, len(total_list), batch_size):
            block = total_list[i: i + batch_size]
            sub_lists.append(block)

        if len(sub_lists) != n:
            last_list_one = sub_lists.pop()
            last_list_two = sub_lists.pop()
            last_list_two.extend(last_list_one)
            sub_lists.append(last_list_two)

        return sub_lists

    except Exception as e:
        print(e)
        return [[]]


# 获取文件夹大小；
def get_origin_size(file_dir):
    file_size = 0

    for file in get_file_list(file_dir):
        file_size += os.path.getsize(file)

    return file_size


# 得到概率值标定的下标；
def get_host_by_percent(*args):
    sums = 0.0
    ran = random.random()
    print(ran)
    for index, arg in enumerate(args):
        sums += arg
        if ran < sums:
            return index
    return 0


# 计算每块数据的模块下标；
def get_hosts(size_list):

    current_size = 0
    batch_index = 0
    batch_indexs = []

    for size in size_list:
        if size > max_part_size:
            add_times = int(size / max_part_size) + 1
            # current_size == 0表示该标示未被使用；
            if current_size == 0:
                batch_indexs.extend([batch_index + add_time for add_time in range(add_times)])
                batch_index += add_times
            else:
                batch_indexs.extend([batch_index + add_time + 1 for add_time in range(add_times)])
                batch_index += add_times + 1
            # 使用下一个标示；
            current_size = 0
        else:
            if current_size + size > max_part_size:
                batch_index += 1
                current_size = size
            else:
                current_size += size
            batch_indexs.append(batch_index)

    return batch_indexs


# 获取公司列表；
def get_company_list(file_dir):
    company_list = []

    # 获取公司名和大小；
    for company in os.listdir(file_dir):
        company_name = company
        company_size = get_origin_size(company) / 1024 / 1024 / 1024

        company_list.append(Company(company_name, company_size))

    # 按照大小进行排序；
    company_list.sort()

    return company_list


# 获取快递公司的相关属性；
def get_company_info(company_list):
    try:

        # 获取模块的下标；
        size_list = [company.size for company in company_list]
        batch_indexes = get_hosts(size_list)

        batch_num = batch_indexes[-1]

        intend = int(batch_num / 3) + 1

        batch_index = 0
        for i in range(len(company_list)):

            block_num = int(company_list[i].size / max_part_size) + 1

            tmp_hosts = []
            for j in range(block_num):
                host = str(int(batch_indexes[batch_index] / intend)) + \
                    str(batch_indexes[batch_index] % intend + 1)
                tmp_hosts.append(host)
                batch_index += 1
            company_list[i].dest_hosts = tmp_hosts

        return company_list
    except Exception as e:
        print(e)



