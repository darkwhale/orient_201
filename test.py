
from utils import *


def init():
    company_list = get_company_list('test')

    company_list[0].size = 200
    company_list[1].size = 180
    company_list[2].size = 170
    company_list[3].size = 160
    company_list[4].size = 100
    company_list[5].size = 79
    company_list[6].size = 50
    company_list[7].size = 20
    company_list[8].size = 7.8

    return company_list


def test():
    company_list = init()
    company_list = get_company_info(company_list)
    for i in company_list:
        print(i)
