# -*- coding: UTF-8 -*-
import sys
# import time


def process_bar(percent, width=50):
    percent = float(percent)

    use_num = int(percent*width)
    space_num = int(width - use_num)

    percent = percent * 100

    print_str = '[%s%s]%d' % (use_num*'#', space_num*' ', percent)

    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(print_str)
